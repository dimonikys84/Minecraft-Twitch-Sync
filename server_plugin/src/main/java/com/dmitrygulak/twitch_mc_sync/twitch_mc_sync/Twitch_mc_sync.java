package com.dmitrygulak.twitch_mc_sync.twitch_mc_sync;

import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.plugin.java.JavaPlugin;

public final class Twitch_mc_sync extends JavaPlugin {
    FileConfiguration config = getConfig();

    public String syncServerHost;
    public String syncServerToken;

    @Override
    public void onEnable() {
        config.addDefault("syncServerHost", "http://localhost:8000");
        config.addDefault("syncServerToken", "test");
        config.options().copyDefaults(true);
        saveConfig();

        syncServerHost = config.getString("syncServerHost");
        syncServerToken = config.getString("syncServerToken");

        EventListener.initialize(config);
        EventListener eventListener = new EventListener();

        // Plugin startup logic
        getServer().getPluginManager().registerEvents(eventListener, this);
    }

    @Override
    public void onDisable() {
        // Plugin shutdown logic
    }
}
