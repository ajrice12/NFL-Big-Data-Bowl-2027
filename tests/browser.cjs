/* Start scripts.serve first. PLAYWRIGHT_MODULE_PATH may point to an existing install. */
const fs=require('node:fs'),path=require('node:path');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE_PATH||'playwright');
const root=path.resolve(__dirname,'..'),out=path.join(root,'outputs/verification/v3/research-regression');fs.mkdirSync(out,{recursive:true});
const base=process.env.PRESENTATION_URL||'http://127.0.0.1:8765/presentation/';
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.BROWSER_EXECUTABLE||'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:900}}),errors=[],failed=[],requests=[],checks=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
 page.on('request',r=>requests.push(r.url()));page.on('requestfailed',r=>failed.push(r.url()));page.on('response',r=>{if(r.status()>=400)failed.push(`${r.status()} ${r.url()}`)});
 const check=(value,label)=>{if(!value)throw Error(label);checks.push(label);};
 const nav=async id=>{await page.locator(`#chapters a[href="#${id}"]`).click();await page.locator(`[data-section="${id}"]`).waitFor();};
 const ready=async()=>{await page.locator('#play').waitFor();await page.waitForFunction(()=>!document.getElementById('play').disabled)};
 const screenshot=async name=>{await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:path.join(out,name),fullPage:true,animations:'disabled'});};
 try{
  const start=Date.now();await page.goto(base+'#overview',{waitUntil:'networkidle'});await page.locator('[data-section="overview"]').waitFor();const loadMs=Date.now()-start;
  check(await page.locator('#chapters a').count()===5,'Five concise presentation sections');
  check((await page.locator('.overview').textContent()).includes('NO CLEAR ADDED VALUE'),'First screen states actual exploratory finding');
  check((await page.locator('.cohort-counts').textContent()).includes('21,363'),'First screen shows verified model-cohort opportunity count');
  check(requests.filter(u=>u.includes('/attempts/')).length===2,'Initial overview fetches only two featured attempts');
  check(!requests.some(u=>u.endsWith('/research.json')||u.endsWith('/catalog.json')||u.endsWith('/appendix.json')),'No full trajectory bundle, catalog or raw samples at startup');
  check(fs.statSync(path.join(root,'outputs/presentation/briefing.json')).size<65000,'Compact initial evidence file is under 65 KB');
  check(await page.locator('.cohort-counts').evaluate(e=>e.getBoundingClientRect().bottom<=innerHeight),'Cohort counts are visible without scrolling on initial screen');
  check(await page.locator('.evidence-strip').evaluate(e=>e.getBoundingClientRect().bottom<=innerHeight),'Main finding is visible without scrolling on initial screen');
  await screenshot('01-overview.png');
  await nav('movement');await ready();check((await page.locator('.scorebug').textContent()).includes("O'Cyrus Torrence")&&(await page.locator('.scorebug').textContent()).includes('Steve Avila'),'Default comparison uses documented comparable guards');
  const catalog=JSON.parse(fs.readFileSync(path.join(root,'outputs/presentation/catalog.json'),'utf8'));
  await page.locator('#player-a').selectOption({index:2});await ready();const selected=await page.locator('#player-a').inputValue(),meta=catalog.find(t=>t.id===selected);
  check((await page.locator('.scorebug').textContent()).includes(meta.name)&&(await page.locator('.scorebug').textContent()).includes(`ID ${meta.nfl_id}`),'Selected name and NFL ID match source attempt metadata');
  check((await page.locator('.scorebug').textContent()).includes(`ATT ${meta.attempt}`),'Selected attempt identifier matches metadata');
  const t=JSON.parse(fs.readFileSync(path.join(root,'outputs/presentation',meta.file),'utf8'));
  await page.locator('#timeline').fill('2');await page.locator('#timeline').dispatchEvent('input');const index=t.frames.findLastIndex(f=>f[0]-t.frames[0][0]<=2+1e-7);
  check((await page.locator('.athlete-score').first().textContent()).includes(`F${index+1}/${t.frames.length}`),'Scrubbing selects actual recorded frame by timestamp');
  await page.locator('#play').click();await page.waitForTimeout(350);check(Number(await page.locator('#timeline').inputValue())>2,'Playback advances real elapsed time');await page.locator('#play').click();const paused=await page.locator('#timeline').inputValue();await page.waitForTimeout(120);check(await page.locator('#timeline').inputValue()===paused,'Pause freezes timeline');
  await page.locator('#speed').selectOption('2');await page.locator('#encoding').selectOption('speed');await page.locator('#encoding').selectOption('acceleration');checks.push('Playback speed and speed/acceleration trail controls');
  await page.locator('#view-mode').selectOption('split');check(await page.locator('#field-b').isVisible(),'Side-by-side field comparison');await page.locator('#view-mode').selectOption('overlay');
  const geometry=await page.evaluate(async()=>{const {geometry,observedFrame}=await import('./scripts/field.js');const a={frames:[[0,0,0,1,0,0,0,1],[.1,1,1,1,0,0,0,1],[1,3,2,1,0,0,0,2]]};const b={frames:[[0,100,200,1,0,0,0,1],[.1,101,201,1,0,0,0,1]]};const g=geometry([a,b]),p=g.point(a,a.frames[0]),q=g.point(a,a.frames[1]),r=g.point(b,b.frames[1]);return {isotropic:Math.abs((q[0]-p[0])+(q[1]-p[1]))<1e-8,translation:Math.abs(q[0]-r[0])+Math.abs(q[1]-r[1])<1e-8,gapIndex:observedFrame(a,.5)};});
  check(geometry.isotropic&&geometry.translation,'Field mapping preserves geometry with isotropic shared scale and translation only');check(geometry.gapIndex===1,'Playback does not interpolate missing coordinates across a gap');
  await page.locator('#restart').click();check(Number(await page.locator('#timeline').inputValue())===0,'Replay resets recorded clock');
  await page.locator('#drill').selectOption({index:1});await ready();check((await page.locator('.film-analysis').textContent()).includes('LRE not defined'),'Context drill does not receive fabricated LRE');
  await page.locator('#drill').selectOption('PASS_PRO_MIRROR_DRILL');await ready();await page.locator('#timeline').fill('3.8');await page.locator('#timeline').dispatchEvent('input');await screenshot('02-movement.png');
  await nav('metric');await ready();await page.locator('[data-phase="reversal"]').click();check((await page.locator('#time').textContent()).startsWith('1.50'),'Metric step jumps to actual observed reversal');await page.locator('[data-phase="recovery"]').click();check((await page.locator('#event-measure').textContent()).includes('0.60'),'Worked recovery delay originates from recorded reversal output');
  await page.locator('#target-fraction').selectOption('0.25');check((await page.locator('#event-measure').textContent()).includes('0.70'),'Alternate target changes actual recovery measurement');await page.locator('#reversal-event').selectOption('1');check((await page.locator('#time').textContent()).startsWith('3.10'),'Reversal-event selector seeks actual timestamp');await screenshot('03-metric.png');
  await page.locator('#methods-appendix summary').click();await page.locator('[data-step="8"]').waitFor();for(let i=0;i<9;i++){await page.locator(`[data-step="${i}"]`).click();check((await page.locator('#alg-content').textContent()).length>150,`Preserved methodology step ${i+1}`);}
  await nav('results');check((await page.locator('#result-content').textContent()).includes('2.3369'),'OL performance shown in correctly converted percentage points');check(await page.locator('#result-content svg:visible').count()===3,'Legible baseline, interval and prediction charts render');await screenshot('04-results.png');await page.locator('#receiver-tab').click();check((await page.locator('#result-content').textContent()).includes('0.249'),'Receiver experiment remains distinct');await page.locator('#ol-tab').click();
  await nav('application');check((await page.locator('.application').textContent()).includes('13,490'),'Timing chart contains the verified early-censoring count');await screenshot('05-application.png');
  await nav('overview');await page.locator('#data-appendix summary').click();await page.locator('#sample-table').waitFor();await page.locator('#sample-table').selectOption({index:1});check(await page.locator('#sample-preview tbody tr').count()>0,'Secondary local data appendix loads only on request');
  for(const viewport of [{width:1366,height:768},{width:1920,height:1080},{width:1280,height:800},{width:390,height:844}]){
   await page.setViewportSize(viewport);for(const id of ['overview','movement','metric','results','application']){await nav(id);if(id==='movement'||id==='metric')await ready();check(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`${viewport.width}×${viewport.height} ${id}: no page overflow`);}
   if(viewport.width===1366){await nav('movement');await ready();await screenshot('laptop-movement.png');}if(viewport.width===390)await screenshot('mobile-application.png');
  }
  check(errors.length===0,'No normal-load JavaScript or console errors');check(failed.length===0,'No failed normal application resources');
  const missing=await browser.newPage();await missing.route('**/briefing.json',r=>r.fulfill({status:404,body:'missing'}));await missing.goto(base);await missing.locator('[role="alert"]').waitFor();check((await missing.locator('[role="alert"]').textContent()).includes('Analysis incomplete'),'Missing briefing shows incomplete-analysis state');await missing.close();
  const model=await browser.newPage();await model.route('**/briefing.json',r=>{const d=JSON.parse(fs.readFileSync(path.join(root,'outputs/presentation/briefing.json'),'utf8'));delete d.ol.models;return r.fulfill({json:d});});await model.goto(base+'#results');await model.locator('[role="alert"]').waitFor();check((await model.locator('[role="alert"]').textContent()).includes('OL model results unavailable'),'Missing model output displays incomplete status instead of scores');await model.close();
  const unavailable=await browser.newPage();await unavailable.route('**/attempts/*.json',r=>r.fulfill({status:404,body:'missing'}));await unavailable.goto(base+'#movement');await unavailable.locator('.viewer-status.failed').waitFor();check(await unavailable.locator('#play').isDisabled(),'Missing selected trajectory disables playback and hides stale film');await unavailable.close();
  const raw=await page.request.get(new URL('../data/raw/players.csv',base).href);check(raw.status()===404,'Original CSVs remain unavailable through presentation server');
  const report={status:'passed',checks:checks.length,passed:checks,errors,failed_resources:failed,initial_load_ms:loadMs,initial_attempt_requests:2,briefing_bytes:fs.statSync(path.join(root,'outputs/presentation/briefing.json')).size,verified_at:new Date().toISOString(),url:base};fs.writeFileSync(path.join(out,'browser-report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
 }catch(e){await screenshot('failure.png');fs.writeFileSync(path.join(out,'browser-report.json'),JSON.stringify({status:'failed',checks,errors,failed_resources:failed,error:e.stack},null,2));console.log(await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,over:[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).slice(0,12).map(e=>[e.tagName,e.className,e.getBoundingClientRect().right])})));throw e;}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
