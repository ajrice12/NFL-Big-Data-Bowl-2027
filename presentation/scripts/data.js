import {namePortrait} from './portraits.js';
export const esc = value => String(value ?? '—').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const fmt = (x,n=2) => Number.isFinite(x) ? x.toLocaleString('en-US',{maximumFractionDigits:n,minimumFractionDigits:n}) : '—';
export const count = x => Number.isFinite(Number(x)) ? Number(x).toLocaleString('en-US') : '—';
export const pct = x => Number.isFinite(x) ? `${fmt(x*100,1)}%` : '—';
export function stat(value,label){return `<div class="stat"><b>${value}</b><span>${label}</span></div>`;}
export function table(rows,keys){return `<div class="table-wrap"><table><thead><tr>${keys.map(k=>`<th>${esc(k.replaceAll('_',' '))}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${keys.map(k=>`<td>${k==='player'||k==='display_name'?`<span class="table-player">${namePortrait(r[k])}${esc(r[k])}</span>`:esc(r[k])}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;}
async function json(file){const response=await fetch(`../outputs/presentation/${file}`,{cache:'no-store'});if(!response.ok)throw Error(`${file}: HTTP ${response.status}`);return response.json();}
export async function loadResearch(){const d=await json('briefing.json');if(d.schema_version!==2||!d.featured_attempts?.length)throw Error('Analysis incomplete: rebuild the presentation export');return d;}
let catalog,appendix;
export async function loadCatalog(){catalog??=json('catalog.json').catch(e=>{catalog=null;throw e});return catalog;}
export async function loadAppendix(){appendix??=json('appendix.json').catch(e=>{appendix=null;throw e});return appendix;}
const attempts=new Map();
export async function loadTrajectory(meta){
 if(!attempts.has(meta.id)) attempts.set(meta.id,json(meta.file).then(t=>{
  if(t.id!==meta.id||t.nfl_id!==meta.nfl_id||!t.frames?.length)throw Error('Selected trajectory identity or frames are invalid');return t;
 }).catch(e=>{attempts.delete(meta.id);throw e}));
 return attempts.get(meta.id);
}
