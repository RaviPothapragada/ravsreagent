---
title: "Remediate unsafe local authentication on my-sre-app-rav (main issue)"
status: completed
labels: [security, remediation, sre]
---

Resource
--------

- Resource Name: `my-sre-app-rav`
- Location: `australiaeast`
- Resource ID: `/subscriptions/425dbe7c-a593-4c8a-9912-f7f0fc5bfa99/resourcegroups/my-app-service-group/providers/microsoft.web/sites/my-sre-app-rav`
- Service Type: `Microsoft.Web/sites` (App Service)

Original security risk
----------------------

Local/key-based authentication (FTP basic auth, SCM/Kudu basic auth, publish profiles) exposes long-lived secrets that can be leaked or reused. The remediation plan was to remove local auth surfaces and move deployments to identity-based methods (GitHub OIDC / Managed Identity).

Work performed in this repository (summary)
----------------------------------------

All changes were implemented in the repository to provide a secure pipeline and the tools/operators need to complete the live migration. No destructive changes were executed against Azure resources from this environment — the repository contains scripts and CI changes to do so when operators run them in a trusted environment.

Files added and purpose
----------------------

- `.github/workflows/deploy.yml` — GitHub Actions workflow to deploy using GitHub OIDC and `azure/login` (no publish-profile secrets required).
- `scripts/disable-local-auth.sh` — helper script that will disable FTPS and remove publishing credentials when run with Azure CLI authenticated credentials.
- `.github/workflows/smoke-test.yml` — optional workflow to run smoke tests (requires `APP_URL` secret set in repo settings).
- `UnitTest/test_smoke.py` — basic smoke test that checks the root path. Skips if `APP_URL` not set.
- `UnitTest/test_health.py` — configurable health endpoint smoke test (`HEALTH_PATH`, `HEALTH_EXPECT`). Skips if `APP_URL` not set.
- `UnitTest/requirements.txt` — pytest + requests for smoke tests.
- `pytest.ini` — registers the `smoke` pytest mark to silence warnings.
- `docs/README.md` — full documentation describing the repository, CI, scripts, tests, and next steps.
- `.github/ISSUES/0001-0007-*.md` — child-issue markdown files summarizing each change and marking them completed.

Testing and validation performed
------------------------------

- Ran the local pytest suite in this environment. Results:
  - 2 tests skipped (because `APP_URL` was not set).
  - No unknown-mark warnings after adding `pytest.ini`.
- The smoke-test workflow file exists but was not executed here (would run in GitHub Actions with `APP_URL` secret configured).

Elapsed time for repository changes (start -> finish)
--------------------------------------------------

- Earliest file creation: `.github/workflows/deploy.yml` at 2025-10-15T17:38:45Z
- Latest file creation: `.github/ISSUES/0007-smoke-test-workflow.md` at 2025-10-15T17:46:19Z
- Total elapsed wall-clock time: 454 seconds (0:07:34)

Acceptance criteria (repository-level)
-------------------------------------

1. All files above exist in the repository (workflows, scripts, tests, docs).
2. Tests run locally and skip when `APP_URL` is not present.
3. CI workflows are configured to use OIDC and not to rely on repository secrets for Azure credentials (service principal with federated credential required and `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID` secrets expected).

Results vs operational acceptance criteria
---------------------------------------

- Repository acceptance criteria: met. All files are present and tested locally (skips).
- Operational acceptance criteria (live Azure config): NOT automatically applied by these commits. The following manual/operator steps remain and must be completed in a trusted environment with appropriate permissions:
  - Create a service principal, add a federated credential for GitHub Actions, and store `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID` as repository secrets.
  - Run `./scripts/disable-local-auth.sh my-app-service-group my-sre-app-rav` from a machine with `az` authenticated to disable FTPS and remove publishing credentials, or perform equivalent actions in the Azure Portal.
  - Validate deployments by pushing to `main` (workflow will run) and/or running the smoke-test workflow (ensure `APP_URL` secret is set).

Links to child issue records in this repo
---------------------------------------

- `.github/ISSUES/0001-github-actions-deploy.md`
- `.github/ISSUES/0002-disable-local-auth-script.md`
- `.github/ISSUES/0003-readme-update.md`
- `.github/ISSUES/0004-smoke-tests.md`
- `.github/ISSUES/0005-pytest-config.md`
- `.github/ISSUES/0006-docs-readme.md`
- `.github/ISSUES/0007-smoke-test-workflow.md`

Next steps (recommended)
------------------------

1. Create the service principal and add a federated identity credential in Azure AD scoped to this repo/branch.
2. Add the required GitHub secrets in repository settings.
3. Run the `disable-local-auth.sh` script from a trusted operator shell to actually disable FTPS and remove publish credentials.
4. Run the `smoke-test` workflow or the post-deploy smoke step to validate the live app.
5. Monitor authentication logs and CI logs after cutover.

Completion note
---------------
This main issue consolidates the work performed in the repository and the child-issue summaries. The repository-level remediation artifacts are complete; operational execution requires an operator with Azure permissions to run the scripts and configure federated credentials.

Checklist
---------

- [x] Repository artifacts added (workflows, scripts, tests, docs)
- [ ] Create Service Principal and add federated credential in Azure AD
- [ ] Add GitHub secrets: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`
- [ ] Run `./scripts/disable-local-auth.sh my-app-service-group my-sre-app-rav` from a trusted operator shell
- [ ] Validate deployments via `main` push and smoke tests
- [ ] Monitor logs and confirm no unintended access
