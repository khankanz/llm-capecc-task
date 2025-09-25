"""Command line utilities for batch prompt creation."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich import print

from cap_dcis_resection import ContextWindow, PatientContext, ResectionPrompt

app = typer.Typer(help="Batch helpers for CAP DCIS resection prompts.")


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


@app.command()
def window(
    path: Path = typer.Argument(..., exists=True, readable=True, help="Input text file."),
    window_size: int = typer.Option(200, help="Number of tokens in each window."),
    overlap: int = typer.Option(20, help="Number of tokens shared between windows."),
) -> None:
    """Display overlapping windows for the provided text file."""

    content = _load_text(path)
    generator = ContextWindow(window_size=window_size, overlap=overlap)
    for index, chunk in enumerate(generator.generate(content), start=1):
        print({"index": index, "text": chunk})


@app.command()
def assemble(
    patient_id: str = typer.Option(..., help="Patient identifier."),
    history: str = typer.Option(..., help="Clinical history summary."),
    model_name: Optional[str] = typer.Option(None, help="Target model identifier."),
) -> None:
    """Create a prompt payload from CLI parameters."""

    context = PatientContext(patient_id=patient_id, clinical_history=history)
    prompt = ResectionPrompt(context=context, model_name=model_name or ResectionPrompt.DEFAULT_MODEL_NAME)
    print(prompt.to_prompt_dict())


if __name__ == "__main__":
    app()
