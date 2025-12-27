import requests

def get_lyrics_from_lrclib(artiste="", titre="", url=None) -> str:
    """Récupère les paroles depuis lrclib.net"""
    try:
        SEARCH_URL = url or f"https://lrclib.net/api/get?artist_name={artiste}&track_name={titre}"
        
        response = requests.get(SEARCH_URL, timeout=15)
        print(SEARCH_URL)
        # Si 404, retourner None sans erreur
        if "status_code" in response and response.status_code == 404:
            return None
        
        response.raise_for_status()
        
        # Vérifier si la réponse est vide
        if not response.text or response.text.strip() == '':
            return None
        
        data = dict(response.json())
        
        # Vérifier si l'API retourne un 404 dans le JSON
        if "statusCode" in data and data["statusCode"] == 404:
            return None
        
        lyrics = data.get("plainLyrics")
        
        return lyrics if lyrics else None
        
    except requests.exceptions.Timeout:
        print(f"Timeout lrclib: {SEARCH_URL if 'SEARCH_URL' in locals() else 'URL inconnue'}")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return None
        print(f"Erreur HTTP lrclib ({e.response.status_code})")
        return None
    except requests.exceptions.JSONDecodeError:
        # C'est ici que l'erreur "Expecting value: line 1 column 1" se produisait
        print(f"Réponse non-JSON de lrclib (réponse vide ou invalide)")
        return None
    except KeyError as e:
        # Si plainLyrics n'existe pas dans la réponse
        print(f"Clé manquante dans la réponse lrclib: {str(e)}")
        return None
    except Exception as e:
        print(f"Erreur inattendue lrclib: {str(e)}")
        return None

# TEST
if __name__ == '__main__':
    print("Test 1:")
    result = get_lyrics_from_lrclib(url="https://lrclib.net/api/get?artist_name=Dadju&track_name=Ma+Woman")
    print(result[:200] if result else "Aucune parole trouvée")
    
    print("\nTest 2:")
    result = get_lyrics_from_lrclib(artiste="Adele", titre="Hello")
    print(result[:200] if result else "Aucune parole trouvée")