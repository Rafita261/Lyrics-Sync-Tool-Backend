import requests

def get_lyrics_from_ovh(artiste="", titre="", url=None):
    try:
        SEARCH_URL = url or "https://api.lyrics.ovh/v1/"
        SEARCH_URL += artiste + "/" + titre
        
        response = requests.get(SEARCH_URL, timeout=15)
        
        response.raise_for_status()
        data = dict(response.json())
        
        if 'lyrics' in data:
            return data['lyrics']
        return None
        
    except requests.exceptions.Timeout:
        print(f"Timeout OVH: {SEARCH_URL}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur requête OVH: {str(e)}")
        return None
    except Exception as e:
        print(f"Erreur inattendue OVH: {str(e)}")
        return None

# TEST
if __name__ == '__main__':
    print(get_lyrics_from_ovh(url="https://api.lyrics.ovh/v1/Dadju/Reine"))