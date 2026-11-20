"""Daily attendance migration and transactional state tests, using actual JS."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'learning-library/tools'))
import content
import build_tracker as bt

class CheckinTests(unittest.TestCase):
    def test_attendance_transactions_and_migration(self):
        data=content.app_data(content.load())
        adapter=next(new for _,new,label in bt.progress_edits(data) if label=='progress loader').split('\nfunction loadLegacyState()')[0]
        vendor=(content.REPO/'.agents/skills/resource-learning-library/scripts/interactive_app.py').read_text()
        start=vendor.index('function streakLength() {')
        streak=vendor[start:vendor.index('function resourceKey',start)]
        helpers='\n'.join(line for line in vendor.splitlines() if line.startswith(('function dateFromKey(', 'function previousDay(')))
        source='const assert=require("node:assert/strict"); const DATA='+json.dumps(data)+';\n'+adapter+'\n'+helpers+'\n'+streak+r'''
let today='2026-10-26';
function localDateKey(date){return date ? `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}` : today;}
function updateDashboard(){}
let notice=''; function setNotice(text){notice=text;}
const STORAGE_KEY='test-state';
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
assert.equal(streakLength(),2);
assert.equal(store.get(STORAGE_KEY+':before-checkins-v3'),JSON.stringify(legacy));
assert.equal(changeDailyCheckin(),true);
assert.deepEqual(state.manualCheckinDates,['2026-10-26']);
assert.deepEqual(normalizeProgress(JSON.parse(store.get(STORAGE_KEY)),true),state);
assert.equal(changeDailyCheckin(true),true);
assert.deepEqual(state.activityDates,['2026-10-25']);
assert.equal(streakLength(),1); // yesterday's run remains visible
// Undo must preserve a same-day inherited activity date.
state=normalizeProgress({...legacy,activityDates:[today]},true);
assert.equal(changeDailyCheckin(),true); assert.equal(changeDailyCheckin(true),true);
assert.deepEqual(state.activityDates,[today]);
// Advancing the local calendar must not award tomorrow's attendance automatically.
today='2026-10-27';
assert.equal(state.activityDates.includes(today),false);
assert.equal(streakLength(),1);
// Storage failure leaves the previous persisted and in-memory progress unchanged.
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
// Import never invents today's attendance or asks for notification permission.
const imported=normalizeProgress(legacy,true);
assert.equal(imported.activityDates.includes(today),false);
assert.equal(imported.notificationsEnabled,false);
'''
        proc=subprocess.run(['node','-e',source],capture_output=True,text=True,timeout=15)
        self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
