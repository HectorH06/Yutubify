import time

def obtener_canciones_spotify(sp, playlist_url):
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    playlist_data = sp.playlist(playlist_id)
    nombre_playlist = playlist_data["name"]
    
    canciones = []
    results = playlist_data["tracks"]
    while results:
        for item in results["items"]:
            track = item["track"]
            if track:
                nombre = track["name"]
                artista = track["artists"][0]["name"]
                canciones.append(f"{nombre} {artista}")
        if results.get("next"):
            results = sp.next(results)
        else:
            break
    return nombre_playlist, canciones

def crear_playlist_youtube(youtube, titulo):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": titulo, "description": "Transferida desde Spotify"},
            "status": {"privacyStatus": "private"}
        }
    )
    response = request.execute()
    return response["id"]

def agregar_canciones_youtube(youtube, canciones, playlist_id):
    for cancion in canciones:
        print(f"Buscando: {cancion}")
        try:
            search_response = youtube.search().list(
                q=cancion, part="snippet", maxResults=1, type="video"
            ).execute()
            if search_response["items"]:
                video_id = search_response["items"][0]["id"]["videoId"]
                youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id
                            }
                        }
                    }
                ).execute()
                print(f"Agregada: {cancion}")
            else:
                print(f"No se encontró: {cancion}")
        except Exception as e:
            print(f"Error al agregar '{cancion}': {e}")
        time.sleep(1)