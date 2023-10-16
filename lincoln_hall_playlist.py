import os
import sys
module_path = os.path.abspath(os.path.join('../'))
if module_path not in sys.path:
    sys.path.append(module_path)

import datetime as dt
import spotipy
import utils

def main(time_in_future: dt.timedelta, track_limit: int):
    spotify = utils.auth()
    id = spotify.me()["id"]
    playlist_url = 'https://open.spotify.com/playlist/5SJEQwEzWMWlbg1WxdCgfC?si=2dfa7bb730bf4319'
    
    # clear old items
    spotify.playlist_replace_items(playlist_url, [])
    num_songs_added = 0
    with open('lincoln_hall_artists.txt', 'r') as f:
        for line in f.readlines():
            datestr = line[:10]
            artist_name = line[11:-1]
            date = dt.datetime.strptime(datestr, '%Y-%m-%d')
            if date.date() >= dt.date.today() and date.date() - dt.date.today() <= time_in_future:
                search_result = spotify.search(q=f"artist:{artist_name}", type="artist")
                if len(search_result["artists"]["items"]) > 0:
                    artist = search_result["artists"]["items"][0]
                    if artist['name'].lower() == artist_name.lower():
                        artist_uri = search_result["artists"]["items"][0]["uri"]
                        tracks = spotify.artist_top_tracks(artist_uri)["tracks"][:track_limit]
                        track_uris = [track["uri"] for track in tracks]
                        spotify.playlist_add_items(playlist_url, track_uris, position=num_songs_added)
                        num_songs_added += len(track_uris)
                    else:
                        print(f'Searched for {artist_name}, best match {artist["name"]}')
                else:
                    print(f'{artist_name} not found.')

main(dt.timedelta(days=30), 3)