import telebot
import json
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# সরাসরি টোকেন না দিয়ে এনভায়রনমেন্ট ভেরিয়েবল ব্যবহার
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
    bot.reply_to(message, f"✅ '{caption}' সেভ হয়েছে!\nমোট ভিডিও: {len(video_db)}")

@app.route('/get_videos')
def get_videos():
    return jsonify(load_data())

if __name__ == "__main__":
    from threading import Thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.polling()
