"""Memory of each local component as PSS (proportional set size: shared pages are split between the processes that share them,
so the sum is not inflated the way adding up RSS is). Linux only.   python3 measure_pss.py"""

import os, re, subprocess

COMPONENTS = {
    "PostgreSQL 16 (default settings)": lambda c, u: u == "postgres" and "pgbouncer" not in c,
    "PgBouncer": lambda c, u: "pgbouncer" in c,
    "Keycloak 26.8.2 (JVM, production mode)": lambda c, u: "quarkus-run.jar" in c or "io.quarkus.bootstrap.runner" in c,
    "Next.js 16 server (next start)": lambda c, u: (
        "next-server" in c or ("next" in c and "start" in c and "node" in c and "gzip" not in c)
    ),
    "Traefik v3 (gateway, after 1,200 proxied requests)": lambda c, u: (
        "traefik --config" in c or c.endswith("/traefik --configFile=/tmp/traefik/traefik.yml")
    ),
    "MinIO (object storage, idle)": lambda c, u: "minio server" in c,
    "API (uvicorn + FastAPI, mek_kernel)": lambda c, u: "uvicorn" in c and "mek_kernel" in c,
}


def pss_kb(pid):
    try:
        with open(f"/proc/{pid}/smaps_rollup") as f:
            return int(re.search(r"^Pss:\s+(\d+)", f.read(), re.M).group(1))
    except Exception:
        return 0


def main():
    ps = subprocess.run(["ps", "-eo", "pid=,user=,args="], capture_output=True, text=True).stdout.splitlines()
    rows = [(int(l.split(None, 2)[0]), l.split(None, 2)[1], l.split(None, 2)[2]) for l in ps]
    total = 0
    print(f"{'component':45} {'processes':>9} {'PSS MB':>8}")
    for name, match in COMPONENTS.items():
        pids = [p for p, u, c in rows if match(c, u) and p != os.getpid()]
        mb = sum(pss_kb(p) for p in pids) / 1024
        total += mb
        print(f"{name:45} {len(pids):>9} {mb:>8.0f}")
    print(f"{'TOTAL of the above':45} {'':>9} {total:>8.0f}")


main()
