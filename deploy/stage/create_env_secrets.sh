status_code=$(curl -X PUT --write-out %{http_code} --silent --output /dev/null -H "Content-Type: application/yaml" -H "Authorization: Bearer $K8S_TOKEN" --data-binary @env-secrets.yaml $K8S_URL/api/v1/namespaces/default/secrets/environment)

if [[ "$status_code" e 404 ]] ; then
  curl -X POST -H "Content-Type: application/yaml" -H "Authorization: Bearer $K8S_TOKEN" --data-binary @env-secrets.yaml $K8S_URL/api/v1/namespaces/default/secrets
else
  exit 0
fi
