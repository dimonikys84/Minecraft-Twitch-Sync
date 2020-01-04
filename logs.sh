#!/usr/bin/env bash
source PROD_CONF

ssh $HOST_NAME@$HOST_ADDR /bin/bash << EOF
cd $HOST_PROJECT_DIR;
docker-compose logs --tail=1000 -f
EOF
