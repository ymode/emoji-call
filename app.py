from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime
import os
import random  # Add import for random selection


app = Flask(__name__)

# Use Azure's writable directory if available, otherwise use local path
if 'WEBSITE_SITE_NAME' in os.environ:
    DB_PATH = os.path.join('/home/data', 'emoji_stats.db')
else:
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'emoji_stats.db')

# Ensure the directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

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

    # Country Flags
    "afghanistan": "🇦🇫",
    "albania": "🇦🇱",
    "algeria": "🇩🇿",
    "andorra": "🇦🇩",
    "angola": "🇦🇴",
    "antigua & barbuda": "🇦🇬",
    "argentina": "🇦🇷",
    "armenia": "🇦🇲",
    "australia": "🇦🇺",
    "austria": "🇦🇹",
    "azerbaijan": "🇦🇿",
    "bahamas": "🇧🇸",
    "bahrain": "🇧🇭",
    "bangladesh": "🇧🇩",
    "barbados": "🇧🇧",
    "belarus": "🇧🇾",
    "belgium": "🇧🇪",
    "belize": "🇧🇿",
    "benin": "🇧🇯",
    "bhutan": "🇧🇹",
    "bolivia": "🇧🇴",
    "bosnia & herzegovina": "🇧🇦",
    "botswana": "🇧🇼",
    "brazil": "🇧🇷",
    "brunei": "🇧🇳",
    "bulgaria": "🇧🇬",
    "burkina faso": "🇧🇫",
    "burundi": "🇧🇮",
    "cabo verde": "🇨🇻",
    "cambodia": "🇰🇭",
    "cameroon": "🇨🇲",
    "canada": "🇨🇦",
    "central african republic": "🇨🇫",
    "chad": "🇹🇩",
    "chile": "🇨🇱",
    "china": "🇨🇳",
    "colombia": "🇨🇴",
    "comoros": "🇰🇲",
    "congo - brazzaville": "🇨🇬",
    "congo - kinshasa": "🇨🇩",
    "costa rica": "🇨🇷",
    "croatia": "🇭🇷",
    "cuba": "🇨🇺",
    "cyprus": "🇨🇾",
    "czechia": "🇨🇿",
    "denmark": "🇩🇰",
    "djibouti": "🇩🇯",
    "dominica": "🇩🇲",
    "dominican republic": "🇩🇴",
    "ecuador": "🇪🇨",
    "egypt": "🇪🇬",
    "el salvador": "🇸🇻",
    "equatorial guinea": "🇬🇶",
    "eritrea": "🇪🇷",
    "estonia": "🇪🇪",
    "eswatini": "🇸🇿",
    "ethiopia": "🇪🇹",
    "fiji": "🇫🇯",
    "finland": "🇫🇮",
    "france": "🇫🇷",
    "gabon": "🇬🇦",
    "gambia": "🇬🇲",
    "georgia": "🇬🇪",
    "germany": "🇩🇪",
    "ghana": "🇬🇭",
    "greece": "🇬🇷",
    "grenada": "🇬🇩",
    "guatemala": "🇬🇹",
    "guinea": "🇬🇳",
    "guinea-bissau": "🇬🇼",
    "guyana": "🇬🇾",
    "haiti": "🇭🇹",
    "honduras": "🇭🇳",
    "hong kong": "🇭🇰",
    "hungary": "🇭🇺",
    "iceland": "🇮🇸",
    "india": "🇮🇳",
    "indonesia": "🇮🇩",
    "iran": "🇮🇷",
    "iraq": "🇮🇶",
    "ireland": "🇮🇪",
    "israel": "🇮🇱",
    "italy": "🇮🇹",
    "jamaica": "🇯🇲",
    "japan": "🇯🇵",
    "jordan": "🇯🇴",
    "kazakhstan": "🇰🇿",
    "kenya": "🇰🇪",
    "kiribati": "🇰🇮",
    "kosovo": "🇽🇰",
    "kuwait": "🇰🇼",
    "kyrgyzstan": "🇰🇬",
    "laos": "🇱🇦",
    "latvia": "🇱🇻",
    "lebanon": "🇱🇧",
    "lesotho": "🇱🇸",
    "liberia": "🇱🇷",
    "libya": "🇱🇾",
    "liechtenstein": "🇱🇮",
    "lithuania": "🇱🇹",
    "luxembourg": "🇱🇺",
    "madagascar": "🇲🇬",
    "malawi": "🇲🇼",
    "malaysia": "🇲🇾",
    "maldives": "🇲🇻",
    "mali": "🇲🇱",
    "malta": "🇲🇹",
    "marshall islands": "🇲🇭",
    "mauritania": "🇲🇷",
    "mauritius": "🇲🇺",
    "mexico": "🇲🇽",
    "micronesia": "🇫🇲",
    "moldova": "🇲🇩",
    "monaco": "🇲🇨",
    "mongolia": "🇲🇳",
    "montenegro": "🇲🇪",
    "morocco": "🇲🇦",
    "mozambique": "🇲🇿",
    "myanmar": "🇲🇲",
    "namibia": "🇳🇦",
    "nauru": "🇳🇷",
    "nepal": "🇳🇵",
    "netherlands": "🇳🇱",
    "new zealand": "🇳🇿",
    "nicaragua": "🇳🇮",
    "niger": "🇳🇪",
    "nigeria": "🇳🇬",
    "north korea": "🇰🇵",
    "north macedonia": "🇲🇰",
    "norway": "🇳🇴",
    "oman": "🇴🇲",
    "pakistan": "🇵🇰",
    "palau": "🇵🇼",
    "palestinian territories": "🇵🇸",
    "panama": "🇵🇦",
    "papua new guinea": "🇵🇬",
    "paraguay": "🇵🇾",
    "peru": "🇵🇪",
    "philippines": "🇵🇭",
    "poland": "🇵🇱",
    "portugal": "🇵🇹",
    "qatar": "🇶🇦",
    "romania": "🇷🇴",
    "russia": "🇷🇺",
    "rwanda": "🇷🇼",
    "saint kitts & nevis": "🇰🇳",
    "saint lucia": "🇱🇨",
    "saint vincent & grenadines": "🇻🇨",
    "samoa": "🇼🇸",
    "san marino": "🇸🇲",
    "sao tome & principe": "🇸🇹",
    "saudi arabia": "🇸🇦",
    "senegal": "🇸🇳",
    "serbia": "🇷🇸",
    "seychelles": "🇸🇨",
    "sierra leone": "🇸🇱",
    "singapore": "🇸🇬",
    "slovakia": "🇸🇰",
    "slovenia": "🇸🇮",
    "solomon islands": "🇸🇧",
    "somalia": "🇸🇴",
    "south africa": "🇿🇦",
    "south korea": "🇰🇷",
    "south sudan": "🇸🇸",
    "spain": "🇪🇸",
    "sri lanka": "🇱🇰",
    "sudan": "🇸🇩",
    "suriname": "🇸🇷",
    "sweden": "🇸🇪",
    "switzerland": "🇨🇭",
    "syria": "🇸🇾",
    "taiwan": "🇹🇼",
    "tajikistan": "🇹🇯",
    "tanzania": "🇹🇿",
    "thailand": "🇹🇭",
    "timor-leste": "🇹🇱",
    "togo": "🇹🇬",
    "tonga": "🇹🇴",
    "trinidad & tobago": "🇹🇹",
    "tunisia": "🇹🇳",
    "turkey": "🇹🇷",
    "turkmenistan": "🇹🇲",
    "tuvalu": "🇹🇻",
    "uganda": "🇺🇬",
    "ukraine": "🇺🇦",
    "united arab emirates": "🇦🇪",
    "united kingdom": "🇬🇧",
    "united states": "🇺🇸",
    "uruguay": "🇺🇾",
    "uzbekistan": "🇺🇿",
    "vanuatu": "🇻🇺",
    "vatican city": "🇻🇦",
    "venezuela": "🇻🇪",
    "vietnam": "🇻🇳",
    "yemen": "🇾🇪",
    "zambia": "🇿🇲",
    "zimbabwe": "🇿🇼",

    # Other flags
    "rainbow flag": "🏳️‍🌈",
    "transgender flag": "🏳️‍⚧️",
    "white flag": "🏳️",
    "black flag": "🏴",
    "pirate flag": "🏴‍☠️",
    "united nations": "🇺🇳",
    "european union": "🇪🇺",
    "checkered flag": "🏁",
    "triangular flag": "🚩",
    
    # Vehicles and Transport
    "car": "🚗",
    "taxi": "🚕",
    "bus": "🚌",
    "ambulance": "🚑",
    "fire truck": "🚒",
    "police car": "🚓",
    "motorcycle": "🏍️",
    "bicycle": "🚲",
    "airplane": "✈️",
    "helicopter": "🚁",
    "sailboat": "⛵",
    "ship": "🚢",
    "train": "🚆",
    "metro": "🚇",

    # Buildings and Places
    "house": "🏠",
    "office": "🏢",
    "hospital": "🏥",
    "school": "🏫",
    "church": "⛪",
    "mosque": "🕌",
    "synagogue": "🕍",
    "stadium": "🏟️",
    "castle": "🏰",
    "tent": "⛺",
    "statue of liberty": "🗽",
    "mount fuji": "🗻",

    # Hands and Body
    "ok hand": "👌",
    "pinching hand": "🤏",
    "point up": "☝️",
    "point right": "👉",
    "point left": "👈",
    "point down": "👇",
    "open hands": "👐",
    "palms up": "🤲",
    "fist": "✊",
    "call me hand": "🤙",
    "writing hand": "✍️",
    "nail polish": "💅",
    "eyes": "👀",
    "brain": "🧠",
    "tongue": "👅",
    "ear": "👂",
    "nose": "👃",
    "foot": "🦶",
    "bone": "🦴",
    "tooth": "🦷",

    # Clothing and Accessories
    "glasses": "👓",
    "sunglasses": "🕶️",
    "crown": "👑",
    "top hat": "🎩",
    "baseball cap": "🧢",
    "ring": "💍",
    "handbag": "👜",
    "backpack": "🎒",
    "high heel": "👠",
    "sneaker": "👟",
    "necktie": "👔",
    "dress": "👗",

    # Office and Tech
    "laptop": "💻",
    "desktop": "🖥️",
    "keyboard": "⌨️",
    "printer": "🖨️",
    "mouse": "🖱️",
    "phone": "📱",
    "telephone": "📞",
    "floppy disk": "💾",
    "cd": "💿",
    "tv": "📺",
    "radio": "📻",
    "satellite": "📡",
    "envelope": "✉️",
    "package": "📦",
    "clipboard": "📋",
    "pushpin": "📌",
    "paperclip": "📎",
    "scissors": "✂️",
    "pen": "🖊️",
    "pencil": "✏️",
    "calendar": "📅",

    # Symbols
    "check mark": "✅",
    "cross mark": "❌",
    "question mark": "❓",
    "exclamation mark": "❗",
    "plus": "➕",
    "minus": "➖",
    "multiply": "✖️",
    "infinity": "♾️",
    "recycle": "♻️",
    "peace": "☮️",
    "yin yang": "☯️",
    "atom": "⚛️",
    "radioactive": "☢️",
    "biohazard": "☣️",
    "medical symbol": "⚕️",
    "no entry": "⛔",
    "prohibited": "🚫",
    "arrow up": "⬆️",
    "arrow down": "⬇️",
    "arrow left": "⬅️",
    "arrow right": "➡️",

    # Animals
    "bee": "🐝",
    "ladybug": "🐞",
    "snail": "🐌",
    "turtle": "🐢",
    "snake": "🐍",
    "whale": "🐋",
    "dolphin": "🐬",
    "shark": "🦈",
    "eagle": "🦅",
    "owl": "🦉",
    "parrot": "🦜",
    "flamingo": "🦩",
    "bat": "🦇",
    "gorilla": "🦍",
    "fox": "🦊",
    "deer": "🦌",
    "hedgehog": "🦔",
    "squirrel": "🐿️",
    "rabbit": "🐰",
    "bear": "🐻",
    "wolf": "🐺",
    "horse": "🐴",
    "crocodile": "🐊",
    "dinosaur": "🦕",
    "t-rex": "🦖",

    # Food and Drink
    "apple": "🍎",
    "banana": "🍌",
    "grapes": "🍇",
    "watermelon": "🍉",
    "strawberry": "🍓",
    "cherry": "🍒",
    "peach": "🍑",
    "mango": "🥭",
    "avocado": "🥑",
    "broccoli": "🥦",
    "carrot": "🥕",
    "corn": "🌽",
    "hot pepper": "🌶️",
    "egg": "🥚",
    "cheese": "🧀",
    "bacon": "🥓",
    "popcorn": "🍿",
    "ramen": "🍜",
    "cookie": "🍪",
    "chocolate": "🍫",
    "candy": "🍬",
    "lollipop": "🍭",
    "tea": "🍵",
    "bubble tea": "🧋",
    "tropical drink": "🍹",

    # Science and Nature
    "microscope": "🔬",
    "telescope": "🔭",
    "test tube": "🧪",
    "dna": "🧬",
    "petri dish": "🧫",
    "magnet": "🧲",
    "volcano": "🌋",
    "earth globe": "🌍",
    "globe americas": "🌎",
    "globe asia": "🌏",
    "milky way": "🌌",
    "comet": "☄️",
    "ringed planet": "🪐",

    # Music and Entertainment
    "drum": "🥁",
    "trumpet": "🎺",
    "violin": "🎻",
    "piano": "🎹",
    "saxophone": "🎷",
    "ticket": "🎫",
    "clapper board": "🎬",
    "video game": "🎮",
    "joystick": "🕹️",
    "slot machine": "🎰",
    "bowling": "🎳",
    "trophy": "🏆",
    "medal": "🏅",
    "first place medal": "🥇",

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

# Category mapping for filtering
CATEGORIES = {}
_current_category = "Other"
import re as _re
# Parse categories from comments in EMOJIS source
_source_lines = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.py')).read().split('\n')
_in_emojis = False
for _line in _source_lines:
    _stripped = _line.strip()
    if _stripped.startswith('EMOJIS = {'):
        _in_emojis = True
        continue
    if _in_emojis and _stripped == '}':
        break
    if _in_emojis and _stripped.startswith('#'):
        _current_category = _stripped.lstrip('# ').strip()
        if _current_category not in CATEGORIES:
            CATEGORIES[_current_category] = []
    elif _in_emojis and '":' in _stripped:
        _match = _re.match(r'"([^"]+)"', _stripped)
        if _match:
            _name = _match.group(1)
            if _name in EMOJIS:
                if _current_category not in CATEGORIES:
                    CATEGORIES[_current_category] = []
                CATEGORIES[_current_category].append(_name)

# Build reverse lookup: emoji_name -> category
EMOJI_TO_CATEGORY = {}
for _cat, _names in CATEGORIES.items():
    for _name in _names:
        EMOJI_TO_CATEGORY[_name] = _cat

# Database initialization
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

# Initialize database on app startup
init_db()

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
    
    # Get updated combined count (copy + api)
    c.execute('SELECT copy_count + api_count FROM emoji_counts WHERE emoji_name = ?', (emoji_name,))
    count = c.fetchone()[0]
    
    conn.close()
    return count

def get_all_emojis():
    return EMOJIS

@app.route('/')
def index():
    emojis = get_all_emojis()
    counts = get_emoji_counts()

    # Sort emojis by total usage count (descending)
    sorted_emojis = dict(sorted(emojis.items(), key=lambda x: counts.get(x[0], 0), reverse=True))

    return render_template('index.html', emojis=sorted_emojis, counts=counts,
                         categories=CATEGORIES, emoji_to_category=EMOJI_TO_CATEGORY)

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

@app.route('/api/random')
def get_random_emoji():
    emoji_name = random.choice(list(EMOJIS.keys()))
    count = increment_count(emoji_name, 'api')
    return jsonify({
        'emoji': EMOJIS[emoji_name],
        'name': emoji_name,
        'count': count
    })

@app.route('/api-docs')
def api_docs():
    return render_template('api.html')

if __name__ == '__main__':
    app.run(debug=True) 
