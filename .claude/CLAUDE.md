# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Spendly is a Flask-based expense tracker built as a step-by-step teaching project (package name `expense-tracker`). The repo is intentionally in an early, partially-scaffolded state: some modules are placeholder stubs with comments describing what students/future work should implement there, and several routes return plain placeholder strings rather than real views. Don't "complete" these stubs unless the user asks — check `database/db.py` and the placeholder routes in `app.py` before assuming something is unimplemented by accident.

## Commands

This project uses `uv` for dependency management (there's a `uv.lock`).

- Install dependencies: `uv sync`
- Run the app: `uv run python app.py` (serves on `http://localhost:5001` with `debug=True`)
- Run tests: `uv run pytest`
- Run a single test: `uv run pytest path/to/test_file.py::test_name`

`requirements.txt` and `pyproject.toml` are kept in sync manually; both list `flask`, `werkzeug`, `pytest`, `pytest-flask`, and `fastapi[standard]` (FastAPI is a listed dependency but the app itself is Flask — there's no FastAPI code yet).

`main.py` is an unrelated `uv init` placeholder entry point, not part of the Flask app.

## Architecture

- **`app.py`** — single Flask application module; all routes are registered directly on the module-level `app` object (no blueprints). Routes fall into two groups:
  - Implemented: `/`, `/register`, `/login`, `/terms`, `/privacy` — render Jinja templates from `templates/`.
  - Placeholder (return a plain string, no real logic yet): `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`.
- **`database/db.py`** — currently an empty stub. Per its header comment, this file is meant to hold `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (creates tables with `CREATE TABLE IF NOT EXISTS`), and `seed_db()` (sample data for development). No DB layer exists yet — `app.py` does not import from `database` currently.
- **`templates/`** — Jinja2 templates, all extending `base.html`, which defines the shared `<head>`, navbar, footer, and `{% block content %}` region. Google Fonts (`DM Serif Display`, `DM Sans`) are loaded in `base.html`.
- **`static/css/`** — `style.css` holds shared/base styles used across pages; `landing.css` holds styles specific to the landing page. Follow this split when adding page-specific styles rather than growing `style.css` further.
- **`static/js/main.js`** — currently minimal/placeholder.

## Conventions observed in existing code

- Routes use plain string paths and Flask's default `render_template`; no forms library or CSRF protection wired in yet (see the raw `<form method="POST">` in `register.html`/`login.html`).
- `app.py` groups routes under `# ---- #` banner comments separating "Routes" (implemented) from "Placeholder routes — students will implement these". Preserve this separation when adding new routes.
