import telebot
import json
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# Render-এ Environment Variable হিসেবে BOT_TOKEN সেট করে নিও
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
    caption = message.caption if message.caption else f"Premium Video {len(video_db) + 1}"
    
    new_video = {
        "id": len(video_db) + 1,
        "title": caption,
        "file_id": file_id,
        "thumb": f"https://picsum.photos/seed/{len(video_db)}/200/300"
    }
    
    video_db.append(new_video)
    save_data(video_db)
    bot.reply_to(message, f"✅ সেভ হয়েছে: {caption}")

@app.route('/get_videos')
def get_videos():
    return jsonify(load_data())

@app.route('/')
def home():
    return "Bot is Running!"

if __name__ == "__main__":
    from threading import Thread
    # Render-এর জন্য পোর্ট সেট করা হয়েছে
    port = int(os.environ.get("PORT", 10000))
    Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()
    bot.polling(non_stop=True)
