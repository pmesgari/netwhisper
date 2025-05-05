#!/bin/bash

set -e

# ===========================
# NetWhisper VM Manager
# ===========================

# Configuration
RESOURCE_GROUP="rg-netwhisper"
LOCATION="northeurope"
VM_NAME="vm-netwhisper"
IMAGE="Ubuntu2204"
SIZE="Standard_D4s_v3"
ADMIN_USERNAME="azureuser"
SSH_KEY_PATH="$HOME/.ssh/id_rsa.pub"

ACTION=$1

# Function to display usage
usage() {
  echo "Usage: $0 [create|delete]"
  exit 1
}

# Check action argument
if [[ -z "$ACTION" ]]; then
  usage
fi

# Create resources
if [[ "$ACTION" == "create" ]]; then
  echo "🚀 NetWhisper: Creating VM and resources..."

  az group create --name $RESOURCE_GROUP --location $LOCATION

  az vm create \
    --resource-group $RESOURCE_GROUP \
    --name $VM_NAME \
    --image $IMAGE \
    --size $SIZE \
    --admin-username $ADMIN_USERNAME \
    --ssh-key-values $SSH_KEY_PATH \
    --generate-ssh-keys \
    --output json

  PUBLIC_IP=$(az vm show \
    --resource-group $RESOURCE_GROUP \
    --name $VM_NAME \
    --show-details \
    --query "publicIps" \
    --output tsv)

  echo "✅ VM created. Public IP: $PUBLIC_IP"
  echo "💡 Connect using: ssh $ADMIN_USERNAME@$PUBLIC_IP"

# Delete resources
elif [[ "$ACTION" == "delete" ]]; then
  echo "🧨 NetWhisper: Deleting all resources..."
  az group delete --name $RESOURCE_GROUP --yes --no-wait
  echo "🗑️  Deletion initiated for resource group '$RESOURCE_GROUP'."

else
  echo "❌ Invalid action: $ACTION"
  usage
fi
