#!/usr/bin/env bash
source PROD_CONF

echo 'Syncing files...'
rsync -a --exclude=node_modules --exclude=mc_server ./ $HOST_NAME@$HOST_ADDR:$HOST_PROJECT_DIR
echo 'Stop start container...'
ssh $HOST_NAME@$HOST_ADDR /bin/bash << EOF
cd $HOST_PROJECT_DIR;
cp -f ./$PRODUCTION_ENV_FILE ./.env;
docker-compose -f $DOCKER_COMPOSE_FILE stop;
docker-compose -f $DOCKER_COMPOSE_FILE up -d --force-recreate;
cp $HOST_PROJECT_DIR/$PLUGIN_PATH $MINECRAFT_SERVER_PLUGIN_PATH
EOF
