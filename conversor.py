import json
import tempfile
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from sp2yt import obtener_canciones_spotify, crear_playlist_youtube, agregar_canciones_youtube

#* Auth spoti
def autenticar_spotify(spotify_secrets):
    auth = SpotifyClientCredentials(
        client_id=spotify_secrets["client_id"],
        client_secret=spotify_secrets["client_secret"]
    )
    return spotipy.Spotify(auth_manager=auth)

#* Auth yt
def autenticar_youtube(youtube_secrets):
    with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as temp:
        json.dump(youtube_secrets, temp)
        temp.flush()
        flow = InstalledAppFlow.from_client_secrets_file(temp.name, scopes=["https://www.googleapis.com/auth/youtube"])
        credentials = flow.run_local_server(open_browser=True)
    return build("youtube", "v3", credentials=credentials)



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

    print("Autenticando YouTube...")
    youtube = autenticar_youtube(secrets["youtube"])

    print("Creando playlist en YouTube...")
    playlist_id = crear_playlist_youtube(youtube, nombre_playlist)

    print("Agregando canciones a YouTube...")
    agregar_canciones_youtube(youtube, canciones, playlist_id)

    print("¡Listo! Playlist creada con éxito.")
