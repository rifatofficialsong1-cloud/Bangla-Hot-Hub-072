import telebot
import json
import os
import requests
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
CORS(app)

DATA_FILE = 'videos.json'

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except: return []
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    video_db = load_data()
    file_id = message.video.file_id
    caption = message.caption if message.caption else f"Video {len(video_db) + 1}"
    
    new_video = {
        "id": len(video_db) + 1,
        "title": caption,
        "file_id": file_id,
        "thumb": "https://images.unsplash.com/photo-1616469829581-73993eb86b02?q=80&w=200&h=300&fit=crop"
    }
    
    video_db.append(new_video)
    save_data(video_db)
    bot.reply_to(message, f"✅ সেভ হয়েছে: {caption}")

@app.route('/get_videos')
def get_videos():
    return jsonify(load_data())

# এই অংশটি ভিডিও স্ট্রিমিং লিঙ্ক তৈরি করবে
@app.route('/stream/<file_id>')
def stream_video(file_id):
    file_info = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"
    return redirect(file_url)

@app.route('/')
def home():
    return "Bot is Running!"

if __name__ == "__main__":
    from threading import Thread
    port = int(os.environ.get("PORT", 10000))
    Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()
    bot.polling(non_stop=True)
