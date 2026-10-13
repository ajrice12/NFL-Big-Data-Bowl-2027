import {esc,fmt,pct,count,loadCatalog,loadTrajectory,loadAppendix} from './data.js';
import {drawField,drawSeries,observedFrame} from './field.js';
export const isMirror=t=>t.drill.replaceAll('-','_').includes('PASS_PRO_MIRROR');
const drillLabel=name=>({'PASS_PRO_MIRROR_DRILL':'Pass protection / mirror','PASS_RUSH_DROP':'Pass rush / drop','FIVE_YARD_WAVE_DRILL_SLIDE_AND_SHUFFLE':'Five-yard wave / slide & shuffle'}[name]||name.replaceAll('_',' '));
export function labMarkup({metric=false}={}){
 return `<div class="movement-workspace ${metric?'metric-workspace':''}">
 <div class="viewer-controls"><label>Drill<select id="drill" aria-label="Drill"></select></label><label>Athlete A<select id="player-a" aria-label="Athlete A"></select></label>${metric?'':`<label>Athlete B<select id="player-b" aria-label="Athlete B"></select></label>`}<label>${metric?'Target':'View'}<select id="${metric?'target-fraction':'view-mode'}" aria-label="${metric?'Recovery target':'Comparison view'}">${metric?'<option value="0.15">15% excursion</option><option value="0.2" selected>20% excursion</option><option value="0.25">25% excursion</option>':'<option value="overlay">Overlay</option><option value="split">Side by side</option>'}</select></label></div>
 <div id="viewer-status" class="viewer-status" role="status">Loading selected attempts…</div>
 <div class="film-layout"><div class="film"><div class="scorebug" id="scorebug"></div><div id="fields" class="fields"><canvas id="field" width="1200" height="580" aria-label="Football field with actual Combine movement"></canvas><canvas id="field-b" width="1200" height="580" aria-label="Football field athlete B" hidden></canvas></div><div class="transport"><button id="play" disabled>Play</button><button id="restart" disabled>Replay</button><select id="speed" aria-label="Playback speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select><input id="timeline" type="range" min="0" max="10" step="0.01" value="0" aria-label="Timeline" disabled><output id="time">— s</output></div><canvas id="series" width="1200" height="125" aria-label="Synchronized speed versus time"></canvas><div class="film-legend"><span><i class="white"></i>Athlete A</span>${metric?'':'<span><i class="yellow"></i>Athlete B</span>'}<span>◇ Reversal</span><span>○ Reset reached</span><label>Trail color<select id="encoding" aria-label="Trail color"><option value="athlete">Athlete</option><option value="speed">Speed · white → yellow</option><option value="acceleration">Δspeed · blue → yellow</option></select></label></div></div><aside class="film-analysis" id="film-analysis"></aside></div>
 <p class="field-disclosure">Schematic field, not the recorded NFL location. Markings give football context; the scale bar uses source coordinates. Shared scale, translated starts, no rotation or interpolation. Speed uses reported units; acceleration is Δspeed/Δt. Gaps break trails.</p></div>`;
}
export function mountLab(data,{metric=false,preferred=[],onSelection=()=>{}}={}){
 const $=id=>document.getElementById(id);let alive=true,version=0,chosen=[],elapsed=0,duration=1,playing=false,raf=0,last=0,pool=[],catalog=[],first=true,variants=null,eventIndex=0;
 const drill=$('drill'),a=$('player-a'),b=$('player-b'),status=$('viewer-status');
 function stop(){playing=false;cancelAnimationFrame(raf);if(alive)$('play').textContent='Play';}
 function disable(value){['play','restart','timeline'].forEach(id=>$(id).disabled=value);}
 function error(e){if(!alive)return;stop();disable(true);document.querySelector('.film').classList.add('unavailable');$('film-analysis').innerHTML='<p>No selected trajectory is displayed while data is unavailable.</p>';status.className='viewer-status failed';status.textContent=`Selected attempt unavailable: ${e.message}. Rebuild the local export or choose another athlete.`;}
 function populate(){
  pool=catalog.filter(t=>t.drill===drill.value);
  const options=pool.map(t=>`<option value="${esc(t.id)}">${esc(t.name)} · ${t.position} · ${t.year} · att ${t.attempt}</option>`).join('');
  a.innerHTML=options;if(b)b.innerHTML=options;
  [a,b].filter(Boolean).forEach((select,i)=>{const target=pool.find(t=>t.nfl_id===preferred[i]);select.value=(target||pool[Math.min(i,pool.length-1)]).id;});
  loadSelected();
 }
 async function loadSelected(){
  stop();disable(true);const token=++version;status.className='viewer-status';status.textContent='Loading selected recorded attempts…';
  try{
   const selected=[a,b].filter(Boolean).map(select=>pool.find(t=>t.id===select.value));
   const tracks=await Promise.all(selected.map(loadTrajectory));
   if(!alive||token!==version)return;
   chosen=tracks;variants=null;eventIndex=0;
   if(metric){const extra=await loadAppendix();if(!alive||token!==version)return;variants=extra.worked_examples.find(v=>v.nfl_id===tracks[0].nfl_id)?.variants;applyVariant(false);}
   duration=Math.max(...chosen.map(t=>t.frames.at(-1)[0]-t.frames[0][0]));elapsed=first?Math.min(duration,chosen[0].reversals[0]?.time+.3||1.5):0;first=false;
   $('timeline').max=duration;document.querySelector('.film').classList.remove('unavailable');disable(false);status.textContent=`${chosen.map(t=>`${t.name}: ${t.frames.length} recorded frames`).join(' / ')}`;onSelection(chosen.map(t=>t.nfl_id));buildSidebar();draw();
  }catch(e){if(token===version)error(e);}
 }
 function applyVariant(reset=true){
  const variant=variants?.find(v=>v.fraction===Number($('target-fraction').value));
  if(variant)chosen[0]={...chosen[0],summary:variant.summary,reversals:variant.reversals};
  if(reset){stop();eventIndex=Math.min(eventIndex,chosen[0].reversals.length-1);buildSidebar();jump('recovery');}
 }
 function buildSidebar(){
  if(metric){const t=chosen[0];$('film-analysis').innerHTML=`<p class="kicker">HOW THE RESET IS MEASURED</p><h3>Move. Reverse. Recover.</h3><p class="short">After a direction change, how long does it take to regain a set amount of displacement?</p><label class="event-control">Observed reversal<select id="reversal-event" aria-label="Reversal event">${t.reversals.map((r,i)=>`<option value="${i}" ${i===eventIndex?'selected':''}>R${i+1} · ${fmt(r.time)} s</option>`).join('')}</select></label><div class="phase-buttons"><button data-phase="approach">1 Move</button><button data-phase="reversal">2 Reverse</button><button data-phase="recovery">3 Recover</button></div><div id="event-measure"></div><div class="metric-definition"><b>Recovery delay =</b><br>first target-hit time − reversal time</div><p class="small">Target = ${Math.round(Number($('target-fraction').value)*100)}% of p90–p10 projected excursion. Yellow dashed line marks the displacement target, not a first-down line.</p><p class="caution">A candidate movement feature. No added scouting value established.</p>`;
   $('reversal-event').onchange=()=>{eventIndex=Number($('reversal-event').value);jump('reversal');};document.querySelectorAll('[data-phase]').forEach(button=>button.onclick=()=>jump(button.dataset.phase));
  }else{
   $('film-analysis').innerHTML=`<p class="kicker">MOVEMENT → ROOKIE NFL</p><h3>What the film measures</h3><p class="short">Reset time describes the Combine drill. Pressure rate describes observed NFL opportunities. Their relationship remains unvalidated.</p>${chosen.map((t,i)=>{const n=t.nfl;return `<article class="player-note ${i?'athlete-b':''}"><h4>${i?'B':'A'} / ${esc(t.name)}</h4><div class="comparison-number">${isMirror(t)?fmt(t.summary.recovery_delay):'—'}<small> s reset</small></div><p>${isMirror(t)?`${t.summary.completed}/${t.summary.reversals} reversals completed`:'LRE not defined for this drill'}</p><div class="nfl-pair"><b>${pct(n?.pressure_rate)}<span>ANY PRESSURE</span></b><b>${count(n?.opportunities)}<span>OPPORTUNITIES</span></b></div><p class="small">${n?`${pct(n.long_pressure_rate)} on ${count(n.long_opportunities)} dropbacks ≥3 s. Mean pressure time ${fmt(n.mean_pressure_time)} s among valid pressure events.`:'No eligible rookie NFL observations; no outcome is substituted.'}</p></article>`}).join('')}<a class="text-link" href="#metric">See the recovery measurement →</a>`;
  }
 }
 function jump(phase){stop();const r=chosen[0].reversals[eventIndex];if(!r)return;elapsed=Math.max(0,Math.min(duration,phase==='approach'?r.time-.5:phase==='reversal'?r.time:r.completed?r.time+r.delay:r.time+r.observed_until));document.querySelectorAll('[data-phase]').forEach(b=>b.classList.toggle('active',b.dataset.phase===phase));draw();}
 function draw(){
  if(!alive||!chosen.length)return;
  $('timeline').value=elapsed;$('time').textContent=`${fmt(elapsed)} / ${fmt(duration)} s`;
  const split=!metric&&$('view-mode').value==='split';$('fields').classList.toggle('split-view',split);$('field-b').hidden=!split;
  // Both split fields use the same pair geometry and color identity.
  if(split){drawField($('field'),chosen,elapsed,{ghost:true,encoding:$('encoding').value,only:0});drawField($('field-b'),chosen,elapsed,{ghost:true,encoding:$('encoding').value,only:1});}
  else drawField($('field'),chosen,elapsed,{ghost:true,encoding:$('encoding').value,focus:metric});
  drawSeries($('series'),chosen,elapsed,duration);
  $('scorebug').innerHTML=chosen.map((t,i)=>{const idx=observedFrame(t,elapsed),f=t.frames[idx],r=t.reversals.filter(r=>r.index<=idx).at(-1),gap=idx+1<t.frames.length&&t.frames[idx+1][0]-f[0]>.15&&elapsed>f[0]-t.frames[0][0]+.15,ended=elapsed>t.frames.at(-1)[0]-t.frames[0][0];return `<div class="athlete-score ${i?'athlete-b':''}"><div class="identity"><b>${esc(t.name)}</b><span>${t.position} · ${t.year} · ID ${t.nfl_id} · ATT ${t.attempt}</span></div><div class="live-stat"><b>${fmt(f[3],1)}</b><span>SPEED</span></div><div class="live-stat"><b>${fmt(f[4],1)}</b><span>ΔSPEED/S</span></div><div class="frame-tag">F${idx+1}/${t.frames.length}<span>${gap?'GAP / HELD':ended?'COMPLETE':r&&elapsed-r.time<.65?'DIRECTION CHANGE':'RECORDED'}</span></div></div>`}).join('');
  if(metric){const r=chosen[0].reversals[eventIndex];$('event-measure').innerHTML=r?`<div class="recovery-value">${r.completed?fmt(r.delay):'—'}<small>seconds${r.completed?' to target':' / censored'}</small></div><p class="small">Reversal ${fmt(r.time)} s → ${r.completed?`target ${fmt(r.time+r.delay)} s`:'target not observed'}. Displacement ${fmt(r.target_displacement,3)} source units.</p>`:'<p>No defined recovery for this attempt.</p>';}
 }
 function tick(now){if(!playing||!alive)return;elapsed+=Math.min((now-last)/1000,.25)*Number($('speed').value);last=now;if(elapsed>=duration){elapsed=duration;stop();}draw();if(playing)raf=requestAnimationFrame(tick);}
 drill.onchange=populate;a.onchange=loadSelected;if(b)b.onchange=loadSelected;
 $('play').onclick=()=>{if(playing){stop();return;}if(elapsed>=duration)elapsed=0;playing=true;$('play').textContent='Pause';last=performance.now();raf=requestAnimationFrame(tick);};
 $('restart').onclick=()=>{stop();elapsed=0;draw();};$('timeline').oninput=()=>{stop();elapsed=Number($('timeline').value);draw();};$('encoding').onchange=draw;
 if(metric)$('target-fraction').onchange=()=>applyVariant();else $('view-mode').onchange=draw;
 (async()=>{try{catalog=metric?data.featured_attempts:await loadCatalog();if(!alive)return;const drills=[...new Set(catalog.map(t=>t.drill))].sort((x,y)=>Number(isMirror({drill:y}))-Number(isMirror({drill:x}))||x.localeCompare(y));drill.innerHTML=drills.map(d=>`<option value="${esc(d)}">${esc(drillLabel(d))}</option>`).join('');populate();}catch(e){error(e)}})();
 return ()=>{stop();alive=false;version++;};
}
