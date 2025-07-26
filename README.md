# Telegram-instafixbot

A Telegram bot that allows users to view Instagram reels and posts without additional URL modifications.

Thanks to [InstaFix](https://github.com/Wikidepia/InstaFix) for developing the original project and [python-telegram-bot](https://docs.python-telegram-bot.org/en/v21.9/index.html) for the Telegram bot framework.

## Features

- **Dual Server Fallback**: Uses two different servers for redundancy. If one server fails, it automatically tries the second one.
- **Direct Instagram Download**: When both servers fail, the bot falls back to downloading content directly from Instagram using Instaloader.
- **Session Management**: Saves Instagram sessions to avoid repeated authentication.
- **Media Support**: Handles both videos and photos from Instagram posts and reels.


## Screenshots

<img width="439" alt="Снимок экрана 2024-12-11 в 15 21 28" src="https://github.com/user-attachments/assets/706f23c1-3a93-4bf8-89e9-9fc820f0f938" />

https://github.com/user-attachments/assets/5e83fc8d-f518-4829-99ed-405a19701f0e

## How It Works

1. User sends an Instagram reel/post URL to the bot
2. Bot first tries to convert the URL using the primary server (`SERVER_URL`)
3. If the primary server fails, it tries the secondary server (`SERVER_URL2`)
4. If both servers fail, the bot uses Instaloader to download the content directly from Instagram


## Prerequisites

- **Instagram Account**: You need a valid Instagram account for the Instaloader fallback feature to work
- **Telegram Bot Token**: Generated from [BotFather](https://telegram.me/BotFather)
- **Server URLs**: Two ddinstagram server URLs for the primary and fallback servers

## Installation

### Environment Variables

Create a `.env` file with the following variables:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
SERVER_URL=https://your-primary-ddinstagram-server.com/
SERVER_URL2=https://your-secondary-ddinstagram-server.com/
INSTA_USER=your_instagram_username
INSTA_PASSWORD=your_instagram_password
```

### Locally - using Docker

1. Generate a token from [BotFather](https://telegram.me/BotFather)
2. Create the `.env` file with all required environment variables (use `env.dist` as example)
3. Use `SERVER_URL=https://www.yourserver.com/` for testing and development purposes if you don't have your own server URLs yet
4. Build the Docker image: `docker build --tag insta-bot .`
5. Run the container: `docker run -d -p 5001:5000 insta-bot`

### Cloud Deployment - using Fly.io

1. Generate a token from [BotFather](https://telegram.me/BotFather)
2. Follow the [InstaFix](https://github.com/Wikidepia/InstaFix) guide to deploy your own ddinstagram servers
3. Install `flyctl` and run `fly launch` to deploy your Telegram bot
4. Use the provided `fly.toml` configuration
5. Set all required environment variables in Fly.io [secrets](https://fly.io/docs/apps/secrets/):
   ```bash
   fly secrets set TELEGRAM_TOKEN=your_token
   fly secrets set SERVER_URL=https://your-primary-server.com/
   fly secrets set SERVER_URL2=https://your-secondary-server.com/
   fly secrets set INSTA_USER=your_instagram_username
   fly secrets set INSTA_PASSWORD=your_instagram_password
   ```
6. Deploy: `fly deploy`

## Usage

1. Start the bot with `/start`
2. Send any Instagram reel or post URL (e.g., `https://www.instagram.com/reel/ABC123/`)
3. The bot will automatically process the URL and send back the media content


## Troubleshooting

- **"Trying new server..."**: This means the primary server failed and the bot is trying the secondary server
- **"Okay I will download video..."**: This means both servers failed and the bot is using direct Instagram download
- **Authentication Errors**: Make sure your Instagram credentials are correct and your account is not locked
- **Session Issues**: Delete the session file if you encounter authentication problems


## Contributing

Feel free to submit issues and enhancement requests!

## License
 [MIT](LICENSE)
