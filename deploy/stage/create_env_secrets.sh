status_code=$(curl -X PUT --write-out %{http_code} --silent --output /dev/null -H "Content-Type: application/yaml" -H "Authorization: Bearer $K8S_TOKEN" --data-binary @env-secrets.yaml $K8S_URL/api/v1/namespaces/default/secrets/environment)

if [[ "$status_code" -eq 404 ]] ; then
  echo "Secret does not exist. Creating ..."
  curl -X POST -H "Content-Type: application/yaml" -H "Authorization: Bearer $K8S_TOKEN" --data-binary @env-secrets.yaml $K8S_URL/api/v1/namespaces/default/secrets
elif [[ "$status_code" -ne 200 ]] &&  [[ "$status_code" -ne 201 ]]; then
  echo "An error occured when creating secret"  # TODO echo response body
  exit 1
else
  echo "Secret created successfully"
  exit 0
fi
