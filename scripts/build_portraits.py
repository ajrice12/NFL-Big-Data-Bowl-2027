"""Cache rookie-season roster portraits locally; never substitute another season."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlsplit
import hashlib
import io
import json
import re
import unicodedata
import pandas as pd
from PIL import Image
from src.load_data import ROOT, PROCESSED


def main():
    destination=ROOT/'outputs/presentation'
    sources=destination/'portrait-sources';sources.mkdir(parents=True,exist_ok=True)
    images=destination/'portraits';images.mkdir(exist_ok=True)
    players=pd.read_parquet(PROCESSED/'players.parquet')
    records=[]
    for year in sorted(players.draft_year.dropna().astype(int).unique()):
        year=int(year)
        url=f'https://github.com/nflverse/nflverse-data/releases/download/rosters/roster_{year}.csv'
        cached=sources/f'roster_{year}.csv'
        if not cached.exists():cached.write_bytes(urlopen(url,timeout=30).read())
        roster=pd.read_csv(cached,low_memory=False)
        for _,player in players.loc[players.draft_year.eq(year)].iterrows():
            ident=int(player.nfl_id)
            match=roster.loc[roster.gsis_it_id.eq(ident)&roster.season.eq(year)]
            record={'nfl_id':ident,'name':player.display_name,'season':year,'roster_source':url,
                    'capture_date_verified':False,'status':'unavailable','image':None}
            # Require the numeric tracking ID. A DOB discrepancy can be resolved
            # for display identity only when the full normalized names also agree.
            if len(match):
                birthdays=match.birth_date.dropna().astype(str).unique()
                local=pd.to_datetime(player.birth_date).date().isoformat() if pd.notna(player.birth_date) else None
                urls=match.headshot_url.dropna().unique().tolist()
                normalize=lambda text: re.sub(r'[^a-z0-9]','',re.sub(r'\s+(jr\.?|sr\.?|ii|iii|iv)$','',unicodedata.normalize('NFKD',str(text)).encode('ascii','ignore').decode().lower()))
                same_name=normalize(player.display_name)==normalize(match.iloc[0].full_name)
                birthday_conflict=local and len(birthdays) and local not in birthdays
                if birthday_conflict and not same_name:
                    record['reason']='Identity birthday mismatch'
                elif len(urls)==1 and urlsplit(urls[0]).hostname in ['static.www.nfl.com','static.clubs.nfl.com','a.espncdn.com']:
                    record.update(source_url=urls[0],roster_name=match.iloc[0].full_name,
                                  team=match.iloc[0].team,status='pending')
                    if birthday_conflict:record['identity_note']='Exact tracking ID and normalized full-name match; source birthdays differ. Scientific player metadata unchanged.'
                else:record['reason']='No unique season headshot URL'
            else:record['reason']='No matching season roster ID'
            records.append(record)

    def download(record):
        if record['status']!='pending':return record
        filename=f"{record['nfl_id']}-{record['season']}.webp"
        target=images/filename
        try:
            if not target.exists():
                req=Request(record['source_url'],headers={'User-Agent':'NFLResearchLocalPreview/1.0'})
                raw=urlopen(req,timeout=20).read()
                picture=Image.open(io.BytesIO(raw)).convert('RGBA')
                picture.thumbnail((240,240))
                picture.save(target,'WEBP',quality=88)
            with Image.open(target) as picture:
                if min(picture.size)<40:raise ValueError('Portrait too small')
            record.update(image='portraits/'+filename,status='available',sha256=hashlib.sha256(target.read_bytes()).hexdigest())
        except Exception as error:
            record.update(status='unavailable',reason=f'Portrait retrieval failed: {error}')
        return record

    with ThreadPoolExecutor(max_workers=8) as pool:records=list(pool.map(download,records))
    result={'retrieved_at':datetime.now(timezone.utc).isoformat(),'policy':'Season roster association; capture date unverified. No other-season substitution.',
            'available':sum(r['status']=='available' for r in records),'total':len(records),'players':records}
    (destination/'portraits.json').write_text(json.dumps(result,separators=(',',':')),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='players'},indent=2))


if __name__=='__main__':main()
