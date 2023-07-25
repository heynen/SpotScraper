import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

#Function that takes Spotify pagination into account;

def get_playlist_track_uris(playlist_id, client_id, client_secret,destination_folder):
    # Authenticate with Spotify API using client credentials
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Get the tracks from the playlist
    results = sp.playlist_tracks(playlist_id)

    # Extract and save the URIs of each track to a text file
    with open(os.path.join(destination_folder, 'playlist_uris.txt'), 'w') as file:
        while results:
            tracks = results['items']
            for item in tracks:
                track = item['track']
                uri = track['uri']
                file.write(f"{uri}\n")

            # Check if there are more tracks to fetch
            if results['next']:
                results = sp.next(results)
            else:
                results = None

    print("Playlist URIs saved to playlist_uris.txt")
    
def convert_uri_to_track_info(client_id, client_secret,destination_folder):
    # Authenticate with Spotify API using client credentials
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Read the URIs from the playlist_uris.txt file
    with open(os.path.join(destination_folder, 'playlist_uris.txt'), 'r') as file:
        uris = file.read().splitlines()

    # Extract and save all track information to a new text file
    with open(os.path.join(destination_folder, 'track_info.txt'), 'w') as file:
        for uri in uris:
            track_info = sp.track(uri)
            track_name = track_info['name']
            artists = ', '.join([artist['name'] for artist in track_info['artists']])
            album = track_info['album']['name']
            preview_url = track_info['preview_url']

            file.write(f"Track Name: {track_name}\n")
            file.write(f"Artists: {artists}\n")
            file.write(f"Album: {album}\n")
            file.write(f"Preview URL: {preview_url}\n")
            file.write("\n")

    print("Track information saved to track_info.txt")



