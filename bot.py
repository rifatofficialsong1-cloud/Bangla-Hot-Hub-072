import telebot
import json
import os
from flask import Flask, jsonify

# আপনার বটের টোকেন এখানে দিন
API_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# ডাটা সেভ রাখার জন্য একটি ডিকশনারি (বট রানিং থাকা অবস্থায় মেমরিতে থাকবে)
video_db = []

@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_id = message.video.file_id
    caption = message.caption if message.caption else "No Title"
    
    # ভিডিওর তথ্য লিস্টে যোগ করা
    video_data = {
        "id": len(video_db) + 1,
        "file_id": file_id,
        "title": caption
    }
    video_db.append(video_data)
    
    bot.reply_to(message, f"✅ ভিডিও সেভ হয়েছে!\nTitle: {caption}\nTotal: {len(video_db)}")

# Mini App এর জন্য API Route
@app.route('/get_videos', methods=['GET'])
def get_videos():
    return jsonify(video_db)

if __name__ == "__main__":
    # বট এবং ফ্লাস্ক সার্ভার একসাথে চালানোর জন্য (টেস্টিং পারপাস)
    from threading import Thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=5000)).start()
    bot.polling()
