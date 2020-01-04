package com.dmitrygulak.twitch_mc_sync.twitch_mc_sync;

import com.google.gson.Gson;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.net.URISyntaxException;
import java.util.UUID;
import java.util.logging.Logger;

class TwitchSyncIsAllowedResponse {
    Boolean is_allowed;
    String message;
}

public class TwitchSyncClient {
    public TwitchSyncIsAllowedResponse isUserAllowed(String host, String token, String username, UUID uuid) throws IOException, URISyntaxException {
        URIBuilder builder = new URIBuilder(host);
        builder.setPath("/api/v1/is_allowed");
        builder.setParameter("username", username)
                .setParameter("uuid", uuid.toString())
                .setParameter("token", token);
        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpGet httpGet = new HttpGet(builder.build());
        HttpResponse httpResponse = httpClient.execute(httpGet);
        String response = EntityUtils.toString(httpResponse.getEntity());

        Gson gson = new Gson();
        return gson.fromJson(response, TwitchSyncIsAllowedResponse.class);
    }
}
