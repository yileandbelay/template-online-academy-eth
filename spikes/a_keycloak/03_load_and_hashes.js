// Capacity: memory and login throughput. Then: can Keycloak take over Mek's password hashes?
const crypto = require('crypto');
const { admin, passwordGrant, rssMb } = require('./kc');
const log = (ok, name, detail = '') => console.log(`[${ok ? 'PASS' : 'INFO'}] ${name}${detail ? '  (' + detail + ')' : ''}`);
const pct = (a, p) => a.slice().sort((x, y) => x - y)[Math.min(a.length - 1, Math.floor(a.length * p))];

(async () => {
  const stamp = Date.now();
  // 1. 40 learners, then a burst of password logins.
  const users = [];
  const t0 = Date.now();
  for (let i = 0; i < 40; i++) {
    const email = `load${i}.${stamp}@example.com`;
    await admin('POST', '/mek/users', { username: email, email, firstName: 'L', lastName: String(i), enabled: true, emailVerified: true,
      attributes: { phone: ['+251911000000'] }, credentials: [{ type: 'password', value: 'Load-Pass-2026!', temporary: false }] });
    users.push(email);
  }
  log(true, 'create 40 learners through the admin API', `${((Date.now() - t0) / 40).toFixed(0)} ms each`);
  const rssBefore = rssMb();
  const lat = []; let fails = 0; let next = 0; const N = 600; const C = 8;
  const w0 = Date.now();
  await Promise.all(Array.from({ length: C }, async () => { while (next < N) { const i = next++; const r = await passwordGrant(users[i % users.length], 'Load-Pass-2026!'); lat.push(r.ms); if (r.status !== 200) fails++; } }));
  const secs = (Date.now() - w0) / 1000;
  log(fails === 0, `${N} password logins, ${C} at a time`, `${(N / secs).toFixed(0)} logins/s; p50 ${pct(lat, 0.5).toFixed(0)} ms, p95 ${pct(lat, 0.95).toFixed(0)} ms, failures ${fails}`);
  log(true, 'memory of the Keycloak process (RSS)', `before the burst ${rssBefore} MB, after ${rssMb()} MB`);

  // 2. Password hashes. Mek stores Werkzeug hashes; which can Keycloak read?
  const cred = (value, salt, algorithm, iterations) => ({ type: 'password',
    secretData: JSON.stringify({ value, salt, additionalParameters: {} }), credentialData: JSON.stringify({ hashIterations: iterations, algorithm, additionalParameters: {} }) });
  const pw = 'Legacy-Pass-2026!';
  const salt = crypto.randomBytes(16);
  const pbkdf2 = crypto.pbkdf2Sync(pw, salt, 600000, 32, 'sha256').toString('base64');
  const e1 = `pbkdf2.${stamp}@example.com`;
  const c1 = await admin('POST', '/mek/users', { username: e1, email: e1, firstName: 'P', lastName: 'B', enabled: true, emailVerified: true, attributes: { phone: ['+251911000000'] },
    credentials: [cred(pbkdf2, salt.toString('base64'), 'pbkdf2-sha256', 600000)] });
  const g1 = await passwordGrant(e1, pw);
  log(g1.status === 200, 'import a PBKDF2-SHA256 hash (an older Werkzeug default): login works with no password reset', `create ${c1.status}, login HTTP ${g1.status}`);
  const id1 = (await admin('GET', `/mek/users?email=${e1}&exact=true`)).json[0].id;
  const cr = (await admin('GET', `/mek/users/${id1}/credentials`)).json[0];
  log(true, 'after that first login Keycloak upgrades the stored hash to its own current algorithm', JSON.parse(cr.credentialData).algorithm + ', ' + JSON.parse(cr.credentialData).hashIterations + ' iterations');

  const e2 = `scrypt.${stamp}@example.com`;
  const scrypt = crypto.scryptSync(pw, salt, 64, { N: 32768, r: 8, p: 1, maxmem: 128 * 1024 * 1024 }).toString('base64');
  const c2 = await admin('POST', '/mek/users', { username: e2, email: e2, firstName: 'S', lastName: 'C', enabled: true, emailVerified: true, attributes: { phone: ['+251911000000'] },
    credentials: [cred(scrypt, salt.toString('base64'), 'scrypt', 32768)] });
  const g2 = await passwordGrant(e2, pw);
  log(g2.status !== 200, 'import a scrypt hash (the Werkzeug 3 default, what Mek uses today): Keycloak cannot verify it', `create ${c2.status}, login HTTP ${g2.status} ${g2.error || ''}`);
})().catch((e) => { console.error('SCRIPT ERROR', e); process.exit(1); });
