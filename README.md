# MC Twitch Sync
MC Twitch Sync - A service that can integrate twitch channel activities with the Minecraft server. For example: give access to the Minecraft server if the user got channel reward or subscribed to channel. This repository is some kind of example of how you can integrate activities of your twitch channel with the Minecraft server.

## Structure:
backend - Flask server + PubSub listener

frontend - Vue.js basic homepage for linking twitch account to Minecraft account

server_plugin - Source code of the very simple plugin for Minecraft server, which can integrate with Flask server.

rootfs - root directories, which will be posted to the docker containers.

## PubSub listener:
PubSub listener allows you to handle channel activities through WebSockets. For more details check: https://dev.twitch.tv/docs/pubsub

## Helper scripts:
deploy.sh - Deploy your backend and frontend to the remote server through ssh (docker required).

deploy_frontend.sh - Build frontend locally and copy dist to remote server and restart server.

deploy_lite.sh - Deliver backend code and restart the server.

logs.sh - Check logs of the remote server.
