import requests


def search_minecraft_profile(nickname):
    response = requests.get(
        f'https://api.mojang.com/users/profiles/minecraft/{nickname}')
    response.raise_for_status()
    return response.json()
