# spotify_api.py
import requests

def get_spotify_token(CLIENT_ID, CLIENT_SECRET):
    auth_response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={'grant_type': 'client_credentials'},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    return auth_response.json().get('access_token')

def get_episode_preview_url(episode_url, access_token):
    try:
        episode_id = episode_url.split("/")[-1].split("?")[0]
        endpoint = f"https://api.spotify.com/v1/episodes/{episode_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("audio_preview_url"), data.get("name", "Unknown Episode")
    except Exception as e:
        return None, None