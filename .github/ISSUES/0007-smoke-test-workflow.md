---
title: "Add smoke-test GitHub Actions workflow"
status: completed
labels: [ci, tests]
---

Summary
-------

Added `.github/workflows/smoke-test.yml` which installs test dependencies and runs the pytest smoke tests. The workflow accepts `APP_URL` from repository secrets.

Acceptance criteria
-------------------
- Workflow file present at `.github/workflows/smoke-test.yml`.
- Installs `pytest` and `requests` and runs `pytest -m smoke UnitTest`.
- CI job reads `APP_URL` from `secrets.APP_URL` when available.

Completion notes
----------------
Workflow added. Note: ensure `APP_URL` secret exists in repo settings before running to avoid failures.

Checklist
---------

- [x] Workflow file added
- [ ] Add `APP_URL` secret to repo settings
- [ ] Optionally wire this workflow as a post-deploy check in `deploy.yml`
