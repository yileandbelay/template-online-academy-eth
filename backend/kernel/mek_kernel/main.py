"""Application factory. M0: health and readiness only; blocks are mounted by the registry from M1."""

from fastapi import FastAPI

from mek_kernel import __version__


def create_app() -> FastAPI:
    app = FastAPI(title="Mek API", version=__version__)

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    @app.get("/readyz")
    def readyz() -> dict[str, str]:
        # M1 adds database, identity and event-relay checks here.
        return {"status": "ready"}

    return app


app = create_app()
