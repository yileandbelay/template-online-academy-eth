// Small helpers for talking to a local Keycloak. Spike code, not production code.
const crypto = require('crypto');
const BASE = process.env.KC_URL || 'http://127.0.0.1:8085';
const REALM = 'mek';
const form = (o) => new URLSearchParams(o).toString();
async function adminToken() {
  const r = await fetch(`${BASE}/realms/master/protocol/openid-connect/token`, { method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: form({ grant_type: 'password', client_id: 'admin-cli', username: 'admin', password: 'admin-spike-only' }) });
  return (await r.json()).access_token;
}
async function admin(method, path, body) {
  const token = await adminToken();
  const r = await fetch(`${BASE}/admin/realms${path}`, { method, headers: { authorization: `Bearer ${token}`, 'content-type': 'application/json' }, body: body ? JSON.stringify(body) : undefined });
  const text = await r.text();
  return { status: r.status, json: text ? (() => { try { return JSON.parse(text); } catch { return text; } })() : null, headers: r.headers };
}
const b64url = (b) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
function pkce() { const verifier = b64url(crypto.randomBytes(32)); return { verifier, challenge: b64url(crypto.createHash('sha256').update(verifier).digest()) }; }
const authUrl = (o) => `${BASE}/realms/${REALM}/protocol/openid-connect/auth?` + form({ client_id: 'web', response_type: 'code', scope: 'openid',
  redirect_uri: 'http://127.0.0.1:8099/cb', code_challenge_method: 'S256', ...o });
async function exchange(code, verifier) {
  const r = await fetch(`${BASE}/realms/${REALM}/protocol/openid-connect/token`, { method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: form({ grant_type: 'authorization_code', client_id: 'web', code, code_verifier: verifier, redirect_uri: 'http://127.0.0.1:8099/cb' }) });
  return { status: r.status, json: await r.json() };
}
async function passwordGrant(username, password) {
  const t0 = performance.now();
  const r = await fetch(`${BASE}/realms/${REALM}/protocol/openid-connect/token`, { method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: form({ grant_type: 'password', client_id: 'load', username, password, scope: 'openid' }) });
  const j = await r.json().catch(() => ({}));
  return { status: r.status, ms: performance.now() - t0, error: j.error_description || j.error };
}
const decodeJwt = (t) => JSON.parse(Buffer.from(t.split('.')[1], 'base64url').toString());
const rssMb = () => { const { execSync } = require('child_process');
  const pid = execSync("pgrep -f 'quarkus-run.jar|io.quarkus.bootstrap.runner' | head -1").toString().trim();
  return Math.round(parseInt(execSync(`ps -o rss= -p ${pid}`).toString()) / 1024); };
module.exports = { BASE, REALM, admin, pkce, authUrl, exchange, passwordGrant, decodeJwt, rssMb, form, adminToken };
