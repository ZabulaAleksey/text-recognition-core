# Воспроизводимость 2026-10-01

Исходный HEAD 17976d112b29927a225dd02c451eeabe3a7fcfc6, feature/trc-stage-01-foundation.
Восстановление старой migrated .venv выявило реальный lock gap: Hatchling editable build запрашивает editables~=0.3, отсутствующий в dev dependency graph. ADR-012 уточнён до изменения manifest. Добавлен только editables~=0.3 → 0.6 с hashes в uv.lock; другие версии не обновлены.

После двухступенчатого locked restore: 56 tests PASS, Ruff check/format PASS (22 files), strict mypy PASS (11 sources), uv lock --check --offline PASS, offline wheel/sdist build PASS. Единственное pytest warning — отказ записи .pytest_cache в restricted host, assertions прошли.
Свежая отдельная среда work/trc-clean-env: uv sync --locked --offline --no-install-project, затем uv sync --locked --offline --no-build-isolation и import text_recognition_core PASS; 20 dependencies + project. uv audit --locked: 20 packages, zero known vulnerabilities/adverse statuses.
Текущий фактический interpreter CPython 3.13.6; Python 3.13.7 в старой машинной записи исторический.

Stage 02 остаётся PARTIAL: signatures/hashes и три synthetic images не доказывают decoder isolation, representative corpus или accepted OCR adapter. Нет REST/backend E2E. Не активирован native parsing.

Повторение: используйте README two-step restore, затем uv run --locked pytest --basetemp <writable-directory>, uv run --locked ruff check src tests, uv run --locked ruff format --check src tests, uv run --locked mypy src, uv lock --check --offline и uv build --offline --no-build-isolation.
