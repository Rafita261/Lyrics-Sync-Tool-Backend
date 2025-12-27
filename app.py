from flask import Flask, request, jsonify
from flask_cors import CORS
from Lyrics.tononkira import get_lyrics_in_tononkira, get_list_lyrics_in_tononkira
from Lyrics.ovh import get_lyrics_from_ovh
from Lyrics.lrclib import get_lyrics_from_lrclib
import logging

from Export.audio import ffmpeg_exists

app = Flask(__name__)
CORS(app)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mapping des sources vers les fonctions
LYRICS_FUNCTIONS = {
    'tononkira': get_lyrics_in_tononkira,
    'lrclib': get_lyrics_from_lrclib,
    'ovh': get_lyrics_from_ovh
}

@app.route("/get_lyrics_list", methods=["POST"])
def get_lyrics_list():
    """Recherche des paroles dans plusieurs sources"""
    try:
        data = request.get_json(silent=True) or {}
        titre = data.get("titre", "").strip()
        artiste = data.get("artiste", "").strip()
        
        if not titre or not artiste:
            return jsonify({
                "error": "Champs requis manquants",
                "required": ["titre", "artiste"]
            }), 400
        
        # Recherche dans tononkira
        results = []
        try:
            results = get_list_lyrics_in_tononkira(title=titre, artiste=artiste)
        except Exception as e:
            logger.error(f"Erreur tononkira search: {str(e)}")
        
        # Vérifier lyrics.ovh
        try:
            ovh_lyrics = get_lyrics_from_ovh(artiste, titre)
            if ovh_lyrics and ovh_lyrics.strip():
                results.append({
                    "titre": titre,
                    "artiste": artiste,
                    "url": f"https://api.lyrics.ovh/v1/{artiste}/{titre}",
                    "from": "ovh"
                })
        except Exception as e:
            logger.error(f"Erreur OVH check: {str(e)}")
        
        # Vérifier lrclib
        try:
            lrclib_lyrics = get_lyrics_from_lrclib(artiste, titre)
            if lrclib_lyrics and lrclib_lyrics.strip():
                results.append({
                    "titre": titre,
                    "artiste": artiste,
                    "url": f"https://lrclib.net/api/get?artist_name={artiste}&track_name={titre}",
                    "from": "lrclib"
                })
        except Exception as e:
            logger.error(f"Erreur lrclib check: {str(e)}")
        
        return jsonify(results), 200
        
    except Exception as e:
        logger.error(f"Erreur get_lyrics_list: {str(e)}")
        return jsonify({"error": "Erreur serveur interne"}), 500

@app.route("/get_lyrics", methods=["POST"])
def get_lyrics():
    """Récupère les paroles depuis une URL spécifique"""
    try:
        data = request.get_json(silent=True) or {}
        url = data.get("url", "").strip()
        lyrics_site = data.get("from", "").strip().lower()
        
        if not url:
            return jsonify({"error": "URL requise"}), 400
        
        if not lyrics_site:
            return jsonify({"error": "Source (from) requise"}), 400
        
        # Récupérer la fonction appropriée
        lyrics_function = LYRICS_FUNCTIONS.get(lyrics_site)
        
        if not lyrics_function:
            return jsonify({
                "error": f"Source '{lyrics_site}' non supportée",
                "supported": list(LYRICS_FUNCTIONS.keys())
            }), 400
        
        # Appeler la fonction
        lyrics = lyrics_function(url=url)
        
        if not lyrics or not lyrics.strip():
            return jsonify({"error": "Aucune parole trouvée"}), 404
        
        return jsonify({"lyrics": lyrics}), 200
        
    except Exception as e:
        logger.error(f"Erreur get_lyrics: {str(e)}")
        return jsonify({"error": "Erreur lors de la récupération des paroles"}), 500

@app.route("/health", methods=["GET"])
def health():
    """Endpoint de santé pour Railway"""
    return jsonify({"status": "ok", "service": "lyrics-api"}), 200

@app.route("/ffmpeg",methods = ["GET"])
def ffmeg_verification() :
    return jsonify({"Exists FFmpeg" : ffmpeg_exists()}), 200 

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint non trouvé"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Erreur serveur interne"}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host="0.0.0.0", port=port, debug=False)