---
title: "Add pytest.ini to register smoke mark"
status: completed
labels: [tests, config]
---

Summary
-------

Added `pytest.ini` at the repository root to register the `smoke` pytest mark and silence PytestUnknownMarkWarning warnings.

Acceptance criteria
-------------------
- `pytest.ini` exists and contains registration for the `smoke` mark.
- Running `pytest` locally no longer emits UnknownMark warnings.

Completion notes
----------------
`pytest.ini` added and pytest run locally showed no warnings; tests skipped as expected due to missing `APP_URL`.

Checklist
---------

- [x] `pytest.ini` added to repo
- [x] Pytest warnings resolved locally
