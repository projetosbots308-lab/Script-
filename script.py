import os
import time
import json
from pyrogram import Client
from pyrogram.errors import FloodWait

# ================= CONFIG =================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")

ORIGIN_CHAT = int(os.getenv("ORIGIN_CHAT"))
DEST_CHAT = int(os.getenv("DEST_CHAT"))

DELAY = float(os.getenv("DELAY", 1))
CACHE_FILE = "progress.json"

# ================= CLIENT =================
app = Client(
    "railway",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

# ================= UTILS =================
def safe_exec(func):
    while True:
        try:
            return func()
        except FloodWait as e:
            print(f"FloodWait {e.value}s")
            time.sleep(e.value)
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(5)

def load_progress():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {"last_id": 0}

def save_progress(last_id):
    with open(CACHE_FILE, "w") as f:
        json.dump({"last_id": last_id}, f)

def get_caption(msg):
    return msg.caption if msg.caption else None

# ================= SENDERS =================
def send_message(msg):
    if msg.text:
        safe_exec(lambda: app.send_message(
            DEST_CHAT,
            msg.text,
            disable_web_page_preview=True
        ))

    elif msg.photo:
        safe_exec(lambda: app.send_photo(
            DEST_CHAT,
            msg.photo.file_id,
            caption=get_caption(msg)
        ))

    elif msg.video:
        safe_exec(lambda: app.send_video(
            DEST_CHAT,
            msg.video.file_id,
            caption=get_caption(msg)
        ))

    elif msg.document:
        safe_exec(lambda: app.send_document(
            DEST_CHAT,
            msg.document.file_id,
            caption=get_caption(msg)
        ))

    elif msg.audio:
        safe_exec(lambda: app.send_audio(
            DEST_CHAT,
            msg.audio.file_id,
            caption=get_caption(msg)
        ))

    elif msg.voice:
        safe_exec(lambda: app.send_voice(
            DEST_CHAT,
            msg.voice.file_id
        ))

    elif msg.animation:
        safe_exec(lambda: app.send_animation(
            DEST_CHAT,
            msg.animation.file_id,
            caption=get_caption(msg)
        ))

    elif msg.sticker:
        safe_exec(lambda: app.send_sticker(
            DEST_CHAT,
            msg.sticker.file_id
        ))

    elif msg.video_note:
        safe_exec(lambda: app.send_video_note(
            DEST_CHAT,
            msg.video_note.file_id
        ))

# ================= MAIN =================
def main():
    progress = load_progress()
    last_id = progress["last_id"]

    print(f"Continuando do ID: {last_id}")

    for msg in app.get_chat_history(ORIGIN_CHAT, reverse=True):
        if msg.id <= last_id:
            continue

        if msg.empty or msg.service:
            continue

        send_message(msg)

        save_progress(msg.id)

        print(f"Enviado: {msg.id}")

        time.sleep(DELAY)

# ================= RUN =================
with app:
    while True:
        try:
            main()
            print("Finalizado. Verificando novos em 60s...")
            time.sleep(60)
        except Exception as e:
            print(f"Erro geral: {e}")
            time.sleep(10)
