import requests

def get_lyrics_from_lrclib(artiste : str, titre : str) -> str :
    SEARCH_URL = f"https://lrclib.net//api/get?artist_name={artiste}&track_name={titre}"

    data = dict(requests.get(SEARCH_URL).json())

    if "statusCode" in data and data["statusCode"] == 404 :
        return None
    
    return data["plainLyrics"]

def get_lyrics_from_lrclib(url : str) -> str :
    data = dict(requests.get(url).json())

    if "statusCode" in data and data["statusCode"] == 404 :
        return None
    
    return data["plainLyrics"]

if __name__ == '__main__' :
    print(get_lyrics_from_lrclib("Ceasar","Tanteraky"))