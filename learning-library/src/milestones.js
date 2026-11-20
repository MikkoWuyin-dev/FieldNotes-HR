// Each first-iteration resource has one required action tick. Progress is
// self-reported; array positions never identify saved work.
function isGrandfathered(resource) {
  return state.done['resource:'+resource.id] === true && state.detailed[resource.id] !== true;
}
function resourceFraction(resource) {
  if (isGrandfathered(resource)) return 1;
  const required = resource.milestones.filter(m=>m.required);
  return required.length ? required.filter(m=>state.milestones[m.id]===true).length / required.length : 0;
}
function balancedProgress(resources) {
  const core=resources.filter(r=>!r.optional);
  const fractions=core.map(resourceFraction);
  const completed=fractions.filter(n=>n===1).length;
  const fraction=core.length ? fractions.reduce((a,b)=>a+b,0)/core.length : 0;
  return {total:core.length,completed,pct:completed===core.length && core.length ? 100 : Math.min(99,Math.floor(fraction*100+1e-9))};
}
function persistMilestoneState(candidate) {
  try {
    preserveProgressUpgradeSnapshot();
    const old=localStorage.getItem(STORAGE_KEY);
    if(old && !localStorage.getItem(STORAGE_KEY+':before-milestones-v3')) localStorage.setItem(STORAGE_KEY+':before-milestones-v3',old);
    localStorage.setItem(STORAGE_KEY,JSON.stringify(candidate));
  } catch (_) { setNotice('Could not save task progress. Existing progress was not replaced. Export a backup and retry.'); return false; }
  state=candidate; updateMilestoneViews(); updateDashboard(); updateStageMeters(); return true;
}
function changeMilestone(id,checked) {
  const candidate=normalizeProgress({...state,milestones:{...state.milestones,[id]:checked}});
  const saved=persistMilestoneState(candidate);
  if(!saved) updateMilestoneViews();
  else setNotice('Task saved.');
  return saved;
}
function switchToDetailed(resource) {
  if(!window.confirm('Use task tracking for this resource instead of its old Done mark? Your old progress stays in the backup.')) return;
  if(persistMilestoneState(normalizeProgress({...state,detailed:{...state.detailed,[resource.id]:true}}))){
    setNotice('Task tracking is on. Your old Done mark remains saved.');
  }
}
function updateMilestoneViews() {
  DATA.stages.forEach(stage=>stage.resources.forEach(resource=>{
    const card=document.querySelector(`[data-resource-id="${resource.id}"]`); if(!card) return;
    card.classList.toggle('done',resourceFraction(resource)===1);
    const required=resource.milestones.filter(m=>m.required);
    const n=required.filter(m=>state.milestones[m.id]===true).length;
    const inherited=isGrandfathered(resource);
    const status=card.querySelector('.completion');
    status.textContent=inherited?'Done before update':`${n}/${required.length}`;
    status.setAttribute('aria-label',inherited
      ? 'Done before task tracking; task details are not recorded.'
      : `${n} of ${required.length} ${required.length===1?'task':'tasks'} done`);
    const reopen=card.querySelector('.use-detailed'); if(reopen) reopen.hidden=!inherited;
    card.querySelectorAll('input[data-milestone-id]').forEach(input=>{input.checked=state.milestones[input.dataset.milestoneId]===true;});
  }));
}
function splitAccessPoints(text) {
  const points=[]; let start=0;
  function push(end) {
    const point=text.slice(start,end).trim();
    if(point) points.push(point.replace(/^([a-z])/,(_,letter)=>letter.toUpperCase()));
    start=end; while(/\s/.test(text[start]||'')) start++;
  }
  for(let i=0;i<text.length;i++) {
    if(text[i]===';') { push(i+1); continue; }
    if(!'.!?'.includes(text[i])) continue;
    const next=text.slice(i+1).match(/^\s+(\S)/);
    if(!next || !/[A-Z“\"0-9]/.test(next[1])) continue;
    const before=text.slice(start,i+1);
    if(/(?:^|\s)(?:Dr|Mr|Mrs|Ms|Prof|St)\.$/.test(before)) continue;
    if(/(?:^|\s)(?:e\.g|i\.e|U\.S)\.$/.test(before)) continue;
    push(i+1);
  }
  if(start<text.length) {
    const point=text.slice(start).trim();
    if(point) points.push(point.replace(/^([a-z])/,(_,letter)=>letter.toUpperCase()));
  }
  return points;
}
function accessList(className,text,label) {
  const list=el('ul',className); list.setAttribute('aria-label',label);
  splitAccessPoints(text).forEach(point=>list.append(el('li','',point)));
  return list;
}
function buildRoadmap() {
  buildLegacyRoadmap();
  // Keep full stage copy in source and generated library documents, but omit
  // descriptions and repeated outcome bullets from the concise tracker accordions.
  document.querySelectorAll('.stage-body > .stage-description, .stage-body > .outcomes').forEach(copy=>copy.remove());
  DATA.stages.forEach((stage,si)=>stage.resources.forEach((resource,ri)=>{
    const stageNode=document.querySelectorAll('.stage')[si];
    const card=stageNode && stageNode.querySelectorAll('.resource')[ri];
    if(!card) throw new Error(`resource card missing for ${resource.id}`);
    card.dataset.resourceId=resource.id;
    const old=card.querySelector('.completion'); const status=el('span','completion');
    status.setAttribute('aria-label','Task progress'); old.replaceWith(status);
    const content=card.querySelector('.resource-top > div');
    content.querySelectorAll('p').forEach(p=>{if(p.textContent.startsWith('Next action:'))p.remove();});
    const accessNote=[...content.querySelectorAll('p')].find(p=>p.textContent===resource.access_note);
    if(!accessNote || !resource.access_summary) throw new Error(`access summary missing for ${resource.id}`);
    const summary=accessList('access-summary',resource.access_summary,'Access summary');
    const firstSummaryPoint=summary.querySelector('li');
    if(firstSummaryPoint) firstSummaryPoint.prepend(document.createTextNode('Access: '));
    const access=el('details','resource-access');
    access.append(el('summary','','How access was checked'));
    content.insertBefore(summary,accessNote);
    content.insertBefore(access,accessNote);
    access.append(accessNote);
    accessNote.replaceWith(accessList('access-note-list',resource.access_note,'Access and verification details'));
    const reopen=el('button','use-detailed','Track this task');reopen.type='button';
    reopen.addEventListener('click',()=>switchToDetailed(resource)); content.append(reopen);
    const detail=el('details','milestones');detail.append(el('summary','','Study task'));
    const list=el('ul','milestone-list');
    resource.milestones.forEach(m=>{
      if(!m.required)return;
      const li=el('li');const label=el('label','milestone-label');const input=el('input');input.type='checkbox';
      input.dataset.milestoneId=m.id;input.setAttribute('aria-label',`${resource.title}: ${m.label}`);
      input.addEventListener('change',()=>changeMilestone(m.id,input.checked));
      label.append(input,el('span','',m.label));li.append(label);list.append(li);
    });
    detail.append(list);content.append(detail);
  }));
  renderPriorLearning();
  updateMilestoneViews();updateDashboard();updateStageMeters();
}
function renderPriorLearning() {
  document.getElementById('prior-learning')?.remove();
  const activeKeys=new Set([
    ...DATA.stages.map(stage=>'stage:'+stage.id),
    ...DATA.stages.flatMap(stage=>stage.resources.map(resource=>'resource:'+resource.id))
  ]);
  const previousCompletions=Object.entries(state.done).filter(([key,value])=>value===true&&!activeKeys.has(key)).length;
  const activeIds=new Set(DATA.stages.flatMap(stage=>stage.resources.flatMap(resource=>resource.milestones.map(m=>m.id))));
  const previousTicks=Object.entries(state.milestones).filter(([id,value])=>value===true&&!activeIds.has(id)).length;
  if(!previousCompletions&&!previousTicks)return;
  const panel=el('details','prior-learning');panel.id='prior-learning';
  panel.append(el('summary','',`Saved from older versions: ${previousCompletions} completions, ${previousTicks} task checks`));
  panel.append(el('p','','Older or unknown items stay in your backup but do not count here. Check-ins are separate.'));
  panel.append(el('p','','Download a backup before clearing progress.'));
  document.getElementById('roadmap').prepend(panel);
}
function updateDashboard() {
  const resources=DATA.stages.flatMap(stage=>stage.resources), result=balancedProgress(resources);
  document.getElementById('overall-percent').textContent=`${result.pct}%`;
  document.getElementById('progress-label').textContent=`${result.completed} of ${result.total} tasks done`;
  const fill=document.getElementById('progress-fill');fill.style.width=`${result.pct}%`;fill.parentElement.setAttribute('aria-valuenow',String(result.pct));
  fill.parentElement.setAttribute('aria-valuetext',`${result.pct}% complete; ${result.completed} of ${result.total} tasks done`);
  document.getElementById('streak-count').textContent=String(streakLength());renderDailyCheckin();
  const next=resources.find(resource=>!resource.optional&&resourceFraction(resource)<1);
  document.getElementById('next-step').textContent=next?`Next: ${next.title}`:'All tasks are done. Revisit any resource when you like.';
}
function updateStageMeters() {
  DATA.stages.forEach((stage,si)=>{
    const meter=document.querySelector(`[data-meter="${si}"]`);if(meter)meter.textContent=`${balancedProgress(stage.resources).pct}%`;
  });
}
