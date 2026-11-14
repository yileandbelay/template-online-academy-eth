# Spike D: footprint of the local stack

Throwaway scripts. Result: `docs/spikes/m0-report.md`.

- `measure_pss.py`: memory of each component running natively, as PSS (proportional set size; not inflated by shared pages).
  This is what produced the numbers in the report (PostgreSQL 16, PgBouncer, Keycloak, Traefik, MinIO, Next.js, the API).
- `docker-compose.spike.yml` + `measure.sh`: the same stack in containers, so you can measure it on your machine with
  `docker stats`. **Untested where it was written** (that environment had no Docker daemon); expect to fix small things, and pin
  image tags you keep. Run:
  ```bash
  docker compose -f spikes/d_footprint/docker-compose.spike.yml up -d --build
  bash spikes/d_footprint/measure.sh
  docker compose -f spikes/d_footprint/docker-compose.spike.yml down -v
  ```
