# Emoji Library 😎

A simple and fun way to find, copy, and use emojis! Browse our collection through the web interface or access emojis programmatically via our API.

## How to Use

### Web Interface

1. Visit [emoji-app.com](https://emoji-app.com) to browse through our emoji collection
2. Click on any emoji card to instantly copy it to your clipboard
3. See how many times each emoji has been used
4. The count updates in real-time when you or others copy the emoji

### API Usage

#### Get a Single Emoji

Need a specific emoji in your application? Just make a GET request:

```bash
# Get a smiling face emoji
curl https://emoji-app.com/api/emoji/smiling%20face

# Get a heart emoji
curl https://emoji-app.com/api/emoji/red%20heart
```

Response:
```json
{
    "emoji": "😊",
    "name": "smiling face",
    "count": 42  // How many times this emoji has been used
}
```

#### View Popular Emojis

Want to see what's trending? Get the top 10 most used emojis:

```bash
curl https://emoji-app.com/api/stats
```

Response:
```json
[
    {
        "emoji": "😊",
        "name": "smiling face",
        "copy_count": 42,    // Times copied from website
        "api_count": 12,     // Times accessed via API
        "last_used": "2024-01-01 12:00:00"
    },
    // ... more emojis
]
```

### Available Emojis

Here are some popular emojis you can try:
- Faces: "smiling face", "winking face", "thinking face"
- Hearts: "red heart", "blue heart", "purple heart"
- Animals: "cat", "dog", "monkey", "unicorn"
- Objects: "rocket", "camera", "books"
- And many more!

Example API usage:
```bash
curl https://emoji-app.com/api/emoji/thinking%20face
```

## API Endpoints

All endpoints are available at `https://emoji-app.com/api/`:

- `GET /emoji/<emoji_name>` - Get a specific emoji by name
- `GET /stats` - Get top 10 most used emojis with usage statistics
- `GET /increment/<emoji_name>` - Record a copy event for an emoji

## Rate Limits

The API is free to use with reasonable rate limits. Please contact us if you need higher limits for your application.

## For Developers

If you want to run your own instance or contribute to the project, check out our [Developer Guide](DEVELOPER.md). 