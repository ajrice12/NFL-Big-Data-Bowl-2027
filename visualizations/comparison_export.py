"""Actual-frame two-athlete GIF; positions are translated, never interpolated."""
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from src.load_data import ROOT

def main():
    d=json.loads((ROOT/'outputs/presentation/research.json').read_text())
    ts=[next(t for t in d['trajectories'] if t['nfl_id']==c['nfl_id'] and t['reversals']) for c in [d['cases'][0],d['cases'][2]]]
    # Use a local system font when available.
    try:font=ImageFont.truetype('arial.ttf',22);small=ImageFont.truetype('arial.ttf',16)
    except OSError:font=ImageFont.load_default(size=22);small=ImageFont.load_default(size=16)
    points=np.concatenate([np.array(t['frames'])[:,1:3]-np.array(t['frames'])[0,1:3] for t in ts]);low=points.min(axis=0);high=points.max(axis=0);scale=min(440/max(high[0]-low[0],1),280/max(high[1]-low[1],1));duration=max(t['frames'][-1][0]-t['frames'][0][0] for t in ts);frames=[]
    for elapsed in np.arange(0,duration+.05,.1):
        im=Image.new('RGB',(1200,520),'#08121e');draw=ImageDraw.Draw(im);draw.text((28,18),'THE 3-SECOND PROBLEM / RECORDED MIRROR COMPARISON',fill='#53e2e0',font=font)
        for side,t in enumerate(ts):
            fs=t['frames'];origin=fs[0];idx=max(i for i,f in enumerate(fs) if f[0]-origin[0]<=elapsed+1e-6);color=['#53e2e0','#f5bb71'][side];offset=side*600
            def p(f):return (int(offset+300+(f[1]-origin[1]-(low[0]+high[0])/2)*scale),int(260-(f[2]-origin[2]-(low[1]+high[1])/2)*scale))
            draw.text((offset+30,65),f"{t['name']} / G / {t['year']}",fill='white',font=font)
            for x in range(offset+40,offset+570,60):draw.line([(x,110),(x,420)],fill='#243445')
            for y in range(110,421,60):draw.line([(offset+40,y),(offset+570,y)],fill='#243445')
            vmax=max(f[3] for f in fs)
            for j in range(1,idx+1):
                if fs[j][7]!=fs[j-1][7]:continue
                ratio=fs[j][3]/max(vmax,.1);rgb=(int(83+162*ratio),int(226-39*ratio),int(224-111*ratio));draw.line([p(fs[j-1]),p(fs[j])],fill=rgb,width=4)
            for ri,r in enumerate(t['reversals']):
                if r['index']>idx:continue
                x,y=p(fs[r['index']]);draw.polygon([(x,y-8),(x+8,y),(x,y+8),(x-8,y)],outline=color);draw.text((x+10,y-20),f'R{ri+1}',fill=color,font=small)
            x,y=p(fs[idx]);draw.ellipse((x-8,y-8,x+8,y+8),fill=color);f=fs[idx];acc='—' if f[4] is None else f'{f[4]:.2f}';draw.text((offset+30,440),f"t={f[0]-origin[0]:.2f}s  frame={idx+1}/{len(fs)}  speed={f[3]:.2f} units/s",fill='white',font=small);draw.text((offset+30,467),f"Δspeed/Δt={acc} units/s²   median reset={t['summary']['recovery_delay']:.2f}s",fill=color,font=small)
        draw.text((28,496),'Source coordinates translated to common origin / shared scale / 10 fps / no interpolation',fill='#a4b4c6',font=small);frames.append(im)
    dest=ROOT/'outputs/animations';dest.mkdir(parents=True,exist_ok=True);frames[0].save(dest/'mirror_comparison.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=False)
    print(f'Wrote comparison GIF: {len(frames)} frames at 10 fps.')
if __name__=='__main__':main()
