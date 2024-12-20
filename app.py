from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime
import os


app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'emoji_stats.db')# Database initialization
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Create table for emoji usage counts
    c.execute('''
        CREATE TABLE IF NOT EXISTS emoji_counts (
            emoji_name TEXT PRIMARY KEY,
            copy_count INTEGER DEFAULT 0,
            api_count INTEGER DEFAULT 0,
            last_used TIMESTAMP
        )
    ''')
    # Create table for usage history
    c.execute('''
        CREATE TABLE IF NOT EXISTS usage_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emoji_name TEXT,
            usage_type TEXT,
            timestamp TIMESTAMP,
            FOREIGN KEY (emoji_name) REFERENCES emoji_counts (emoji_name)
        )
    ''')
    # Initialize counts for all emojis if they don't exist
    for emoji_name in EMOJIS.keys():
        c.execute('INSERT OR IGNORE INTO emoji_counts (emoji_name, copy_count, api_count) VALUES (?, 0, 0)', (emoji_name,))
    conn.commit()
    conn.close()

def get_emoji_counts():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT emoji_name, copy_count + api_count as total_count FROM emoji_counts')
    counts = {row[0]: row[1] for row in c.fetchall()}
    conn.close()
    return counts

def increment_count(emoji_name, usage_type):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if usage_type == 'copy':
        c.execute('UPDATE emoji_counts SET copy_count = copy_count + 1, last_used = ? WHERE emoji_name = ?',
                 (datetime.now(), emoji_name))
    else:  # api
        c.execute('UPDATE emoji_counts SET api_count = api_count + 1, last_used = ? WHERE emoji_name = ?',
                 (datetime.now(), emoji_name))
    
    # Record in history
    c.execute('INSERT INTO usage_history (emoji_name, usage_type, timestamp) VALUES (?, ?, ?)',
             (emoji_name, usage_type, datetime.now()))
    
    conn.commit()
    
    # Get updated count
    if usage_type == 'copy':
        c.execute('SELECT copy_count FROM emoji_counts WHERE emoji_name = ?', (emoji_name,))
    else:
        c.execute('SELECT api_count FROM emoji_counts WHERE emoji_name = ?', (emoji_name,))
    count = c.fetchone()[0]
    
    conn.close()
    return count

# Manual emoji dictionary
EMOJIS = {
    # Faces and Expressions
    "smiling face": "😊",
    "grinning face": "😀",
    "laughing face": "😂",
    "rolling on floor": "🤣",
    "winking face": "😉",
    "heart eyes": "😍",
    "star struck": "🤩",
    "thinking face": "🤔",
    "mind blown": "🤯",
    "cool face": "😎",
    "nerd face": "🤓",
    "crying face": "😢",
    "loudly crying": "😭",
    "shocked face": "😱",
    "sleeping face": "😴",
    "drooling face": "🤤",
    "zany face": "🤪",
    "partying face": "🥳",
    "smirking face": "😏",
    "unamused face": "😒",
    "rolling eyes": "🙄",
    "angry face": "😠",
    "devil": "😈",
    "angel": "😇",
    
    # Gestures and People
    "thumbs up": "👍",
    "thumbs down": "👎",
    "clapping hands": "👏",
    "raised hands": "🙌",
    "folded hands": "🙏",
    "handshake": "🤝",
    "victory hand": "✌️",
    "love you gesture": "🤟",
    "crossed fingers": "🤞",
    "waving hand": "👋",
    "muscle": "💪",
    "ninja": "🥷",
    "person dancing": "💃",
    "person running": "🏃",
    
    # Hearts and Emotions
    "red heart": "❤️",
    "orange heart": "🧡",
    "yellow heart": "💛",
    "green heart": "💚",
    "blue heart": "💙",
    "purple heart": "💜",
    "broken heart": "💔",
    "sparkling heart": "💖",
    "hundred points": "💯",
    
    # Animals
    "cat": "🐱",
    "dog": "🐶",
    "monkey": "🐒",
    "unicorn": "🦄",
    "panda": "🐼",
    "penguin": "🐧",
    "koala": "🐨",
    "lion": "🦁",
    "tiger": "🐯",
    "cow": "🐮",
    "pig": "🐷",
    "frog": "🐸",
    "octopus": "🐙",
    "butterfly": "🦋",
    
    # Food and Drink
    "pizza": "🍕",
    "burger": "🍔",
    "fries": "🍟",
    "hotdog": "🌭",
    "taco": "🌮",
    "sushi": "🍣",
    "ice cream": "🍦",
    "donut": "🍩",
    "cake": "🎂",
    "coffee": "☕",
    "beer": "🍺",
    "wine": "🍷",
    
    # Activities and Objects
    "soccer ball": "⚽",
    "basketball": "🏀",
    "football": "🏈",
    "tennis": "🎾",
    "volleyball": "🏐",
    "musical note": "🎵",
    "headphones": "🎧",
    "guitar": "🎸",
    "camera": "📷",
    "movie camera": "🎥",
    "game die": "🎲",
    "jigsaw": "🧩",
    "art": "🎨",
    "microphone": "🎤",
    
    # Nature and Weather
    "fire": "🔥",
    "rainbow": "🌈",
    "sun": "☀️",
    "moon": "🌙",
    "cloud": "☁️",
    "lightning": "⚡",
    "umbrella": "☔",
    "snowflake": "❄️",
    "palm tree": "🌴",
    "christmas tree": "🎄",
    "flower": "🌸",
    "four leaf clover": "🍀",
    
    # Other
    "rocket": "🚀",
    "star": "⭐",
    "sparkles": "✨",
    "party popper": "🎉",
    "gift": "🎁",
    "ghost": "👻",
    "alien": "👽",
    "robot": "🤖",
    "poop": "💩",
    "money bag": "💰",
    "gem stone": "💎",
    "warning": "⚠️",
    "light bulb": "💡",
    "lock": "🔒",
    "key": "🔑",
    "magnifying glass": "🔍",
    "alarm clock": "⏰",
    "hourglass": "⌛",
    "battery": "🔋",
    "books": "📚"
}

def get_all_emojis():
    return EMOJIS

@app.route('/')
def index():
    emojis = get_all_emojis()
    counts = get_emoji_counts()
    return render_template('index.html', emojis=emojis, counts=counts)

@app.route('/api/emoji/<emoji_name>')
def get_emoji(emoji_name):
    emojis = get_all_emojis()
    if emoji_name in emojis:
        count = increment_count(emoji_name, 'api')
        return jsonify({
            'emoji': emojis[emoji_name],
            'name': emoji_name,
            'count': count
        })
    return jsonify({'error': 'Emoji not found'}), 404

@app.route('/api/increment/<emoji_name>')
def increment_emoji_count(emoji_name):
    emojis = get_all_emojis()
    if emoji_name in emojis:
        count = increment_count(emoji_name, 'copy')
        return jsonify({
            'success': True,
            'count': count
        })
    return jsonify({'error': 'Emoji not found'}), 404

@app.route('/api/stats')
def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT 
            emoji_name,
            copy_count,
            api_count,
            last_used
        FROM emoji_counts
        ORDER BY (copy_count + api_count) DESC
        LIMIT 10
    ''')
    top_emojis = [{
        'emoji': EMOJIS[row[0]],
        'name': row[0],
        'copy_count': row[1],
        'api_count': row[2],
        'last_used': row[3]
    } for row in c.fetchall()]
    conn.close()
    return jsonify(top_emojis)

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 