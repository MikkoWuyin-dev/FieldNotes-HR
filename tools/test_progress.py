"""Milestone progress and explicit attendance use the real JavaScript source."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'learning-library/tools'))
import content
import build_tracker as bt


def app_data():
    return content.app_data(content.load())


def progress_source(data):
    edits = {label: new for _, new, label in bt.progress_edits(data)}
    return edits['progress loader'].split('\nfunction loadLegacyState()')[0]


class ProgressTests(unittest.TestCase):
    @unittest.skipUnless(__import__('shutil').which('node'), 'Node required for progress tests')
    def test_balanced_action_ticks_and_legacy_completion(self):
        data = app_data()
        adapter = progress_source(data)
        script = 'const assert=require("node:assert/strict"); const DATA=' + json.dumps(data) + ';\n' + adapter + r'''
let today='2026-10-26';
function localDateKey(){return today;}
let notice=''; function setNotice(text){notice=text;}
const store=new Map(); let failWrite=false;
const STORAGE_KEY='first-iteration-test';
const localStorage={getItem:key=>store.get(key)||null,setItem:(key,value)=>{if(failWrite)throw Error('quota');store.set(key,value);}};
const document={querySelector:()=>null};
const window={confirm:()=>true};
let state=normalizeProgress({done:{}});
updateDashboard=()=>{};
const all=DATA.stages.flatMap(stage=>stage.resources);
assert.equal(DATA.stages.length,8);
assert.equal(all.length,20);
assert.equal(balancedProgress(all).total,20);
assert(all.every(resource=>resource.milestones.length===1));
assert(all.every(resource=>resource.milestones[0].label===resource.action));
assert.equal(balancedProgress(all).pct,0);
const first=all[0];
// Preserve an older payload exactly before normalizing active progress.
const previous={version:3,storage_id:DATA.storage_id,title:'previous roadmap version',
  done:{'resource:legacy-unmapped':true},activityDates:['2026-10-25'],
  manualCheckinDates:[],legacyActivityDates:['2026-10-25'],
  milestones:{'legacy-action':true},detailed:{}};
const previousPayload=JSON.stringify(previous);store.set(STORAGE_KEY,previousPayload);
state=loadState();
assert.equal(state.done['resource:legacy-unmapped'],true);
assert.equal(changeMilestone(first.milestones[0].id,true),true);
assert.equal(store.get(STORAGE_KEY+':before-progress-v3'),previousPayload);
assert.equal(state.milestones['legacy-action'],true);
assert.equal(resourceFraction(first),1);
assert.equal(balancedProgress(all).completed,1);
assert.equal(balancedProgress(all).pct,5);
assert.deepEqual(state.activityDates,['2026-10-25']);
assert.deepEqual(state.manualCheckinDates,[]);
// The unchanged first-iteration card completion receives prior credit.
state=normalizeProgress({version:2,done:{'hr-essentials-v1':true},activityDates:[]},true);
assert.equal(state.done['resource:hr-essentials'],true);
assert.equal(resourceFraction(first),1);
window.confirm=()=>false; switchToDetailed(first);
assert.equal(state.detailed[first.id],undefined);
window.confirm=()=>true;
store.set(STORAGE_KEY,JSON.stringify(state));
switchToDetailed(first);
assert.equal(state.detailed[first.id],true);
assert.equal(state.done['resource:hr-essentials'],true);
assert.equal(resourceFraction(first),0);
assert.equal(changeMilestone(first.milestones[0].id,true),true);
assert.equal(resourceFraction(first),1);
assert.equal(state.done['resource:hr-essentials'],true);
// Every action contributes one equal resource fraction; optional future cards do not gate.
const complete=Object.fromEntries(all.map(resource=>[resource.milestones[0].id,true]));
state=normalizeProgress({done:{},milestones:complete});
assert.equal(balancedProgress(all).pct,100);
assert.equal(balancedProgress([...all,{...first,id:'optional-test',optional:true}]).pct,100);
const floorTest={id:'floor-test',optional:false,milestones:Array.from({length:1000},(_,i)=>({id:'floor-'+i,required:true}))};
state=normalizeProgress({done:{},milestones:Object.fromEntries(floorTest.milestones.slice(1).map(m=>[m.id,true]))});
assert.equal(balancedProgress([floorTest]).pct,99);
// Unknown boolean leaves survive a v3 backup round trip.
state=normalizeProgress({...state,milestones:{...state.milestones,'future-leaf':false}});
assert.equal(normalizeProgress(JSON.parse(JSON.stringify(state)),true).milestones['future-leaf'],false);
const before=JSON.stringify(state),persisted=store.get(STORAGE_KEY);
failWrite=true;
assert.equal(changeMilestone('future-write',true),false);
assert.equal(JSON.stringify(state),before);
assert.equal(store.get(STORAGE_KEY),persisted);
assert.match(notice,/Could not save/);
failWrite=false;
for(const patch of [{milestones:null},{milestones:{bad:1}},{detailed:[]},{detailed:{bad:'yes'}}])assert.throws(()=>normalizeProgress({...state,...patch},true));
'''
        proc = subprocess.run(['node', '-e', script], capture_output=True, text=True, timeout=15)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    @unittest.skipUnless(__import__('shutil').which('node'), 'Node required for check-in tests')
    def test_checkin_migration_streak_undo_and_storage_failure(self):
        data = app_data()
        adapter = progress_source(data)
        vendor = (ROOT / '.agents/skills/resource-learning-library/scripts/interactive_app.py').read_text()
        start = vendor.index('function streakLength() {')
        streak = vendor[start:vendor.index('function resourceKey', start)]
        helpers = '\n'.join(line for line in vendor.splitlines() if line.startswith(('function dateFromKey(', 'function previousDay(')))
        script = 'const assert=require("node:assert/strict"); const DATA=' + json.dumps(data) + ';\n' + adapter + '\n' + helpers + '\n' + streak + r'''
let today='2026-10-26';
function localDateKey(date){return date ? `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}` : today;}
function updateDashboard(){}
let notice=''; function setNotice(text){notice=text;}
const STORAGE_KEY='first-iteration-checkin-test';
const store=new Map(); let failWrite=false;
const localStorage={getItem:key=>store.get(key)||null,setItem:(key,value)=>{if(failWrite)throw Error('quota');store.set(key,value);}};
const legacy={version:2,storage_id:DATA.storage_id,done:{'s0-r0':true},activityDates:['2026-10-25'],reminderTime:'08:30'};
let state=normalizeProgress(legacy,true);
assert.equal(state.version,3);
assert.equal(state.done['resource:talent-acquisition'],true);
assert.deepEqual(state.legacyActivityDates,['2026-10-25']);
assert.deepEqual(state.manualCheckinDates,[]);
store.set(STORAGE_KEY,JSON.stringify(legacy));
const progress=JSON.stringify(state.done);
assert.equal(changeDailyCheckin(),true);
assert.equal(JSON.stringify(state.done),progress);
assert.deepEqual(state.activityDates,['2026-10-25','2026-10-26']);
assert.deepEqual(state.manualCheckinDates,['2026-10-26']);
assert.equal(streakLength(),2);
assert.equal(store.get(STORAGE_KEY+':before-progress-v3'),JSON.stringify(legacy));
assert.equal(store.get(STORAGE_KEY+':before-checkins-v3'),JSON.stringify(legacy));
assert.deepEqual(normalizeProgress(JSON.parse(store.get(STORAGE_KEY)),true),state);
assert.equal(changeDailyCheckin(),true);
assert.deepEqual(state.manualCheckinDates,['2026-10-26']);
assert.equal(changeDailyCheckin(true),true);
assert.deepEqual(state.activityDates,['2026-10-25']);
assert.equal(streakLength(),1);
// Undo must preserve a same-day inherited activity date.
state=normalizeProgress({...legacy,activityDates:[today]},true);
store.set(STORAGE_KEY,JSON.stringify({...legacy,activityDates:[today]}));
assert.equal(changeDailyCheckin(),true); assert.equal(changeDailyCheckin(true),true);
assert.deepEqual(state.activityDates,[today]);
// A new local day does not receive automatic attendance.
today='2026-10-27';
assert.equal(state.activityDates.includes(today),false);
assert.equal(streakLength(),1);
// Failed storage writes leave both the in-memory and saved state unchanged.
const before=JSON.stringify(state), persisted=store.get(STORAGE_KEY);
failWrite=true;
assert.equal(changeDailyCheckin(),false);
assert.equal(JSON.stringify(state),before);
assert.equal(store.get(STORAGE_KEY),persisted);
assert.match(notice,/Could not save/);
failWrite=false;
for(const bad of [
 {...state,storage_id:'foreign'},
 {...state,manualCheckinDates:null},
 {...state,legacyActivityDates:['2026-02-30']},
 {...state,version:4}
]) assert.throws(()=>normalizeProgress(bad,true));
// Imported study dates stay historical; import cannot create an attendance tick or permission.
const imported=normalizeProgress(legacy,true);
assert.equal(imported.activityDates.includes(today),false);
assert.equal(imported.notificationsEnabled,false);
'''
        proc = subprocess.run(['node', '-e', script], capture_output=True, text=True, timeout=15)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


if __name__ == '__main__':
    unittest.main()
