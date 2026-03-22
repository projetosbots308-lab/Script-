from pyrogram import Client
import os

app = Client(
    "test",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    session_string=os.getenv("STRING_SESSION")
)

app.start()

print("LOGADO COM SUCESSO")

app.stop()
