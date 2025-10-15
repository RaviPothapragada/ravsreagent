---
title: "Add pytest smoke tests"
status: completed
labels: [tests]
---

Summary
-------

Added smoke tests under `UnitTest/`:

- `test_smoke.py` — basic root path smoke test, skips if `APP_URL` not set.
- `test_health.py` — health endpoint test, configurable via `HEALTH_PATH` and `HEALTH_EXPECT`.
- `requirements.txt` — lists `pytest` and `requests`.

Acceptance criteria
-------------------
- Tests run locally and skip when `APP_URL` is not set.
- CI workflow can run tests when `APP_URL` is provided via secrets.

Completion notes
----------------
Tests added and executed locally (skipped because APP_URL not set). Added an optional smoke-test workflow in `.github/workflows/smoke-test.yml`.

Checklist
---------

- [x] Tests added to `UnitTest/`
- [x] `requirements.txt` included
- [ ] Add `APP_URL` secret to CI for running tests
- [ ] Add post-deploy smoke test to `deploy.yml` (recommended)
