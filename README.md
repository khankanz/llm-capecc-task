# cap_dcis_resection

Utilities and runners for assembling CAP-compliant DCIS resection pathology prompts with Python.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -c "import cap_dcis_resection"
pytest
```

The package also exposes CLI helpers via `cap-dcis-batch` and an ASGI app via `cap-dcis-serve` once installed.
