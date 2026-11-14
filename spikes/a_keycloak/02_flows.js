// Browser flows on a 390 px phone viewport against the realm made by 01_setup.js.
const { chromium } = require('playwright');
const fs = require('fs');
const { admin, pkce, authUrl, exchange, passwordGrant, decodeJwt } = require('./kc');
const MAIL = '/tmp/kc/mail';
const out = (n) => `results/${n}.png`;
const stamp = Date.now();
const email = `abel.${stamp}@example.com`;
const log = (ok, name, detail = '') => console.log(`[${ok ? 'PASS' : 'FAIL'}] ${name}${detail ? '  (' + detail + ')' : ''}`);

async function newPage(browser) {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, locale: 'en-US' });
  const page = await ctx.newPage();
  await page.route('http://127.0.0.1:8099/**', (r) => r.fulfill({ status: 200, contentType: 'text/html', body: '<h1>app</h1>' }));
  return { ctx, page };
}
const waitMail = async (before, to, timeout = 20000) => {
  const t0 = Date.now();
  while (Date.now() - t0 < timeout) {
    const files = fs.readdirSync(MAIL).filter((f) => !before.has(f));
    for (const f of files) { const body = fs.readFileSync(`${MAIL}/${f}`, 'utf8'); if (body.toLowerCase().includes(to.toLowerCase())) return body; }
    await new Promise((r) => setTimeout(r, 300));
  }
  return null;
};
const linkFrom = (eml) => { const text = eml.replace(/=\r?\n/g, '').replace(/=3D/g, '='); const m = text.match(/https?:\/\/127\.0\.0\.1:8085\/[^\s"<>]+/); return m ? m[0].replace(/&amp;/g, '&') : null; };
const fields = async (page) => page.$$eval('input:not([type=hidden]):not([type=submit]):not([type=checkbox]), select', (els) => els.filter((e) => e.offsetParent).map((e) => e.name || e.id));

(async () => {
  const browser = await chromium.launch();
  const mails = () => new Set(fs.readdirSync(MAIL));

  // A. Sign up from "Enrol" on a course page, then come back to that course.
  {
    const { verifier, challenge } = pkce();
    const { page, ctx } = await newPage(browser);
    let navs = 0; page.on('framenavigated', (f) => { if (f === page.mainFrame()) navs++; });
    await page.goto(authUrl({ state: '/courses/excel-for-the-workplace', code_challenge: challenge }));
    await page.screenshot({ path: out('a1-login-390') });
    await page.click('a:has-text("Register")');
    await page.waitForSelector('#email');
    await page.screenshot({ path: out('a2-register-390'), fullPage: true });
    const f = await fields(page);
    log(true, 'A1 registration form fields shown', f.join(', '));
    await page.fill('#email', email); await page.fill('#firstName', 'Abel'); await page.fill('#lastName', 'Tesfaye');
    await page.fill('#phone', '+251911223344'); await page.fill('#city', 'Addis Ababa');
    await page.fill('#password', 'Spike-Pass-2026!'); await page.fill('#password-confirm', 'Spike-Pass-2026!');
    const t0 = Date.now();
    const [req] = await Promise.all([page.waitForRequest((r) => r.url().startsWith('http://127.0.0.1:8099/'), { timeout: 30000 }), page.click('input[type=submit], button[type=submit]')]);
    const ms = Date.now() - t0;
    const u = new URL(req.url());
    log(u.searchParams.get('state') === '/courses/excel-for-the-workplace', 'A2 after registering the learner is sent back to the course they chose', `state=${u.searchParams.get('state')} in ${ms} ms`);
    const tok = await exchange(u.searchParams.get('code'), verifier);
    const claims = tok.json.id_token ? decodeJwt(tok.json.id_token) : {};
    log(claims.email === email && claims.phone === '+251911223344' && claims.city === 'Addis Ababa' && claims.given_name === 'Abel',
      'A3 token carries email, name, phone and city claims', `email=${claims.email} phone=${claims.phone} city=${claims.city}`);
    log(true, 'A4 pages visited from login to back in the app', `${navs} navigations (login, register form, redirect)`);
    await ctx.close();
  }

  // B. Plain login.
  {
    const { verifier, challenge } = pkce();
    const { page, ctx } = await newPage(browser);
    await page.goto(authUrl({ state: '/dashboard', code_challenge: challenge }));
    await page.fill('#username', email); await page.fill('#password', 'Spike-Pass-2026!');
    const t0 = Date.now();
    const [req] = await Promise.all([page.waitForRequest((r) => r.url().startsWith('http://127.0.0.1:8099/'), { timeout: 30000 }), page.click('#kc-login')]);
    const code = new URL(req.url()).searchParams.get('code');
    const tok = await exchange(code, verifier);
    log(tok.status === 200, 'B login with email and password', `${Date.now() - t0} ms to redirect`);
    await ctx.close();
  }

  // C. Forgot password by email, set a new one, log in with it.
  {
    const { challenge } = pkce();
    const { page, ctx } = await newPage(browser);
    const before = mails();
    await page.goto(authUrl({ state: '/dashboard', code_challenge: challenge }));
    await page.click('a:has-text("Forgot Password")');
    await page.fill('#username', email); await page.click('input[type=submit], button[type=submit]');
    await page.screenshot({ path: out('c1-forgot-sent-390') });
    const eml = await waitMail(before, email);
    const link = eml && linkFrom(eml);
    log(!!link, 'C1 reset email arrives with a link', link ? link.slice(0, 70) + '...' : 'no email');
    if (link) {
      await page.goto(link);
      await page.screenshot({ path: out('c2-reset-390') });
      const hasNew = await page.$('#password-new');
      if (hasNew) { await page.fill('#password-new', 'Brand-New-Pass-2026!'); await page.fill('#password-confirm', 'Brand-New-Pass-2026!'); await page.click('input[type=submit], button[type=submit]'); }
      await page.waitForTimeout(1500);
      const g = await passwordGrant(email, 'Brand-New-Pass-2026!');
      log(g.status === 200, 'C2 the new password works', `HTTP ${g.status} ${g.error || ''}`);
    }
    await ctx.close();
  }

  // D. Staff invitation: admin creates the account, Keycloak emails a "set your password" link.
  {
    const inv = `teacher.${stamp}@example.com`;
    const before = mails();
    const c = await admin('POST', '/mek/users', { username: inv, email: inv, firstName: 'Meklit', lastName: 'Haile', enabled: true, emailVerified: true,
      attributes: { phone: ['+251922334455'], city: ['Addis Ababa'] }, requiredActions: ['UPDATE_PASSWORD'] });
    const id = c.headers.get('location')?.split('/').pop();
    const a = await admin('PUT', `/mek/users/${id}/execute-actions-email?client_id=web&redirect_uri=${encodeURIComponent('http://127.0.0.1:8099/cb')}&lifespan=604800`, ['UPDATE_PASSWORD']);
    const eml = await waitMail(before, inv);
    const link = eml && linkFrom(eml);
    log(c.status === 201 && a.status === 204 && !!link, 'D1 invitation email with a set-your-password link (7-day lifetime)', `create ${c.status}, send ${a.status}`);
    if (link) {
      const { page, ctx } = await newPage(browser);
      await page.goto(link);
      await page.screenshot({ path: out('d1-invite-390') });
      if (await page.$('a:has-text("Click here to proceed")')) await page.click('a:has-text("Click here to proceed")');
      await page.waitForSelector('#password-new', { timeout: 15000 });
      await page.fill('#password-new', 'Teacher-Pass-2026!'); await page.fill('#password-confirm', 'Teacher-Pass-2026!');
      await page.click('input[type=submit], button[type=submit]'); await page.waitForTimeout(1500);
      const g = await passwordGrant(inv, 'Teacher-Pass-2026!');
      log(g.status === 200, 'D2 invited person sets a password and can sign in', `HTTP ${g.status} ${g.error || ''}`);
      await ctx.close();
    }
  }

  // E. Amharic: what does Keycloak show for locale am out of the box?
  {
    const { challenge } = pkce();
    const { page, ctx } = await newPage(browser);
    await page.goto(authUrl({ kc_locale: 'am', code_challenge: challenge }));
    const label = await page.textContent('#kc-login');
    const opts = await page.$$eval('#kc-locale-dropdown a, [id^=language-] a, a[href*="kc_locale"]', (els) => els.map((e) => e.textContent.trim()));
    await page.screenshot({ path: out('e1-amharic-default-390') });
    log(/Sign In/i.test(label), 'E1 stock Keycloak has no Amharic: the page falls back to English', `button says "${label.trim()}", locale links: ${opts.join(' | ')}`);
    await ctx.close();
  }
  await browser.close();
})().catch((e) => { console.error('SCRIPT ERROR', e); process.exit(1); });
