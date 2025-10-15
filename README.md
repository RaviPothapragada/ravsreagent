# ravsreagent
rav sre agent 

## Deployment pipeline (GitHub Actions) and disabling local auth

This repository includes a GitHub Actions workflow that deploys to an Azure Web App using GitHub OIDC (no long-lived secrets required in the repo).

Files added:

- `.github/workflows/deploy.yml` — pipeline that logs in to Azure using OIDC and runs `az webapp deploy`.
- `scripts/disable-local-auth.sh` — helper script to disable FTPS and remove publish credentials.

Prerequisites

- A GitHub repository connected to this code.
- Create a Service Principal in Azure and add a federated credential for the GitHub Actions OIDC provider. Store the SP's client id in `AZURE_CLIENT_ID` and the tenant and subscription ids in GitHub secrets `AZURE_TENANT_ID` and `AZURE_SUBSCRIPTION_ID`.

Quick setup (outline)

1. Create a service principal and grant it Contributor (or least privilege) on the target resource group:

```bash
az ad sp create-for-rbac --name "github-actions-deployer-$(date +%s)" --role contributor --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/my-app-service-group
```

2. In Azure AD, add a federated identity credential to the service principal for GitHub Actions (see Microsoft docs for exact steps). Use the repo and branch filters that match this repository.

3. Add the following GitHub secrets to your repository settings:

- `AZURE_CLIENT_ID` — client id (appId) of the service principal with federated credential
- `AZURE_TENANT_ID` — your Azure tenant id
- `AZURE_SUBSCRIPTION_ID` — subscription id where the App Service lives

4. Commit and push to `main`. The workflow will run and deploy.

Disabling local auth (run once, from a trusted machine with az-cli logged in):

```bash
./scripts/disable-local-auth.sh my-app-service-group my-sre-app-rav
```

Testing and rollback

- After disabling local auth, test CI/CD deployments using the workflow. If deployment fails, you can re-enable ftps or restore publishing credentials from Azure Portal or by reversing the commands.

Security notes

- Remove any publish profiles stored in CI system variables or repo secrets.
- Ensure the service principal is constrained with federated credential filters and least privilege.
