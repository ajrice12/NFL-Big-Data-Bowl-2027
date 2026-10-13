const fs=require('node:fs'),path=require('node:path');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE_PATH||'playwright');
const root=path.resolve(__dirname,'..'),out=path.join(root,'outputs/verification/portraits');fs.mkdirSync(out,{recursive:true});
const base='http://127.0.0.1:8765/presentation/';
(async()=>{
 const browser=await chromium.launch({executablePath:'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:900}}),checks=[],errors=[],failed=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)failed.push(r.url())});
 const check=(ok,label)=>{if(!ok)throw Error(label);checks.push(label);};
 const go=async id=>{await page.goto(base+'#'+id);await page.locator(`[data-section="${id}"]`).waitFor();};
 const ready=async id=>page.waitForFunction(id=>!document.getElementById(id).disabled,id);
 const photoReady=async selector=>page.waitForFunction(selector=>[...document.querySelectorAll(selector)].every(i=>i.complete&&i.naturalWidth>40),selector);
 const shot=async name=>page.screenshot({path:path.join(out,name),fullPage:true,animations:'disabled'});
 try{
  await go('overview');await photoReady('.matchup .portrait img');check(await page.locator('.matchup .portrait img').count()===2,'Both overview player names have decoded season portraits');
  check(await page.locator('.matchup [data-player-id="55924"]').getAttribute('data-season')==='2023','Torrence uses 2023 portrait, not a current photo');await shot('overview-1440.png');
  await go('film');await ready('story-play');await page.locator('#story-play').click();await photoReady('#story-lower img');
  await page.locator('#story-timeline').fill('2.4');await page.locator('#story-timeline').dispatchEvent('input');check((await page.locator('#story-large-time').textContent()).includes('2.40'),'Large guided timer matches scrubbed actual elapsed time');
  check(await page.locator('#story-large-time').evaluate(e=>parseFloat(getComputedStyle(e).fontSize)>=40),'Guided clock has prominent broadcast-size digits');
  await page.evaluate(()=>window.portraitUnderTest=document.querySelector('#story-lower img'));await page.locator('#story-play').click();await page.waitForTimeout(250);await page.locator('#story-play').click();check(await page.evaluate(()=>window.portraitUnderTest===document.querySelector('#story-lower img')),'Live playback retains the same decoded image node');
  await page.locator('#story-compare').click();await page.locator('#story-field-b').waitFor({state:'visible'});await photoReady('#story-lower img');check(await page.locator('#story-lower img').count()===2,'Comparison has both real rookie-season headshots');await shot('comparison-1440.png');
  await go('movement');await ready('play');await page.locator('#photo-picker summary').click();await page.locator('#photo-grid button').first().waitFor();check(await page.locator('#photo-grid button').count()>100,'Photo-based athlete picker preserves the full mirror roster');
  const catalog=JSON.parse(fs.readFileSync(path.join(root,'outputs/presentation/catalog.json'),'utf8')),target=catalog.find(t=>t.nfl_id===58286&&t.drill==='PASS_PRO_MIRROR_DRILL');
  await page.locator('#photo-slot').selectOption('b');await page.locator(`[data-photo-attempt="${target.id}"]`).click();await ready('play');check(await page.locator('#player-b').inputValue()===target.id,'Choosing a headshot selects the corresponding actual attempt');check(await page.locator('#scorebug [data-player-id="58286"]').getAttribute('data-season')==='2025','Fairchild switches to his 2025 season portrait');
  await page.locator('#timeline').fill('3.2');await page.locator('#timeline').dispatchEvent('input');check((await page.locator('#large-time').textContent()).includes('3.20'),'Research timer stays synchronized with the original timeline');await photoReady('#scorebug img');await shot('movement-1440.png');
  await go('results');await page.locator('summary').filter({hasText:'Held-out players / season headshots'}).click();check(await page.locator('.portrait-grid .player-name').count()===17,'All OL holdout players have portrait or explicit unavailable identity tiles');await page.locator('#receiver-tab').click();await page.locator('summary').filter({hasText:'Held-out players / season headshots'}).click();check(await page.locator('.portrait-grid .player-name').count()===27,'Separate receiver experiment has its own 27-player portrait list');
  for(const viewport of [{width:1366,height:768},{width:390,height:844}]){await page.setViewportSize(viewport);for(const id of ['overview','film','movement','metric','results']){await go(id);if(id==='film')await ready('story-play');if(id==='movement'||id==='metric')await ready('play');check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`${viewport.width} ${id}: portrait and timer layout fits`);if(viewport.width===1366&&(id==='movement'||id==='film'))await shot(`${id}-1366.png`);}}
  const missing=await browser.newPage();await missing.route('**/portraits.json',route=>route.fulfill({json:{players:[]}}));await missing.goto(base+'#film');await missing.waitForFunction(()=>!document.getElementById('story-play').disabled);check(await missing.locator('#story-lower .portrait img').count()===0,'Missing portrait metadata does not substitute a different season');check((await missing.locator('#story-lower .portrait').textContent()).includes('NO PHOTO'),'Missing portraits have a clearly labeled initials fallback');await missing.close();
  check(errors.length===0,'No portrait/timer JavaScript errors');check(failed.length===0,'No missing normal-load portrait resources');
  fs.writeFileSync(path.join(out,'browser-report.json'),JSON.stringify({status:'passed',checks:checks.length,passed:checks,errors,failed_resources:failed,verified_at:new Date().toISOString()},null,2));console.log(`Passed ${checks.length} portrait/timer browser checks`);
 }catch(e){await shot('failure.png');throw e;}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
