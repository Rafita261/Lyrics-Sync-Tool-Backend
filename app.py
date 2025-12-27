from flask import Flask, request, jsonify
from Lyrics.tononkira import get_lyrics_in_tononkira, get_list_lyrics_in_tononkira
from Lyrics.ovh import get_lyrics_from_ovh
from Lyrics.lrclib import get_lyrics_from_lrclib

app = Flask(__name__)

@app.route("/get_lyrics_list", methods=["POST"])
def get_lyrics_list():
    data = request.get_json(silent=True) or {}

    titre = data.get("titre")
    artiste = data.get("artiste")

    if not titre or not artiste:
        return jsonify({
            "error": "Champs requis manquants",
            "required": ["titre", "artiste"]
        }), 400

    results = get_list_lyrics_in_tononkira(title=titre,artiste=artiste)

    if get_lyrics_from_ovh(artiste, titre) : 
        results.append({
            "titre": titre,
            "artiste": artiste,
            "url": "https://api.lyrics.ovh/v1/"+artiste+"/"+titre,
            "from" : "ovh"
        })

    if get_lyrics_from_lrclib(artiste, titre) :
        results.append({
            "titre": titre,
            "artiste": artiste,
            "url": f"https://lrclib.net//api/get?artist_name={artiste}&track_name={titre}",
            "from" : "lrclib"
        })
        
    return jsonify(results), 200

@app.route("/get_lyrics", methods=["POST"])
def get_lyrics() :
    data = request.get_json(silent=True) or {}

    url = data.get("url")
    lyrics_site = data.get("from")

    lyrics_function = [get_lyrics_in_tononkira, get_lyrics_from_lrclib, get_lyrics_from_ovh][["tononkira", "lrclib", "ovh"].index(lyrics_site)]

    return jsonify({"lyrics" : lyrics_function(url)})

if __name__ == '__main__' :
    app.run(debug=True)