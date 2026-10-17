import {blockingDiagram} from './football-diagrams.js';
document.getElementById('field').innerHTML=blockingDiagram();
const figures=[
 ['metric_definition','Schematic definitions: Combine speed gain and supplied NFL crossing time answer different questions.'],
 ['measurement_review','Timing agreement on identical clips and target availability by cohort. A better-fitting diagnostic gate is not a verified definition.'],
 ['sensor_increment','Nested model errors and paired-player sensor-increment intervals.'],
 ['uncertainty_review','Original estimates under distinct uncertainty scopes. The shared-game row is an exploratory sensitivity.'],
 ['monitoring_population','Every later-evaluable monitoring player, separated by cohort and alignment.'],
 ['case_review','Two aggregate player profiles with game-bootstrap intervals. A persistent gap is a review question, not a technique diagnosis.']
];
const tabs=[...document.querySelectorAll('[data-figure]')];
function showFigure(i){
 const [name,caption]=figures[i],url=`figures/${name}.png`;
 const img=document.getElementById('research-figure');img.src=url;img.alt=`Figure ${i+1}. ${caption}`;img.removeAttribute('height');img.removeAttribute('width');
 for(const id of ['figure-link','figure-open'])document.getElementById(id).href=url;
 document.getElementById('figure-caption').textContent=`Figure ${i+1}. ${caption}`;
 document.getElementById('figure-panel').setAttribute('aria-labelledby',`fig-tab-${i}`);
 tabs.forEach((tab,j)=>{tab.setAttribute('aria-selected',String(i===j));tab.tabIndex=i===j?0:-1;});
}
tabs.forEach((tab,i)=>{tab.addEventListener('click',()=>showFigure(i));tab.addEventListener('keydown',e=>{let next;if(e.key==='ArrowRight')next=(i+1)%tabs.length;if(e.key==='ArrowLeft')next=(i+tabs.length-1)%tabs.length;if(e.key==='Home')next=0;if(e.key==='End')next=tabs.length-1;if(next!==undefined){e.preventDefault();showFigure(next);tabs[next].focus();}});});
const format=x=>x.toFixed(2),signed=x=>(x>0?'+':'')+format(x);
try{
 const response=await fetch('cohorts.json');if(!response.ok)throw Error('Cohort results unavailable');
 const cohorts=await response.json();
 if(cohorts.length!==2||cohorts.some(c=>!Number.isFinite(c.increment)||c.interval.length!==2||Object.values(c.mae).some(x=>!Number.isFinite(x))))throw Error('Invalid cohort report');
 const names={context:'Recorded context only',traditional:'+ Traditional Combine tests',sensor:'+ Sensor burst'};
 const max=Math.max(...cohorts.flatMap(c=>Object.values(c.mae)))*1.15;
 function render(year){const c=cohorts.find(c=>c.year===year);document.getElementById('cohort-note').textContent=`${year} evaluation · ${c.players} eligible rookies · the same players in all three models`;
 document.getElementById('model-bars').innerHTML=Object.entries(c.mae).map(([key,value])=>`<div class="bar-row"><div class="bar-label"><span>${names[key]}</span><b>${format(value)} ms</b></div><div class="bar-track"><div class="bar-fill" style="width:${value/max*100}%"></div></div></div>`).join('');
 document.getElementById('increment').innerHTML=`${signed(c.increment)} <small>ms</small>`;
 document.getElementById('increment-caption').textContent='Traditional-model error minus sensor-model error.';
 document.getElementById('interval').textContent=`Conditional 95% interval: ${signed(c.interval[0])} to ${signed(c.interval[1])} ms`;
 document.getElementById('model-table').innerHTML=`<table><caption>${year} model comparison</caption><thead><tr><th scope="col">Model</th><th scope="col">MAE (ms)</th></tr></thead><tbody>${Object.entries(c.mae).map(([k,v])=>`<tr><th scope="row">${names[k]}</th><td>${format(v)}</td></tr>`).join('')}</tbody></table>`;
 document.querySelectorAll('[data-year]').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.year)===year)));
 }
 document.querySelectorAll('[data-year]').forEach(b=>b.addEventListener('click',()=>render(Number(b.dataset.year))));render(2024);
}catch(error){document.getElementById('cohort-note').textContent='Interactive results could not load. The complete figures remain available below.';document.querySelectorAll('[data-year]').forEach(b=>b.disabled=true);}
