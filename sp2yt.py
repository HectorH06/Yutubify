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