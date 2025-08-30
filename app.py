from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Base music folder (mount this volume in Docker)
MUSIC_DIR = os.getenv("MUSIC_DIR", "/music")

@app.route("/sync", methods=["POST"])
def sync():
    data = request.get_json(force=True)

    # Expecting {"playlist": "spotify_playlist_url"}
    playlist = data.get("playlist")
    sync_file = data.get("sync_file")

    if not playlist:
        return jsonify({"error": "Missing 'playlist'"}), 400

    try:
        # Run spotDL sync
        if sync_file:
            subprocess.run( ["spotdl", "sync", playlist, "--output", MUSIC_DIR, "--save-file", sync_file], check=True )
        else:
            subprocess.run( ["spotdl", "sync", playlist, "--output", MUSIC_DIR], check=True)
        return jsonify({"status": "ok", "playlist": playlist})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Sync failed", "details": str(e)}), 500

