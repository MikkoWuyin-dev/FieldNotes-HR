"""Phase 2 canonical projections, extension and saved-progress regression tests."""
import copy
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'learning-library/tools'))
import content
import build_tracker as bt

class ContentTests(unittest.TestCase):
    def test_frozen_history_and_legacy_aliases(self):
        self.assertEqual(hashlib.sha256((content.SRC/'progress-compatibility.json').read_bytes()).hexdigest(), '3a91f90d7d163d8975ca358a2d85d3da8ef3b91e1b6614c93c6438997fee1a48')
        self.assertEqual(hashlib.sha256((content.SRC/'history/first-link-sweep.json').read_bytes()).hexdigest(), '60c7195ed156f0c4d973a12bbbb932d99f5ff5464538daf1cc0265077cc720cd')

    def test_retired_coursera_evidence_and_progress_alias(self):
        data=content.load()
        active_ids={r['id'] for stage in data['stages'] for r in stage['resources']}
        self.assertNotIn('coursera-hiring',active_ids)
        self.assertEqual(content.totals(data)['cards'],20)
        self.assertEqual(content.totals(data)['free'],20)

        course_url='https://www.coursera.org/learn/recruiting-hiring-onboarding-employees'
        help_url='https://learner.coursera.help/hc/en-us/articles/209818613-Enrollment-options'
        indexed={item['url']:item for item in data['verification']['urls']}
        self.assertEqual(indexed[course_url]['status'],'ambiguous')
        self.assertIn('trial',indexed[course_url]['note'].lower())
        manifest=json.loads((content.SRC/'verification-manifest.json').read_text())
        projected={item['url']:item for item in manifest['urls']}
        self.assertIn(course_url,projected)
        self.assertIn(help_url,projected)

        ledger=json.loads((content.SRC/'progress-compatibility.json').read_text())
        self.assertEqual(ledger['resources']['coursera-hiring'],['s1-r3'])

    def test_projections_current(self):
        content.generate(check=True)

    def test_invalid_catalogue_rejected(self):
        for mutation in ('id','hours','date','study','certificate','account','evidence'):
            d=content.load(); r=d['stages'][0]['resources'][0]
            if mutation=='id': r['id']=d['stages'][0]['id']
            elif mutation=='hours': d['stages'][0]['estimated_hours']=0
            elif mutation=='date': r['checked_at']='2026-02-30'
            elif mutation=='evidence': r['access']['evidence_urls']=['https://invalid.example']
            else: r['access'][mutation]='invalid'
            with self.subTest(mutation=mutation),self.assertRaises((ValueError,KeyError)):
                content.validate(d)

    def test_fact_edit_reaches_projections(self):
        d=content.load(); r=d['stages'][0]['resources'][0]; r['title']='Unique title example'; r['why']='Unique explanation example'
        d['stages'][0]['estimated_hours']+=1
        app=content.app_data(d); md=content.markdown(d)
        self.assertEqual(app['stages'][0]['resources'][0]['title'],r['title'])
        self.assertIn(r['title'],md)
        self.assertIn(r['why'],md)
        self.assertEqual(app['stages'][0]['resources'][0]['why'],content.load_app_copy(d)['resources'][r['id']]['why'])
        self.assertIn('95 planned study hours',md)
        self.assertIn('95 HOURS', ' '.join(bt.facts(app)))

    def test_app_copy_stays_app_only_and_covers_active_items(self):
        d=content.load(); original=copy.deepcopy(d); app=content.app_data(d)
        app_copy=content.load_app_copy(d)
        self.assertEqual(d,original)
        self.assertEqual(app['subtitle'],app_copy['subtitle'])
        for stage,projected in zip(d['stages'],app['stages']):
            display=app_copy['stages'][stage['id']]
            self.assertEqual(projected['description'],display['description'])
            for resource,app_resource in zip(stage['resources'],projected['resources']):
                display=app_copy['resources'][resource['id']]
                self.assertEqual(app_resource['why'],display['why'])
                self.assertEqual(app_resource['action'],display['action'])
                self.assertEqual(app_resource['milestones'][0]['label'],display['action'])
                self.assertEqual(app_resource['access_summary'],display['access_summary'])
                self.assertEqual(app_resource['access_note'],resource['access_note'])
        # Detailed catalogue wording remains in the library document.
        self.assertIn(d['stages'][0]['resources'][0]['why'],content.markdown(d))
        self.assertIn(d['stages'][0]['resources'][0]['access_note'],content.markdown(d))
        broken=copy.deepcopy(d); broken['stages'][0]['resources'][0]['id']='new-resource'
        with self.assertRaisesRegex(ValueError,'app-copy resources'):
            content.load_app_copy(broken)

    def test_contracts_missing_and_duplicate(self):
        d=content.app_data(content.load())
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'base.html'; bt.interactive_app.build_app(d,p); base=p.read_text()
        for pattern,_,label in bt.branding_edits(d):
            match=re.search(pattern,base)
            for malformed in (base[:match.start()]+base[match.end():],base+match[0]):
                with self.subTest(label=label),self.assertRaisesRegex(RuntimeError,label):
                    bt.transform(malformed,d,'')
        for old,_,label in bt.progress_edits(d):
            for malformed in (base.replace(old,'',1),base+old):
                with self.subTest(label=label),self.assertRaisesRegex(RuntimeError,label):
                    bt.apply_progress(malformed,d)
        themed=bt.transform(base,d,'')
        for pattern,_,label in bt.pals_edits(bt.load_pals_sources()):
            match=re.search(pattern,themed)
            for malformed in (themed[:match.start()]+themed[match.end():],themed+match[0]):
                with self.subTest(label=label),self.assertRaisesRegex(RuntimeError,label):
                    bt.inject_pals(malformed,bt.load_pals_sources())
        for malformed in (base.replace('</head>',''),base+'</head>'):
            with self.assertRaisesRegex(RuntimeError,'</head>'):
                bt.transform(malformed,d,'')

    @unittest.skipUnless(shutil.which('node'),'Node required for progress tests')
    def test_progress_migration_backup_and_reorder(self):
        data=content.app_data(content.load())
        edits=bt.progress_edits(data)
        by_label={label:new for _,new,label in edits}
        adapter=by_label['progress loader'].split('\nfunction loadLegacyState()')[0]
        script='const assert=require("node:assert/strict");\nconst DATA='+json.dumps(data)+';\n'+adapter+'\n'+by_label['progress-key']+'\n'+by_label['stage-key']+r'''
const legacy={version:1,done:{'hr-essentials-v1':true,'s0-r0':true,'s0-r2':true,'s1-r3':true,'s0-complete':true,'retired-key':true},activityDates:['2026-10-26','2026-02-30','2026-10-26'],reminderTime:'25:99'};
const migrated=normalizeProgress(legacy,true);
assert.equal(migrated.done['resource:hr-essentials'],true);
assert.equal(migrated.done['resource:talent-acquisition'],true);
assert.equal(migrated.done['resource:openstax-hr'],true);
assert.equal(migrated.done['resource:coursera-hiring'],true);
assert.equal(migrated.done['stage:orientation'],true);
assert.equal(migrated.done['retired-key'],true);
assert.deepEqual(migrated.activityDates,['2026-10-26']);
assert.equal(migrated.reminderTime,'19:00');
assert.deepEqual(normalizeProgress(JSON.parse(JSON.stringify(migrated)),true),migrated);
assert.equal(normalizeProgress({...legacy,done:{'s0-r0':true,'resource:talent-acquisition':false}},true).done['resource:talent-acquisition'],false);
for(const done of [null,[],{'s0-r0':'true'},{'s0-r0':1}]) assert.throws(()=>normalizeProgress({...legacy,done},true));
for(const version of [0,4,'1']) assert.throws(()=>normalizeProgress({...legacy,version},true));
assert.throws(()=>normalizeProgress({...legacy,storage_id:'another-roadmap'},true));
const before=DATA.stages.flatMap((s,si)=>s.resources.map((r,ri)=>[r.id,resourceKey(si,ri)]));
DATA.stages.reverse(); DATA.stages.forEach(s=>s.resources.reverse());
DATA.stages[0].resources.unshift({id:'new-card'});
for(const [id,key] of before) {
 const si=DATA.stages.findIndex(s=>s.resources.some(r=>r.id===id));
 const ri=DATA.stages[si].resources.findIndex(r=>r.id===id);
 assert.equal(resourceKey(si,ri),key);
}
assert.equal(migrated.done[resourceKey(0,0)],undefined);
'''
        subprocess.run(['node','-e',script],check=True,capture_output=True,text=True)

if __name__=='__main__': unittest.main()
