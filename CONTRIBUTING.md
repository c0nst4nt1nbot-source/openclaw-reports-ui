# Contributing

Thanks for considering a contribution. This project is deliberately small and
dependency-light, and it should stay that way.

## Ground rules

1. **Keep it read-only.** No endpoint may write to the SQLite database or to the
   filesystem. New database access must go through `modules/db_browser.py` so the
   read-only connection and identifier validation apply.
2. **No new runtime dependencies without discussion.** Flask, Markdown and Pygments
   are the whole stack; the frontend uses inline CSS/JS with no CDN or build step.
3. **Parameterize, never interpolate.** Table/column identifiers must be validated
   against the live schema (see `_validate_table_name` / `_quote_identifier`);
   values must be bound parameters.
4. **No hardcoded personal paths.** Use the `OPENCLAW_REPORTS_DIR` /
   `OPENCLAW_DB_PATH` environment variables. Defaults may exist for convenience but
   must be overridable.
5. **Do not commit data or secrets.** Reports, databases, `venv/`, and any
   credentials stay out of the repo (see `.gitignore`).

## Development setup

```bash
git clone <this-repo-url>
cd openclaw-reports-ui
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENCLAW_REPORTS_DIR=/path/to/reports
export OPENCLAW_DB_PATH=/path/to/reports/intelligence.db
python app.py
```

Use a scratch copy of any database while developing — the app opens it read-only,
but keeping a disposable copy avoids surprising anyone relying on the live file.

## Before opening a pull request

- [ ] App starts and `/`, `/reports`, `/database`, `/database/<table>` and
      `/database/query` all render against a real reports directory.
- [ ] No secrets, tokens, report content, or database files are included.
- [ ] New config is environment-driven and documented in `README.md` and
      `.env.example`.
- [ ] Security invariants above still hold.
- [ ] `CHANGELOG.md` updated for user-visible changes.

## High-value first contributions

- Add a test suite (pytest) covering the indexer, the Markdown renderer, and the
  database validation helpers, plus a minimal CI workflow.
- Replace the per-request full directory scan with a cached index invalidated by
  mtime, and bound the content cache.
- Add SQLite FTS5-backed content search.
- Clamp `page` / `per_page` and validate them defensively.
- Improve report-type classification (currently filename/path substring matching).

## Reporting issues

Include the Python version, the versions from `requirements.txt`, how the app is
launched (env vars, host/port), and the exact error text. Do not paste report
contents or database rows that you are not free to share.
