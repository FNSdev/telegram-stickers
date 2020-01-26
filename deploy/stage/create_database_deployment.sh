status_code=$(curl -X PUT --write-out %{http_code} --silent --output /dev/null -H "Content-Type: application/yaml" -H "Authorization: Bearer $K8S_TOKEN" --data-binary @deploy/stage/kubernetes/database-deployment.yaml $K8S_URL/apis/apps//v1/namespaces/default/deployments/database-deployment)

if [[ "$status_code" -eq 404 ]] ; then
  echo "Deployment does not exist. Creating ..."
elif [[ "$status_code" -ne 200 ]] &&  [[ "$status_code" -ne 201 ]] ; then
  echo "An error occured when updating database-deployment"  # TODO echo response body
  exit 1
else
  echo "Deployment updated successfully"
  exit 0
fi

status_code=$(curl -X POST --write-out %{http_code} --silent --output /dev/null -H "Content-Type: application/yaml" -H "Authorization: Bearer $K8S_TOKEN" --data-binary @deploy/stage/kubernetes/database-deployment.yaml $K8S_URL/apis/apps/v1/namespaces/default/deployments)

if [[ "$status_code" -ne 200 ]] &&  [[ "$status_code" -ne 201 ]] ; then
  echo "An error occured when creating database-deployment"  # TODO echo response body
  exit 2
else
  echo "Deployment created successfully"
  exit 0
fi
