status_code=$(curl -X PUT --write-out %{http_code} --silent --output /dev/null -H "Content-Type: application/yaml" -H "Authorization: Bearer $K8S_TOKEN" --data-binary @deploy/stage/kubernetes/database-service.yaml $K8S_URL/api/v1/namespaces/default/services/database-service)

if [[ "$status_code" -eq 404 ]] ; then
  echo "Service does not exist. Creating ..."
elif [[ "$status_code" -ne 200 ]] &&  [[ "$status_code" -ne 201 ]] ; then
  echo "An error occured when updating database-service"  # TODO echo response body
  exit 1
else
  echo "Service updated successfully"
  exit 0
fi

status_code=$(curl -X POST --write-out %{http_code} --silent --output /dev/null -H "Content-Type: application/yaml" -H "Authorization: Bearer $K8S_TOKEN" --data-binary @deploy/stage/kubernetes/database-service.yaml $K8S_URL/api/v1/namespaces/default/services)

if [[ "$status_code" -ne 200 ]] &&  [[ "$status_code" -ne 201 ]] ; then
  echo "An error occured when creating database-service"  # TODO echo response body
  exit 2
else
  echo "Service created successfully"
  exit 0
fi
