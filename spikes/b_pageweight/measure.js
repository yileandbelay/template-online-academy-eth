// Page-weight harness: loads URLs in Chromium with a phone-like CPU and network profile and reports bytes and timings.
// usage: node measure.js <profile> <label> <url> [<url> ...]      profiles: fast3g | slow3g | none
const { chromium } = require('playwright');

const PROFILES = {
  // Lighthouse "mobile" simulation: 1.6 Mbps down, 750 Kbps up, 150 ms round trip, 4x slower CPU.
  fast3g: { down: (1.6 * 1024 * 1024) / 8, up: (750 * 1024) / 8, latency: 150, cpu: 4 },
  // DevTools "Slow 3G": 400 Kbps, 400 ms. A stress case for weak connections.
  slow3g: { down: (400 * 1024) / 8, up: (400 * 1024) / 8, latency: 400, cpu: 4 },
  none: null,
};

async function once(browser, url, profile) {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true,
    userAgent: 'Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Mobile Safari/537.36' });
  const page = await ctx.newPage();
  const cdp = await ctx.newCDPSession(page);
  await cdp.send('Network.enable');
  await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
  if (profile) {
    await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: profile.latency,
      downloadThroughput: profile.down, uploadThroughput: profile.up });
    await cdp.send('Emulation.setCPUThrottlingRate', { rate: profile.cpu });
  }
  const byType = {}; const reqs = new Map(); let total = 0; let count = 0;
  cdp.on('Network.responseReceived', (e) => reqs.set(e.requestId, e.type));
  cdp.on('Network.loadingFinished', (e) => {
    const type = (reqs.get(e.requestId) || 'Other'); total += e.encodedDataLength; count++;
    byType[type] = (byType[type] || 0) + e.encodedDataLength;
  });
  await page.addInitScript(() => {
    window.__m = { lcp: 0, fcp: 0 };
    new PerformanceObserver((l) => { for (const e of l.getEntries()) window.__m.lcp = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true });
    new PerformanceObserver((l) => { for (const e of l.getEntries()) if (e.name === 'first-contentful-paint') window.__m.fcp = e.startTime; }).observe({ type: 'paint', buffered: true });
  });
  const t0 = Date.now();
  let status = 0;
  try { const r = await page.goto(url, { waitUntil: 'load', timeout: 120000 }); status = r ? r.status() : 0; } catch (e) { status = -1; }
  let idle = -1;
  try { await page.waitForLoadState('networkidle', { timeout: 90000 }); idle = Date.now() - t0; } catch (e) { idle = -1; }
  await page.waitForTimeout(500);
  const m = await page.evaluate(() => window.__m);
  const nav = await page.evaluate(() => { const n = performance.getEntriesByType('navigation')[0]; return n ? { dcl: n.domContentLoadedEventEnd, load: n.loadEventEnd } : {}; });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  await ctx.close();
  return { status, total, count, byType, fcp: m.fcp, lcp: m.lcp, dcl: nav.dcl, load: nav.load, idle, wall: Date.now() - t0, overflow };
}

(async () => {
  const [profileName, label, ...urls] = process.argv.slice(2);
  const profile = PROFILES[profileName];
  const browser = await chromium.launch();
  const kb = (n) => (n / 1024).toFixed(1);
  console.log(`\n## ${label} (${profileName})`);
  console.log('| page | status | requests | total KB | JS KB | CSS KB | HTML KB | font KB | image KB | FCP ms | LCP ms | network idle ms | h-overflow |');
  console.log('|---|---|---|---|---|---|---|---|---|---|---|---|---|');
  for (const url of urls) {
    const runs = [];
    for (let i = 0; i < 3; i++) runs.push(await once(browser, url, profile));
    runs.sort((a, b) => a.lcp - b.lcp); const r = runs[1]; // median of 3 by LCP
    const t = r.byType;
    console.log(`| ${url.replace(/^https?:\/\/[^/]+/, '') || '/'} | ${r.status} | ${r.count} | ${kb(r.total)} | ${kb(t.Script || 0)} | ${kb(t.Stylesheet || 0)} | ${kb(t.Document || 0)} | ${kb(t.Font || 0)} | ${kb(t.Image || 0)} | ${Math.round(r.fcp)} | ${Math.round(r.lcp)} | ${Math.round(r.idle)} | ${r.overflow ? 'YES' : 'no'} |`);
  }
  await browser.close();
})();
