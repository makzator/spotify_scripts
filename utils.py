import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

def auth():
    with open(".creds.json") as f:
        creds = json.load(f)
    scope = [
        "playlist-read-private",
        "playlist-modify-private",
        "playlist-modify-public",
        "playlist-read-collaborative",
        "user-library-read",
        "user-library-modify",
        "user-read-private",
    ]
    spotify_creds = SpotifyOAuth(**creds, scope=scope)
    spotify = spotipy.Spotify(client_credentials_manager=spotify_creds)
    return spotify

def get_my_playlists(spotify):
    id = spotify.me()["id"]

    with open(".config.json") as f:
        config = json.load(f)
        playlists_ignore = config['playlists_to_ignore']

    my_playlists = []
    offset = 0
    while True:
        pl_batch = spotify.user_playlists(id, limit=50, offset=offset)["items"]
        if len(pl_batch) == 0:
            break
        for pl in pl_batch:
            if pl['owner']['id'] == id and pl['name'] not in playlists_ignore:
                my_playlists.append({
                    'id':pl['id'],
                    'name':pl['name']
                })
        offset += 50
    print(f'Found {len(my_playlists)} playlists.')
    return my_playlists

def get_my_playlist_songs(spotify):
    id = spotify.me()["id"]
    my_playlists = get_my_playlists(spotify)
    my_songs = dict()
    for p in my_playlists:
        tracks = spotify.playlist_items(p['id'])['items']
        for t in tracks:
            if t['added_by']['id'] == id:
                song_id = t['track']['id']
                if not (song_id in my_songs and t['added_at'] > my_songs[song_id]['time']):
                    artists = [artist_info for artist_info in t["track"]["artists"]]
                    my_songs[song_id] = {'name':t['track']['name'], 'time':t['added_at'], 'artists':artists}
    my_songs_sorted = sorted([{'id':s[0]} | s[1] for s in list(my_songs.items())], key=lambda s : s['time'])
    print(f'Found {len(my_songs_sorted)} songs.')
    return my_songs_sorted