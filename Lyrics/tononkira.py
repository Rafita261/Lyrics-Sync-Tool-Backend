from bs4 import BeautifulSoup, NavigableString, Tag
import requests
from fuzzywuzzy import fuzz
from urllib.parse import urljoin

def get_list_lyrics_in_tononkira(title: str, artiste: str) -> list[dict]:
    BASE_URL = "https://tononkira.serasera.org"
    SEARCH_URL = f"{BASE_URL}/tononkira?lohateny={title.replace(' ', '+')}"

    html = requests.get(SEARCH_URL, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")

    results = []

    for bloc in soup.select("div.border.p-2.mb-3"):
        links = bloc.find_all("a")
        if len(links) < 2:
            continue

        titre = links[0].get_text(strip=True)
        paroles_url = urljoin(BASE_URL, links[0]["href"])

        artiste_nom = links[1].get_text(strip=True)

        score = fuzz.token_set_ratio(
            artiste.lower(),
            artiste_nom.lower()
        )

        results.append({
            "titre": titre,
            "artiste": artiste_nom,
            "url": paroles_url,
            "from" : "tononkira",
            "_score": score
        })

    # Tri fuzzy descendant
    results.sort(key=lambda x: x["_score"], reverse=True)

    # Nettoyage
    for r in results:
        r.pop("_score")

    return results

def get_lyrics_in_tononkira(url: str) -> str:
    html = requests.get(url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")

    # Point d’ancrage juste avant les paroles
    marker = soup.select_one("div.print.my-3.fst-italic")
    if not marker:
        return ""

    lyrics_lines = []

    for node in marker.next_siblings:
        # Stop à la séparation --------
        if isinstance(node, NavigableString) and "--------" in node:
            break

        if isinstance(node, Tag):
            if node.name == "br":
                lyrics_lines.append("\n")
            else:
                text = node.get_text(strip=False)
                if text:
                    lyrics_lines.append(text)

        elif isinstance(node, NavigableString):
            text = node.strip()
            if text:
                lyrics_lines.append(text)

    # Nettoyage final
    lyrics = "".join(lyrics_lines)
    lyrics = lyrics.replace("\n\n\n", "\n\n").strip()

    return lyrics

# TEST
if __name__ == '__main__' :
    print(get_lyrics_in_tononkira("https://tononkira.serasera.org/hira/tanjona-randrianarivelo/tiako-izy"))