import {esc} from './data.js';
const records=new Map(),bitmaps=new Map();
export async function loadPortraits(){
 try{const r=await fetch('../outputs/presentation/portraits.json');if(!r.ok)return;const d=await r.json();d.players.forEach(p=>records.set(`${p.nfl_id}-${p.season}`,p));}catch{/* Portraits are optional; research remains usable offline. */}
}
export function portraitRecord(id,year){return records.get(`${Number(id)}-${Number(year)}`);}
export function portraitMarkup(id,year,name){
 const p=portraitRecord(id,year),label=p?.status==='available'?`${year} season roster portrait of ${name}; photo capture date unverified`:`${year} season portrait unavailable for ${name}`;
 return `<span class="portrait" title="${esc(label)}" data-player-id="${Number(id)}" data-season="${Number(year)}">${p?.image?`<img src="../outputs/presentation/${esc(p.image)}" alt="${esc(label)}" loading="lazy" decoding="async" onerror="this.hidden=true;this.parentElement.classList.add('missing')"><span class="portrait-fallback" aria-hidden="true">${esc(name.split(' ').map(s=>s[0]).slice(0,2).join(''))}</span>`:`<span class="portrait-fallback">${esc(name.split(' ').map(s=>s[0]).slice(0,2).join(''))}</span>`}<small>${p?.image?year:'NO PHOTO'}</small></span>`;
}
export async function preloadPortraits(tracks){
 await Promise.all(tracks.map(async t=>{const p=portraitRecord(t.nfl_id,t.year);if(!p?.image)return;const key=`${t.nfl_id}-${t.year}`;if(bitmaps.has(key))return;const image=new Image();image.src='../outputs/presentation/'+p.image;try{await image.decode();bitmaps.set(key,image);}catch{/* Keep the explicit unavailable portrait fallback. */}}));
}
export function canvasPortrait(id,year){return bitmaps.get(`${Number(id)}-${Number(year)}`);}
export function namePortrait(name){const matches=[...records.values()].filter(p=>p.name===name);return matches.length===1?portraitMarkup(matches[0].nfl_id,matches[0].season,name):'';}
// Preserve decoded image nodes while live statistics update every frame.
export function renderWithPortraits(element,html){
 const previous=new Map();element.querySelectorAll('.portrait').forEach(node=>{const key=node.dataset.playerId+'-'+node.dataset.season;if(!previous.has(key))previous.set(key,[]);previous.get(key).push(node);});
 element.innerHTML=html;element.querySelectorAll('.portrait').forEach(node=>{const old=previous.get(node.dataset.playerId+'-'+node.dataset.season)?.shift();if(old)node.replaceWith(old);});
}
