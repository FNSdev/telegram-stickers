status_code=$(curl -X PATCH --write-out %{http_code} --silent --output /dev/null \
  -H "Content-Type: strategic-merge-patch+json" -H "Authorization: Bearer $K8S_TOKEN" \
  --data {"spec":{"template":{"spec":{"containers":[{"name":"telegram-stickers","image":"fnsdev/telegram-stickers-stage:$RELEASE_VERSION"}]}}}} \
  $K8S_URL/apis/apps/v1/namespaces/default/deployments/telegram-stickers-deployment)

if [[ "$status_code" -ne 200 ]] &&  [[ "$status_code" -ne 201 ]] ; then
  echo "An error occured when updating telegram_stickers_deployment"  # TODO echo response body
  exit 1
else
  echo "telegram_stickers_deployment updated successfully"
  exit 0
fi
