# Runbook: execute remediation and validate deployment

This runbook contains step-by-step operator instructions to complete the remediation for `my-sre-app-rav` and validate deployments using the CI pipeline and smoke tests.

Prerequisites
-------------

- An operator account with Azure privileges to create service principals and edit App Service settings.
- Azure CLI installed and authenticated (e.g., `az login`).
- GitHub repository admin access to add repository secrets and edit workflows.

High-level steps
----------------

1. Create Service Principal (SP) with federated credential for GitHub Actions:

   a. Create the SP and scope it to the resource group `my-app-service-group` (least privilege):

   ```bash
   az ad app create --display-name "gh-actions-deployer-<repo>"
   az ad sp create --id <appId>
   az role assignment create --assignee <appId> --role Contributor --scope /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/my-app-service-group
   ```

   b. In Azure AD, open the App Registration for the SP and add a Federated Credential for GitHub Actions. Use the following values:

   - Issuer: `https://token.actions.githubusercontent.com`
   - Subject: `repo:<owner>/<repo>:ref:refs/heads/main` (adjust scope as needed)
   - Audience: the app's client id

2. Add GitHub repository secrets:

   - `AZURE_CLIENT_ID` — SP client id (appId)
   - `AZURE_TENANT_ID` — Azure tenant id
   - `AZURE_SUBSCRIPTION_ID` — subscription id
   - `APP_URL` — `https://my-sre-app-rav.azurewebsites.net` (used by smoke tests)

3. Validate GitHub Actions OIDC deployment:

   - Push a commit to `main` to trigger `.github/workflows/deploy.yml`.
   - Monitor Actions run and confirm `az webapp deploy` completes successfully.

4. Disable local auth (operator action):

   - From a trusted shell with `az` authenticated, run:

   ```bash
   chmod +x ./scripts/disable-local-auth.sh
   ./scripts/disable-local-auth.sh my-app-service-group my-sre-app-rav
   ```

   - Verify in the portal or via CLI that FTPS is Disabled and publish credentials are removed:

   ```bash
   az webapp show --resource-group my-app-service-group --name my-sre-app-rav --query "{ftpsState:ftpsState, publishingUser:publishingUser}" -o json
   ```

5. Run smoke tests:

   - Locally, or via Actions (smoke-test workflow), ensure `APP_URL` is set. Run:

   ```bash
   python -m pip install -r UnitTest/requirements.txt
   export APP_URL="https://my-sre-app-rav.azurewebsites.net"
   pytest -q
   ```

6. Rollback (if needed):

   - Re-enable FTPS temporarily:

   ```bash
   az webapp config set --resource-group my-app-service-group --name my-sre-app-rav --ftps-state AllAllowed
   ```

   - Recreate publishing credentials if required (prefer temporary use only).

Post-run validation and monitoring
---------------------------------

- Monitor Azure Activity Logs and App Service authentication logs for any failed access attempts.
- Confirm deployment logs and smoke tests pass for at least 48 hours before considering the change permanent.

Contact and escalation
----------------------

- SRE Team: `sre-team@example.com`
- On-call: follow standard escalation policy
