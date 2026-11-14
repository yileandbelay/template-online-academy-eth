#!/usr/bin/env bash
# After `docker compose ... up -d --build`: warm the stack a little, then print memory per container.
set -euo pipefail
echo "waiting for the stack..."; for i in $(seq 1 60); do curl -fs http://127.0.0.1:8088/healthz >/dev/null && break; sleep 3; done
for i in $(seq 1 300); do curl -s -o /dev/null http://127.0.0.1:8088/healthz; curl -s -o /dev/null http://127.0.0.1:8088/courses; done
sleep 10
docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}\t{{.CPUPerc}}"
echo; echo "host total used (MB):"; free -m | awk '/Mem:/ {print $3}'
