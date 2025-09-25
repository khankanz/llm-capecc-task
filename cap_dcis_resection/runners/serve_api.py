"""ASGI application exposing validation and prompt assembly."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException

from cap_dcis_resection import DEFAULT_PROMPT, ResectionPrompt, validate_context


def create_app() -> FastAPI:
    app = FastAPI(title="CAP DCIS Resection API", version="0.1.0")

    @app.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/prompts", tags=["prompts"])
    def build_prompt(payload: dict) -> dict[str, object]:
        ok, context, errors = validate_context(payload)
        if not ok or context is None:
            raise HTTPException(status_code=422, detail=errors)
        prompt = ResectionPrompt(context=context)
        return {"template": DEFAULT_PROMPT, "payload": prompt.to_prompt_dict()}

    return app


app = create_app()
