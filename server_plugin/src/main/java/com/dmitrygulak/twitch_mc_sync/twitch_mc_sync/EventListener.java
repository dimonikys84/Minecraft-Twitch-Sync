package com.dmitrygulak.twitch_mc_sync.twitch_mc_sync;

import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.event.EventHandler;
import org.bukkit.event.player.AsyncPlayerPreLoginEvent;
import org.bukkit.event.Listener;

import java.io.IOException;
import java.net.URISyntaxException;
import java.util.logging.Logger;

public class EventListener implements Listener {
    private Logger log = Logger.getLogger("Minecraft");
    private static FileConfiguration config;

    public static void initialize(FileConfiguration configuration) {
        config = configuration;
    }

    @EventHandler
    public void onAsyncPlayerPreLoginEvent(AsyncPlayerPreLoginEvent event) throws IOException, URISyntaxException {
        TwitchSyncIsAllowedResponse response = new TwitchSyncIsAllowedResponse();
        TwitchSyncClient syncClient = new TwitchSyncClient();

        String syncServerHost = config.getString("syncServerHost");
        String syncServerToken = config.getString("syncServerToken");

        if (event.getLoginResult() == AsyncPlayerPreLoginEvent.Result.ALLOWED) {
            event.allow();
        }

        try {
            response = syncClient.isUserAllowed(syncServerHost, syncServerToken, event.getName(), event.getUniqueId());
        } catch (Exception e) {
            log.info("Got exepction while connecting to syncServer: " + e.toString());
            event.disallow(AsyncPlayerPreLoginEvent.Result.KICK_OTHER, "Failed to verify player");
        }

        log.info("Is allowed: " + response.is_allowed.toString());
        log.info("Message: " + response.message);

        if (!response.is_allowed) {
            event.disallow(AsyncPlayerPreLoginEvent.Result.KICK_OTHER, response.message);
            return;
        }

        event.allow();
        return;
    }
}
