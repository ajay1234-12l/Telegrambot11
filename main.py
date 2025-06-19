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
        try:
            link = request.form["link"]
            for session_file in os.listdir():
                if session_file.endswith(".session"):
                    client = TelegramClient(session_file, api_id, api_hash)
                    client.connect()
                    if not client.is_user_authorized():
                        continue
                    client(ImportChatInviteRequest(link.split("/")[-1]))
                    client.disconnect()
            message = "✅ Join request sent!"
        except Exception as e:
            message = f"❌ Error: {str(e)}"
    return render_template("index.html", message=message)
