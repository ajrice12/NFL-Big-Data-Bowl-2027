export const esc = value => String(value ?? '—').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const fmt = (x,n=2) => Number.isFinite(x) ? x.toLocaleString('en-US',{maximumFractionDigits:n,minimumFractionDigits:n}) : '—';
export const count = x => Number(x).toLocaleString('en-US');
export const pct = x => `${fmt(x*100,2)}%`;
export function stat(value,label){return `<div class="stat"><b>${value}</b><span>${label}</span></div>`;}
export function table(rows,keys){return `<div class="table-wrap"><table><thead><tr>${keys.map(k=>`<th>${esc(k.replaceAll('_',' '))}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${keys.map(k=>`<td>${esc(r[k])}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;}
export async function loadResearch(){const r=await fetch('../outputs/presentation/research.json',{cache:'no-store'});if(!r.ok)throw Error(`Research export returned HTTP ${r.status}`);const d=await r.json();if(d.schema_version!==1||!d.trajectories?.length||!d.ol?.models)throw Error('Analysis incomplete: export schema or model results missing');return d;}
