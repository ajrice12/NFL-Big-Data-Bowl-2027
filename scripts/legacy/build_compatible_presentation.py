import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

base = Path(r'C:\Users\shann_o\.codex\visualizations\2026\10\12\01a1327c-2a89-76b0-8274-7156f4482ccc')
data = json.loads(Path('.venv/nfl-vis-data.json').read_text())

def tag(name, attrs=None, text=None, parent=None):
    e = ET.Element(name, attrs or {}) if parent is None else ET.SubElement(parent, name, attrs or {})
    if text is not None:
        e.text = str(text)
    return e

def markup(e):
    return ET.tostring(e,encoding='unicode',method='html')

def options(names, selected=0):
    result = []
    for i, name in enumerate(names):
        attrs = {'value':str(i)}
        if i == selected:
            attrs['selected']=''
        result.append(markup(tag('option',attrs,name)))
    return ''.join(result)

tracks, charts = [], []
for i, trajectory in enumerate(data['trajectories']):
    frames = trajectory['frames']
    xmin,xmax = min(f[1] for f in frames),max(f[1] for f in frames)
    ymin,ymax = min(f[2] for f in frames),max(f[2] for f in frames)
    scale = min(680/max(xmax-xmin,1),310/max(ymax-ymin,1))
    cx,cy=(xmin+xmax)/2,(ymin+ymax)/2
    points=[(round(368+(f[1]-cx)*scale,3),round(175-(f[2]-cy)*scale,3)) for f in frames]
    attrs={'id':f'nfl-track-{i}','class':'nfl-frame'}
    if i:
        attrs['hidden']=''
    group=tag('div',attrs)
    svg=tag('svg',{'class':'nfl-map','viewBox':'0 0 736 350','role':'img','aria-label':trajectory['label']},parent=group)
    tag('title',text=trajectory['label'],parent=svg)
    path=' '.join(('M' if j==0 else 'L')+f'{x},{y}' for j,(x,y) in enumerate(points))
    tag('path',{'d':path,'fill':'none','stroke':'var(--muted-foreground)','stroke-width':'2','vector-effect':'non-scaling-stroke'},parent=svg)
    x0,y0=points[0]
    tag('rect',{'x':str(x0-5),'y':str(y0-5),'width':'10','height':'10','fill':'var(--foreground)'},parent=svg)
    tag('circle',{'id':f'nfl-dot-{i}','cx':str(x0),'cy':str(y0),'r':'8','fill':'var(--viz-series-1)'},parent=svg)
    labels=tag('div',{'class':'nfl-axis text-small'},parent=group)
    tag('span',text=f'x: {xmin:.1f} to {xmax:.1f}',parent=labels)
    tag('span',text=f'y: {ymin:.1f} to {ymax:.1f}',parent=labels)
    charts.append(markup(group))
    tracks.append({'detail':trajectory['detail'],'frames':[f+[x,y] for f,(x,y) in zip(frames,points)]})

names=list(data['tables'])
selected_table=names.index('combine_tracking.csv')
tables=[]
for i,(name,sample) in enumerate(data['tables'].items()):
    attrs={'id':f'nfl-table-{i}','class':'nfl-table'}
    if i!=selected_table:
        attrs['hidden']=''
    group=tag('div',attrs)
    tag('div',{'class':'nfl-readout'},f'{data["manifest"][name]["rows"]:,} rows · {sample["totalColumns"]} columns',group)
    wrap=tag('div',{'class':'table-responsive'},parent=group)
    table=tag('table',{'class':'table table-sm'},parent=wrap)
    thead=tag('thead',parent=table)
    row=tag('tr',parent=thead)
    for column in sample['columns']:
        tag('th',text=column,parent=row)
    tbody=tag('tbody',parent=table)
    for values in sample['rows']:
        row=tag('tr',parent=tbody)
        for value in values:
            tag('td',text='—' if value is None else value,parent=row)
    tables.append(markup(group))

models=[]
for label,key in [('Training-mean benchmark','train_mean'),('Traditional Combine tests','traditional'),('Traditional tests + tracking','traditional_plus_tracking')]:
    model=data['results']['models'][key]
    row=tag('tr')
    tag('td',text=label,parent=row)
    tag('td',{'class':'text-end'},f'{model["mae"]:.3f}',row)
    tag('td',{'class':'text-end'},f'{model["r2"]:.3f}' if 'r2' in model else '—',row)
    models.append(markup(row))
first=tracks[0]['frames'][0]
values=f'Frame 1 / {len(tracks[0]["frames"])} · 0.0 seconds · x {first[1]:.2f} · y {first[2]:.2f} · speed {first[3]:.2f} (source units)'
replacements={
    '__OPTIONS__':options([t['label'] for t in data['trajectories']]),
    '__FIRST_DESCRIPTION__':html.escape(tracks[0]['detail']),
    '__FIRST_MAX__':str(len(tracks[0]['frames'])-1),
    '__FIRST_VALUES__':values,
    '__TRACKS__':''.join(charts),
    '__TABLE_OPTIONS__':options(names,selected_table),
    '__TABLES__':''.join(tables),
    '__MODELS__':''.join(models),
    '__TRACK_DATA__':json.dumps(tracks,separators=(',',':')).replace('<','\\u003c'),
}
result=(base/'nfl-data-compatible-template.html').read_text(encoding='utf-8')
for key,value in replacements.items():
    result=result.replace(key,value)
assert not re.search(r'__[A-Z_]+__',result)
assert len(result.encode('utf-8'))<1_000_000
(base/'nfl-data-presentation.html').write_text(result,encoding='utf-8')
print('Rebuilt presentation:',len(result.encode('utf-8')),'bytes; data and charts render before JavaScript runs.')
