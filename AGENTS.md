# Repository Guidelines

## Project Structure & Module Organization

This repository contains a small full-stack RAG application. Backend code lives in `backend/` and is served by FastAPI from `backend/app.py`. Core RAG behavior is split across `rag_system.py`, `vector_store.py`, `document_processor.py`, `ai_generator.py`, and `session_manager.py`. Shared models are in `backend/models.py`; runtime settings are in `backend/config.py`.

The static UI lives in `frontend/` with `index.html`, `style.css`, and `script.js`. Course materials are plain text files in `docs/`. Root files include `pyproject.toml`, `uv.lock`, `.env.example`, and `run.sh`.

## Build, Test, and Development Commands

- `uv sync --dev`: install the Python 3.13 dependencies and test tools pinned in `uv.lock`.
- `cp .env.example .env`: create local configuration, then set `ZAI_API_KEY`.
- `./run.sh`: start the app from the repository root using the provided script.
- `cd backend && uv run uvicorn app:app --reload --port 8000`: manually start the FastAPI server with reload.

The web interface is available at `http://localhost:8000`; API docs are at `http://localhost:8000/docs`.

## Coding Style & Naming Conventions

Use `snake_case` Python filenames and functions. Keep classes in `PascalCase`, matching `RAGSystem` and `QueryRequest`. Prefer type hints for request/response boundaries and small, focused modules. Follow the existing 4-space indentation style.

Frontend files are plain HTML, CSS, and JavaScript. Keep UI behavior in `frontend/script.js`, styling in `frontend/style.css`, and avoid new build tooling unless clearly needed.

## Testing Guidelines

Tests live under `tests/` and use `pytest`. Add tests when changing behavior, especially document parsing, search, sessions, or API responses. Name files `test_<module>.py` and run:

```bash
uv run pytest
```

For API changes, also verify the relevant endpoint through `/docs` or an HTTP client.

## Commit & Pull Request Guidelines

The current Git history uses short subjects such as `added lab files` and `updated lab files`. Continue using concise summaries that describe the changed area.

Pull requests should include purpose, main files changed, manual test results, and screenshots for visible frontend changes. Link related issues when available. Do not commit `.env`, API keys, caches, or local database artifacts.

## Security & Configuration Tips

Keep secrets only in `.env`; `.env.example` should contain names, not real values. Review new `docs/` materials before committing them. Avoid logging full user queries or model responses if they may contain sensitive data.
