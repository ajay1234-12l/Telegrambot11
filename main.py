from flask import Flask, request, render_template
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
import os

app = Flask(__name__)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# Load session strings from files
def get_sessions():
    session_files = os.listdir("sessions")
    return [f"sessions/{f}" for f in session_files if f.endswith('.session')]

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        link = request.form.get("link")
        if link:
            message = join_all(link)
    return render_template("index.html", message=message)

def join_all(link):
    sessions = get_sessions()
    success = 0
    fail = 0

    for s in sessions:
        try:
            client = TelegramClient(s, API_ID, API_HASH)
            client.connect()
            if not client.is_user_authorized():
                continue
            entity = client.get_entity(link)
            client(JoinChannelRequest(entity))
            success += 1
            client.disconnect()
        except Exception as e:
            fail += 1
    return f"Join requests sent: ✅ {success} | ❌ {fail}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)