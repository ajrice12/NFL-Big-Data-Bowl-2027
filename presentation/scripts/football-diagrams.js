/* Concept illustrations only. These positions are not measured game tracking. */
export function blockingDiagram(state='setup'){
 const pressure=state==='pressure',early=state==='early';
 return `<svg class="blocking-diagram" viewBox="0 0 660 390" role="img" aria-label="Illustrative pass protection: offensive line between a pass rusher and quarterback. ${pressure?'Pressure reaches the quarterback.':early?'The quarterback releases before the checkpoint.':'A blocker reacts to a rusher changing direction.'}">
 <defs><marker id="route-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="none" stroke="#e42a43" stroke-width="1.5"/></marker></defs>
 <rect width="660" height="390" fill="#14372d"/>
 ${[70,170,270,370,470,570].map(x=>`<path d="M${x} 25V365" stroke="#ffffff24"/>`).join('')}
 <path d="M70 148H590" stroke="#60aaff" stroke-width="2" stroke-dasharray="7 7"/>
 <text x="85" y="132" fill="#acd2ff" font-size="12" font-family="Inter,Arial">LINE OF SCRIMMAGE / ILLUSTRATION</text>
 <path d="M200 193Q198 307 330 322Q455 306 460 193" fill="none" stroke="#ffffff50" stroke-width="2" stroke-dasharray="5 6"/>
 ${[205,267,330,393,455].map((x,i)=>`<circle cx="${x}" cy="185" r="21" fill="${i===4?'#ffffff':'#bdc9d8'}"/><text x="${x}" y="190" text-anchor="middle" fill="#101c30" font-size="13" font-family="Oswald,Arial">${i===4?'T':'OL'}</text>`).join('')}
 <circle cx="330" cy="278" r="23" fill="#fff"/><text x="330" y="284" text-anchor="middle" fill="#101c30" font-size="16" font-family="Oswald,Arial">QB</text>
 <path d="M489 82l20 20m-20 0l20-20" stroke="#ff425b" stroke-width="5"/>
 <path d="${pressure?'M499 111Q535 165 485 225Q421 270 362 278':'M499 111Q525 151 487 162L459 155'}" fill="none" stroke="#ff425b" stroke-width="4" marker-end="url(#route-arrow)"/>
 ${pressure?'<circle cx="330" cy="278" r="37" fill="none" stroke="#ff425b" stroke-width="3"/>':''}
 ${early?'<path d="M330 251L290 75" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="6 5"/><text x="220" y="62" fill="#fff" font-size="14" font-family="Oswald,Arial">EARLY RELEASE</text>':''}
 <text x="525" y="89" fill="#ff6a7e" font-size="15" font-family="Oswald,Arial">RUSHER</text>
 <text x="469" y="205" fill="#fff" font-size="14" font-family="Oswald,Arial">RECOVER</text>
 <text x="330" y="349" text-anchor="middle" fill="#d5dfdf" font-size="14" font-family="Inter,Arial">${pressure?'Pressure arrives by the checkpoint':early?'The observation ends before three seconds':state==='clean'?'Clean through 3 s; pressure can still arrive later':'Stay between the rush and the quarterback'}</text>
 </svg>`;
}
export function observationTimeline(type){
 const pressure=type==='pressure',early=type==='early',end=early?166:pressure?218:330;
 return `<svg viewBox="0 0 360 78" role="img" aria-label="Illustrative timeline: ${early?'pressure-free observation ends before three seconds':pressure?'pressure occurs by three seconds':'observation stays clean through three seconds; pressure can occur later'}">
 <path d="M20 36H340" stroke="#41536c" stroke-width="4"/>
 <path d="M20 36H${end}" stroke="${pressure?'#ff425b':early?'#a7b4c8':'#57b1ff'}" stroke-width="6"/>
 <path d="M270 12V56" stroke="#fff" stroke-dasharray="4 4"/>
 <circle cx="${end}" cy="36" r="7" fill="${pressure?'#ff425b':early?'#a7b4c8':'#57b1ff'}"/>
 <text x="20" y="70" fill="#b9c8da" font-size="12" font-family="Inter,Arial">SNAP</text><text x="270" y="70" text-anchor="middle" fill="#fff" font-size="12" font-family="Inter,Arial">3 s</text>
 <text x="${early?110:pressure?160:294}" y="17" fill="#fff" font-size="11" font-family="Inter,Arial">${early?'END':pressure?'PRESSURE':'OBSERVED'}</text>
 </svg>`;
}
