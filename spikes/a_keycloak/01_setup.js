// Creates the "mek" realm the way the template would: email as username, phone and city on sign-up, English and Amharic.
const { admin } = require('./kc');
(async () => {
  await admin('DELETE', '/mek');
  let r = await admin('POST', '', {
    realm: 'mek', enabled: true, sslRequired: 'none', registrationAllowed: true, registrationEmailAsUsername: true, loginWithEmailAllowed: true,
    duplicateEmailsAllowed: false, resetPasswordAllowed: true, rememberMe: true, verifyEmail: false,
    internationalizationEnabled: true, supportedLocales: ['en', 'am'], defaultLocale: 'en',
    smtpServer: { host: '127.0.0.1', port: '1025', from: 'no-reply@mek.test', fromDisplayName: 'Mek Academy', auth: 'false', ssl: 'false', starttls: 'false' },
  });
  console.log('realm', r.status);
  const perm = { view: ['admin', 'user'], edit: ['admin', 'user'] };
  r = await admin('PUT', '/mek/users/profile', { attributes: [
    { name: 'username', displayName: '${username}', validations: { length: { min: 3, max: 255 }, 'username-prohibited-characters': {}, 'up-username-not-idn-homograph': {} }, permissions: perm },
    { name: 'email', displayName: '${email}', validations: { email: {}, length: { max: 255 } }, required: { roles: ['user'] }, permissions: perm },
    { name: 'firstName', displayName: '${firstName}', validations: { length: { max: 255 } }, required: { roles: ['user'] }, permissions: perm },
    { name: 'lastName', displayName: '${lastName}', validations: { length: { max: 255 } }, required: { roles: ['user'] }, permissions: perm },
    { name: 'phone', displayName: 'Phone', validations: { pattern: { pattern: '^\\+?[0-9 ]{9,15}$', 'error-message': 'Enter a valid phone number' } }, required: { roles: ['user'] }, permissions: perm },
    { name: 'city', displayName: 'City', validations: { length: { max: 100 } }, permissions: perm },
  ] });
  console.log('user profile', r.status);
  const mapper = (n) => ({ name: n, protocol: 'openid-connect', protocolMapper: 'oidc-usermodel-attribute-mapper',
    config: { 'user.attribute': n, 'claim.name': n, 'jsonType.label': 'String', 'id.token.claim': 'true', 'access.token.claim': 'true', 'userinfo.token.claim': 'true' } });
  r = await admin('POST', '/mek/clients', { clientId: 'web', publicClient: true, standardFlowEnabled: true, directAccessGrantsEnabled: false,
    redirectUris: ['http://127.0.0.1:8099/*'], webOrigins: ['+'], attributes: { 'pkce.code.challenge.method': 'S256' }, protocolMappers: [mapper('phone'), mapper('city')] });
  console.log('client web', r.status);
  r = await admin('POST', '/mek/clients', { clientId: 'load', publicClient: true, standardFlowEnabled: false, directAccessGrantsEnabled: true, protocolMappers: [mapper('phone')] });
  console.log('client load', r.status);
})();
