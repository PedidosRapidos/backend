#!/bin/bash

set -x

HEROKU_APP=$1
IMAGE_DOCKER_ID=$2
HEROKU_API_KEY=$3

echo $HEROKU_APP $IMAGE_ID

curl --netrc -X PATCH https://api.heroku.com/apps/$HEROKU_APP/formation \
  -d '{
  "updates": [
    {
      "type": "web",
      "docker_image": "'${IMAGE_DOCKER_ID}'"
    }
  ]
}' \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
  -H "Authorization: Bearer ${HEROKU_API_KEY}"