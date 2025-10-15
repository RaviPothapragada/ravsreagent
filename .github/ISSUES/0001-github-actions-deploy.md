---
title: "Add GitHub Actions OIDC-based deploy workflow"
status: completed
labels: [pipeline, security]
---

Summary
-------

Added `.github/workflows/deploy.yml` which authenticates to Azure using GitHub OIDC (`azure/login@v2`) and deploys the repository to the App Service `my-sre-app-rav` using `az webapp deploy`.

Acceptance criteria
-------------------
- Workflow file exists at `.github/workflows/deploy.yml`.
- Uses OIDC (`id-token: write` permission and `azure/login` with `enable-oidc: true`).
- Does not rely on publish profiles or stored Azure secrets in the repository.
- Deploys successfully when correct GitHub secrets and federated credential are configured.

Completion notes
----------------
Workflow added and committed. Manual validation: instruct operators to create the service principal and federated credential and add the required GitHub secrets before running.

Checklist
---------

- [x] Workflow file committed
- [ ] Service Principal created with federated credential
- [ ] GitHub secrets added
- [ ] Deploy from `main` succeeds without publish profile
