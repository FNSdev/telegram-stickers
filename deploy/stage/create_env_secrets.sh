status_code=$(curl -X PUT --write-out %{http_code} --silent --output /dev/null -H "Content-Type: application/yaml" -H "Authorization: Bearer $K8S_TOKEN" --data-binary @env-secrets.yaml $K8S_URL/api/v1/namespaces/default/secrets/environment)

if [[ "$status_code" -eq 404 ]] ; then
  echo "Secret does not exist. Creating ..."
elif [[ "$status_code" -ne 200 ]] &&  [[ "$status_code" -ne 201 ]] ; then
  echo "An error occured when updating environment secret"  # TODO echo response body
  exit 1
else
  echo "Secret updated successfully"
  exit 0
fi

status_code=$(curl -X POST --write-out %{http_code} --silent --output /dev/null -H "Content-Type: application/yaml" -H "Authorization: Bearer $K8S_TOKEN" --data-binary @env-secrets.yaml $K8S_URL/api/v1/namespaces/default/secrets)

if [[ "$status_code" -ne 200 ]] &&  [[ "$status_code" -ne 201 ]] ; then
  echo "An error occured when creating environment secret"  # TODO echo response body
  exit 2
else
  echo "Secret created successfully"
  exit 0
fi
