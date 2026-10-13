/* Actual Combine traces on a practice board; illustrative grid/equipment only. */
export const ATHLETE_COLORS=['#ffffff','#f2c94c'];
export function geometry(tracks,width=1200,height=580){
 const points=tracks.flatMap(t=>t.frames.map(f=>[f[1]-t.frames[0][1],f[2]-t.frames[0][2]]));
 const xs=points.map(p=>p[0]),ys=points.map(p=>p[1]);
 const minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys);
 const scale=Math.min((width-330)/Math.max(maxX-minX,4),(height-220)/Math.max(maxY-minY,3));
 return {scale,point:(t,f)=>[width/2+(f[1]-t.frames[0][1]-(minX+maxX)/2)*scale,height/2-(f[2]-t.frames[0][2]-(minY+maxY)/2)*scale]};
}
export function observedFrame(track,elapsed){
 const fs=track.frames,t0=fs[0][0];let index=0;
 while(index+1<fs.length&&fs[index+1][0]-t0<=elapsed+1e-7)index++;
 return index;
}
function field(ctx,w,h){
 ctx.fillStyle='#173b2f';ctx.fillRect(0,0,w,h);
 ctx.fillStyle='#1e4435';ctx.fillRect(35,40,w-70,h-80);
 ctx.strokeStyle='#dce8df22';ctx.lineWidth=1;
 for(let x=70;x<w-35;x+=55){ctx.beginPath();ctx.moveTo(x,60);ctx.lineTo(x,h-60);ctx.stroke();}
 for(let y=65;y<h-40;y+=55){ctx.beginPath();ctx.moveTo(55,y);ctx.lineTo(w-55,y);ctx.stroke();}
 ctx.strokeStyle='#dce8df77';ctx.lineWidth=2;ctx.strokeRect(35,40,w-70,h-80);
 // Equipment symbols indicate a practice setting, not surveyed cone locations.
 [[65,75],[w-65,75],[65,h-75],[w-65,h-75]].forEach(([x,y])=>{ctx.fillStyle='#ed8a45';ctx.beginPath();ctx.moveTo(x,y-12);ctx.lineTo(x+11,y+8);ctx.lineTo(x-11,y+8);ctx.closePath();ctx.fill();ctx.fillRect(x-14,y+8,28,3);});
 ctx.fillStyle='#e8efea';ctx.font='bold 18px Arial';ctx.textAlign='left';ctx.fillText('COMBINE / PRACTICE DRILL DIAGRAM',38,25);
 ctx.font='13px Arial';ctx.fillStyle='#b8cdbf';ctx.textAlign='right';ctx.fillText('GRID & CONES ILLUSTRATIVE / NOT MEASURED PLACEMENT',w-40,25);ctx.textAlign='left';
}
export function drawField(canvas,tracks,elapsed,{ghost=false,encoding='athlete',focus=false,only=null}={}){
 const ctx=canvas.getContext('2d'),w=canvas.width,h=canvas.height;field(ctx,w,h);
 if(!tracks.length)return;
 const g=geometry(tracks,w,h),point=g.point;
 const maxSpeed=Math.max(.1,...tracks.flatMap(t=>t.frames.map(f=>f[3]||0))),maxAcc=Math.max(.1,...tracks.flatMap(t=>t.frames.map(f=>Math.abs(f[4]||0))));
 tracks.forEach((t,ath)=>{
  if(only!==null&&ath!==only)return;
  const fs=t.frames,idx=observedFrame(t,elapsed),f=fs[idx],color=ATHLETE_COLORS[ath%2];
  if(ghost){ctx.strokeStyle=ath?'#b7a35466':'#dce6db66';ctx.lineWidth=2;ctx.setLineDash([5,6]);ctx.beginPath();fs.forEach((row,j)=>{const p=point(t,row);if(!j||row[7]!==fs[j-1][7])ctx.moveTo(...p);else ctx.lineTo(...p)});ctx.stroke();ctx.setLineDash([]);}
  for(let j=1;j<=idx;j++){
   if(fs[j][7]!==fs[j-1][7])continue;
   let stroke=color;
   if(encoding==='speed'){const v=fs[j][3]/maxSpeed;stroke=`rgb(${Math.round(240+2*v)},${Math.round(240-39*v)},${Math.round(240-164*v)})`;}
   if(encoding==='acceleration'){const v=(fs[j][4]||0)/maxAcc;stroke=v<0?`rgb(${Math.round(240+110*v)},${Math.round(240+70*v)},240)`:`rgb(242,${Math.round(240-39*v)},${Math.round(240-164*v)})`;}
   ctx.strokeStyle='#091c18';ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(...point(t,fs[j-1]));ctx.lineTo(...point(t,fs[j]));ctx.stroke();ctx.strokeStyle=stroke;ctx.lineWidth=4;ctx.stroke();
  }
  let recent=t.reversals.filter(r=>r.index<=idx).at(-1);
  t.reversals.filter(r=>r.index<=idx).forEach((r,i)=>{
   const [x,y]=point(t,fs[r.index]);ctx.strokeStyle=color;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x,y-7);ctx.lineTo(x+7,y);ctx.lineTo(x,y+7);ctx.lineTo(x-7,y);ctx.closePath();ctx.stroke();
   if(focus){ctx.font='bold 17px Arial';ctx.fillStyle=color;ctx.fillText(`R${i+1}`,x+11,y-10);}
   if(r.completed&&r.recovery_index<=idx){const p=point(t,fs[r.recovery_index]);ctx.beginPath();ctx.arc(...p,6,0,Math.PI*2);ctx.stroke();}
  });
  if(recent&&(focus||elapsed-recent.time<.65)){
   const [rx,ry]=point(t,fs[recent.index]);ctx.strokeStyle='#f2c94c';ctx.lineWidth=3;ctx.beginPath();ctx.arc(rx,ry,25,0,Math.PI*2);ctx.stroke();
   if(focus){const axis=[t.summary.axis_x,t.summary.axis_y],r=recent,original=fs[r.index];const target=[...original];target[1]+=axis[0]*r.direction*r.target_displacement;target[2]+=axis[1]*r.direction*r.target_displacement;const [x,y]=point(t,target),vx=axis[1]*18,vy=axis[0]*18;ctx.setLineDash([5,4]);ctx.beginPath();ctx.moveTo(x-vx,y-vy);ctx.lineTo(x+vx,y+vy);ctx.stroke();ctx.setLineDash([]);ctx.font='bold 15px Arial';ctx.fillStyle='#f2c94c';ctx.fillText('RESET TARGET',x+23,y+43);}
  }
  const [x,y]=point(t,f);ctx.fillStyle='#092219';ctx.beginPath();ctx.ellipse(x,y+10,16,6,0,0,Math.PI*2);ctx.fill();ctx.fillStyle=color;ctx.beginPath();ctx.arc(x,y,12,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#101b17';ctx.lineWidth=2;ctx.stroke();ctx.fillStyle='#101b17';ctx.textAlign='center';ctx.font='bold 13px Arial';ctx.fillText(ath?'B':'A',x,y+4);ctx.textAlign='left';
  const name=t.name.split(' ').at(-1).toUpperCase(),label=`${name}  ${t.position}`;ctx.font='bold 16px Arial';const tw=ctx.measureText(label).width+18,ly=y+(ath?39:-27),lx=Math.min(w-120-tw,Math.max(115,ath?x-tw-22:x+22));ctx.fillStyle='#101a17';ctx.fillRect(lx,ly-18,tw,25);ctx.fillStyle=color;ctx.fillText(label,lx+8,ly);
 });
 const units=Math.max(.5,Math.floor(110/g.scale*2)/2);ctx.strokeStyle='#e5ece0';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(135,h-55);ctx.lineTo(135+units*g.scale,h-55);ctx.stroke();ctx.font='14px Arial';ctx.fillStyle='#edf1e9';ctx.fillText(`${units} source units · shared scale`,135,h-42);ctx.textAlign='right';ctx.fillText(`ELAPSED ${elapsed.toFixed(2)} s · NO FRAME INTERPOLATION`,w-130,h-12);ctx.textAlign='left';
}
export function drawSeries(canvas,tracks,elapsed,duration){
 const ctx=canvas.getContext('2d'),w=canvas.width,h=canvas.height;ctx.fillStyle='#10191b';ctx.fillRect(0,0,w,h);
 const max=Math.max(.1,...tracks.flatMap(t=>t.frames.map(f=>f[3]||0))),x=t=>52+t/duration*(w-75),y=s=>h-25-s/max*(h-58);
 ctx.strokeStyle='#44504d';ctx.beginPath();ctx.moveTo(52,27);ctx.lineTo(52,h-25);ctx.lineTo(w-23,h-25);ctx.stroke();
 ctx.font='14px Arial';ctx.fillStyle='#aebdb4';ctx.fillText(`SPEED / REPORTED UNITS`,54,17);ctx.fillText(max.toFixed(1),10,40);ctx.fillText('0',25,h-22);ctx.fillText('0 s',52,h-6);ctx.fillText(`${duration.toFixed(1)} s`,w-62,h-6);
 tracks.forEach((t,i)=>{ctx.strokeStyle=ATHLETE_COLORS[i%2];ctx.lineWidth=2;ctx.beginPath();t.frames.forEach((f,j)=>{const p=[x(f[0]-t.frames[0][0]),y(f[3])];if(!j||f[7]!==t.frames[j-1][7])ctx.moveTo(...p);else ctx.lineTo(...p)});ctx.stroke()});
 ctx.strokeStyle='#ffffff';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(x(elapsed),27);ctx.lineTo(x(elapsed),h-25);ctx.stroke();
}
