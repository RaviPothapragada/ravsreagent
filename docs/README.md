# ravsreagent — Documentation

This document describes the repository structure, the deployment pipeline, helper scripts, and tests added to remediate local authentication on an Azure App Service and to provide secure CI/CD using GitHub OIDC.

## Purpose

The repository demonstrates a secure deployment pipeline for an Azure App Service (`my-sre-app-rav`) and includes tools to disable unsafe local authentication methods (FTP and publish profile credentials). It also includes smoke tests to validate the running application.

## Repository layout

- `.github/workflows/deploy.yml` — GitHub Actions workflow that uses GitHub OIDC and `azure/login` to authenticate to Azure and deploy the code using `az webapp deploy`.
- `.github/workflows/smoke-test.yml` — Optional workflow to run smoke tests (can be dispatched manually or run on push to main).
- `scripts/disable-local-auth.sh` — Helper script to disable FTPS and remove publishing credentials.
- `UnitTest/` — Smoke tests using pytest.
  - `test_smoke.py` — Basic root path smoke test. Skips if `APP_URL` not set.
  - `test_health.py` — Health endpoint test. Configurable via `HEALTH_PATH` and `HEALTH_EXPECT` environment variables.
  - `requirements.txt` — Python package requirements for tests (`pytest`, `requests`).
- `README.md` — High-level setup and usage instructions (updated).
- `docs/README.md` — This file.

## Deployment pipeline (details)

The `deploy.yml` workflow does the following:

1. Checkout code.
2. Log in to Azure using `azure/login@v2` with OIDC. This requires:
   - A Service Principal (app registration) with a federated credential for GitHub Actions.
   - GitHub secrets set: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`.
3. Package the repository into a zip file and run `az webapp deploy --src-path app.zip` to deploy.

Notes:
- The workflow intentionally avoids storing long-lived Azure secrets in the repository.
- The Service Principal's federated credential should be scoped to the repository and branch to limit the blast radius.

## Disabling local auth

Use the `scripts/disable-local-auth.sh` script to disable FTPS and remove publish credentials. Run it from a trusted machine where you are signed in with Azure CLI:

```bash
chmod +x ./scripts/disable-local-auth.sh
./scripts/disable-local-auth.sh my-app-service-group my-sre-app-rav
```

What the script does:
- Sets FTPS state to Disabled for the given web app.
- Removes publishing credentials via `az webapp deployment user delete`.
- Adds an app setting `SRE_DISABLE_LOCAL_AUTH=1` as an indicator.

Rollback: Re-enable FTPS using `az webapp config set --ftps-state AllAllowed` and restore publish credentials if necessary (manual steps in portal or recreate credentials).

## Tests and smoke checks

Tests live in `UnitTest/` and use `pytest` + `requests`.

Environment variables used by tests:
- `APP_URL` — base URL of the deployed app (e.g., `https://my-sre-app-rav.azurewebsites.net`). Required for tests; if not set, tests will skip.
- `HEALTH_PATH` — optional path to the health endpoint, default `/health`.
- `HEALTH_EXPECT` — optional substring to verify in the health endpoint response body.

Run tests locally:

```bash
python -m pip install -r UnitTest/requirements.txt
export APP_URL="https://my-sre-app-rav.azurewebsites.net"
pytest -q
```

CI: Set `APP_URL` as a repository secret or provide it in the workflow environment.

## CI tips and improvements

- Add a post-deploy job to `deploy.yml` that runs smoke tests after a successful deployment. That ensures the newly deployed app is healthy before merging.
- Add least-privilege RBAC assignments for the service principal (scope to the resource group or specific App Service).
- Implement feature-flagged rollbacks or slot swaps for zero-downtime deployments.

## Next steps and maintenance

- Replace the generic `az webapp deploy` with runtime-specific build steps (Node/Python/.NET) if you want build artifacts created in CI.
- Add monitoring/alerts for failed deployments and authentication anomalies.
- Rotate the service principal or re-issue federated credentials periodically.

## Questions

If you'd like, I can:

- Add a `pytest.ini` to register pytest marks and silence warnings (I will add it here by default),
- Wire smoke tests into the deploy workflow, or
- Create an Azure CLI script to create the service principal and federated credential template.
