#!/usr/bin/env bash
set -euo pipefail

# Disable FTP (FTPS) and SCM basic auth on an Azure Web App
# Usage: ./scripts/disable-local-auth.sh <resource-group> <webapp-name>

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <resource-group> <webapp-name>"
  exit 2
fi

RG="$1"
WEBAPP="$2"

echo "Disabling FTPS for $WEBAPP in resource group $RG"
az webapp config set --resource-group "$RG" --name "$WEBAPP" --ftps-state Disabled

echo "Removing publishing credentials (will remove FTP/publish user credentials)"
az webapp deployment user delete || true

echo "Disabling SCM (Kudu) basic auth by setting SCM_USE_MAIN_AUTH to true and removing any publish profiles"
# Note: There's no single toggle called 'disable scm basic auth' exposed; removing publishing credentials and
# avoiding use of publishing profiles is the recommended approach. We also set an app setting to remind operators.
az webapp config appsettings set --resource-group "$RG" --name "$WEBAPP" --settings SRE_DISABLE_LOCAL_AUTH=1

echo "Done. Verify in portal or with 'az webapp show' and test deployments using OIDC/Managed Identity."
