---
title: "Add helper script to disable FTPS and publishing credentials"
status: completed
labels: [scripts, security]
---

Summary
-------

Added `scripts/disable-local-auth.sh` to disable FTPS and remove publishing credentials for an App Service. The script takes `<resource-group>` and `<webapp-name>` as arguments.

Acceptance criteria
-------------------
- Script exists and is executable.
- When run with valid arguments, it sets FTPS state to `Disabled` and attempts to remove publishing credentials.
- Adds an app setting `SRE_DISABLE_LOCAL_AUTH=1` as an indicator.

Completion notes
----------------
Script added. Operators must run it from a trusted environment with Azure CLI authenticated. The script documents usage in the README.

Checklist
---------

- [x] Script exists in `scripts/disable-local-auth.sh`
- [ ] Run script in a trusted operator environment
- [ ] Confirm FTPS is disabled in Azure Portal or via `az webapp show`
- [ ] Confirm publishing credentials are removed
