import json
import tempfile
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from sp2yt import obtener_canciones_spotify, crear_playlist_youtube, agregar_canciones_youtube

#* Auth spoti
def autenticar_spotify(spotify_secrets):
    auth = SpotifyClientCredentials(
        client_id=spotify_secrets["client_id"],
        client_secret=spotify_secrets["client_secret"]
    )
    return spotipy.Spotify(auth_manager=auth)



if __name__ == "__main__":
    with open("secrets.json") as f:
        secrets = json.load(f)

    spotify_url = input("Playlist link: ").strip()

    print("Autenticando Spotify...")
    sp = autenticar_spotify(secrets["spotify"])

    print("Obteniendo canciones de Spotify...")
    nombre_playlist, canciones = obtener_canciones_spotify(sp, spotify_url)
    print(f"{len(canciones)} canciones encontradas.")
    print(f"Nombre da playli: '{nombre_playlist}'")