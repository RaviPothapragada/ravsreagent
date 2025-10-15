---
title: "Update README with pipeline and disable-local-auth guidance"
status: completed
labels: [docs]
---

Summary
-------

Updated top-level `README.md` to include setup steps for the GitHub Actions workflow, required GitHub secrets, instructions to run the `disable-local-auth.sh` script, and validation/rollback guidance.

Acceptance criteria
-------------------
- `README.md` contains instructions for creating a service principal and adding a federated credential.
- Shows required GitHub secrets and example CLI commands for disabling local auth.

Completion notes
----------------
README updated and committed. See `docs/README.md` for the full detailed documentation.

Checklist
---------

- [x] README updated with pipeline and script usage
- [x] `docs/README.md` added with full explanations
- [ ] Share instructions with operators and confirm understanding
