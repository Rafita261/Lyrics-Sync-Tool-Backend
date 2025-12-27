import requests

def get_lyrics_from_ovh(artiste, titre) :
    SEARCH_URL = "https://api.lyrics.ovh/v1/"
    SEARCH_URL+=artiste+"/"+titre

    data = dict(requests.get(SEARCH_URL).json())
    if 'lyrics' in data :
        return data['lyrics']
    return None

def get_lyrics_from_ovh(url) :
    data = dict(requests.get(url).json())
    if 'lyrics' in data :
        return data['lyrics']
    return None

# TEST

if __name__ == '__main__' :
    print(get_lyrics_from_ovh("Rim ka","Vadiko"))