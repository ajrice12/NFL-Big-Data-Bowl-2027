import json
import xml.etree.ElementTree as ET
from pathlib import Path

base=Path(r'C:\Users\shann_o\.codex\visualizations\2026\10\12\01a1327c-2a89-76b0-8274-7156f4482ccc')
data=json.loads(Path('.venv/nfl-vis-data.json').read_text())

def add(parent,name,attrs=None,text=None):
    e=ET.SubElement(parent,name,attrs or {})
    if text is not None:e.text=str(text)
    return e

def serialize(e):return ET.tostring(e,encoding='unicode',method='html')

styles=[]
examples=[]
for i,t in enumerate(data['trajectories']):
    frames=t['frames']
    xmin,xmax=min(f[1] for f in frames),max(f[1] for f in frames)
    ymin,ymax=min(f[2] for f in frames),max(f[2] for f in frames)
    scale=min(680/max(xmax-xmin,1),310/max(ymax-ymin,1))
    mx,my=(xmin+xmax)/2,(ymin+ymax)/2
    points=[(round(368+(f[1]-mx)*scale,2),round(175-(f[2]-my)*scale,2)) for f in frames]
    duration=frames[-1][0]-frames[0][0]
    keyframes=[]
    for frame,(x,y) in zip(frames,points):
        percent=(frame[0]-frames[0][0])/duration*100
        keyframes.append(f'{percent:.4f}%{{transform:translate({x}px,{y}px)}}')
    styles.append(f'@keyframes nfl-track-{i}'+'{'+''.join(keyframes)+'}')
    styles.append(f'#nfl-live-analysis #nfl-example-{i}[open] .nfl-dot{{animation:nfl-track-{i} {duration:.3f}s linear 1 both paused;}}')
    styles.append(f'#nfl-live-analysis #nfl-play-{i}:checked ~ svg .nfl-dot{{animation-play-state:running;}}')
    attrs={'id':f'nfl-example-{i}','class':'nfl-example'}
    if i==0:attrs['open']=''
    item=ET.Element('details',attrs)
    add(item,'summary',text=t['label'])
    add(item,'div',{'class':'nfl-description text-small'},t['detail'])
    add(item,'input',{'id':f'nfl-play-{i}','type':'checkbox','class':'form-check-input'})
    add(item,'label',{'for':f'nfl-play-{i}','class':'form-label'},'Play / pause animation')
    svg=add(item,'svg',{'viewBox':'0 0 736 350','class':'nfl-map','role':'img','aria-label':t['label']+' recorded trajectory'})
    add(svg,'title',text=t['label'])
    add(svg,'path',{'class':'nfl-path','d':' '.join(('M' if j==0 else 'L')+f'{x},{y}' for j,(x,y) in enumerate(points))})
    x0,y0=points[0]
    add(svg,'rect',{'class':'nfl-start','x':str(x0-5),'y':str(y0-5),'width':'10','height':'10'})
    add(svg,'circle',{'class':'nfl-dot','cx':'0','cy':'0','r':'8','style':f'transform:translate({x0}px,{y0}px)'})
    axis=add(item,'div',{'class':'nfl-axis text-small'})
    add(axis,'span',text=f'x: {xmin:.1f} to {xmax:.1f}')
    add(axis,'span',text=f'y: {ymin:.1f} to {ymax:.1f}')
    add(axis,'span',text=f'{len(frames)} frames · {duration:.1f} seconds')
    examples.append(serialize(item))

tables=[]
for name,sample in data['tables'].items():
    item=ET.Element('details',{'class':'nfl-example'})
    add(item,'summary',text=f'{name} · {data["manifest"][name]["rows"]:,} rows')
    wrap=add(item,'div',{'class':'table-responsive'})
    table=add(wrap,'table',{'class':'table table-sm'})
    row=add(add(table,'thead'),'tr')
    for col in sample['columns']:add(row,'th',text=col)
    body=add(table,'tbody')
    for values in sample['rows']:
        row=add(body,'tr')
        for value in values:add(row,'td',text='—' if value is None else value)
    tables.append(serialize(item))

models=[]
for label,key in [('Training-mean benchmark','train_mean'),('Traditional Combine tests','traditional'),('Traditional tests + tracking','traditional_plus_tracking')]:
    model=data['results']['models'][key]
    row=ET.Element('tr')
    add(row,'td',text=label)
    add(row,'td',{'class':'text-end'},f'{model["mae"]:.3f}')
    add(row,'td',{'class':'text-end'},f'{model["r2"]:.3f}' if 'r2' in model else '—')
    models.append(serialize(row))
result=(base/'nfl-native-template.html').read_text(encoding='utf-8')
for key,value in {'__ANIMATION_STYLES__':'\n'.join(styles),'__NATIVE_TRAJECTORIES__':'\n'.join(examples),'__NATIVE_TABLES__':'\n'.join(tables),'__MODELS__':''.join(models)}.items():
    result=result.replace(key,value)
assert '<script' not in result
assert '__NATIVE_' not in result
assert len(result.encode())<1_000_000
(base/'nfl-data-presentation.html').write_text(result,encoding='utf-8')
print('Native animation presentation:',len(result.encode()),'bytes; zero executable scripts.')
