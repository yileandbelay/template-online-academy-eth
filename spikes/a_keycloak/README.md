# Spike A: Keycloak footprint, Amharic, sign-up, invitations, Mek password migration

Throwaway spike code. Result and recommendation: `docs/spikes/m0-report.md`. Keycloak 26.8.2 (production mode, PostgreSQL 16).

## Run it
```bash
# 1. download and build (Keycloak from Maven Central; Java 21 needed)
mkdir -p /tmp/kc && cd /tmp/kc
curl -O https://repo.maven.apache.org/maven2/org/keycloak/keycloak-quarkus-dist/26.8.2/keycloak-quarkus-dist-26.8.2.zip
unzip -q keycloak-quarkus-dist-26.8.2.zip && cd keycloak-26.8.2
cp -r <repo>/spikes/a_keycloak/theme-mek themes/mek                  # custom login theme with Amharic messages
export KC_BOOTSTRAP_ADMIN_USERNAME=admin KC_BOOTSTRAP_ADMIN_PASSWORD=admin-spike-only
./bin/kc.sh build --db=postgres
./bin/kc.sh start --optimized --http-enabled=true --hostname-strict=false --http-port=8085 \
  --db-url=jdbc:postgresql://127.0.0.1:5544/keycloak --db-username=keycloak --db-password=x
# 2. a mail sink so the emails can be read (port 1025), then the scripts in this folder
uv run --with aiosmtpd python smtp_sink.py /tmp/kc/mail 1025 &
node 01_setup.js && node 02_flows.js && node 03_load_and_hashes.js && node 04_amharic_theme.js
```
(`spikes/c_rls/README.md` shows how to start the PostgreSQL cluster used here.)

## What each script checks
- `01_setup.js`: the realm the template would use: email as username, phone (required) and city on sign-up, English and Amharic, SMTP.
- `02_flows.js`: on a 390 px phone: sign-up and return to the course the learner chose (OIDC `state`); token claims; login; forgot-password
  email and new password; staff invitation email ("set your password", 7 days); what stock Keycloak shows for Amharic. Screenshots in `results/`.
- `03_load_and_hashes.js`: 600 logins, memory; import of PBKDF2 and scrypt password hashes.
- `04_amharic_theme.js`: the custom theme `theme-mek` with `messages_am.properties` (technical test; the Amharic strings are **not** reviewed).

## Notes
- Amharic is selected with the standard OIDC parameter `ui_locales=am` (or the language dropdown).
- The theme files here include two fixes found after the last run (`requiredFields` without a doubled asterisk, `phone` and `city`
  labels); they were not re-run.
