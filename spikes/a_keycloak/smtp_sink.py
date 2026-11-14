"""A local SMTP server that stores every message as a file, so the spike can read the emails Keycloak sends.
uv run --with aiosmtpd python smtp_sink.py /tmp/kc/mail 1025"""

import sys, time, pathlib
from aiosmtpd.controller import Controller

out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)


class Sink:
    async def handle_DATA(self, server, session, envelope):
        name = out / f"{int(time.time() * 1000)}.eml"
        name.write_bytes(envelope.original_content)
        return "250 OK"


c = Controller(Sink(), hostname="127.0.0.1", port=int(sys.argv[2]))
c.start()
print("smtp sink on", sys.argv[2], flush=True)
while True:
    time.sleep(3600)
