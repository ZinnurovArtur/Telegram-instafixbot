# Telegram-instafixbot
Telegram example for InstaFix without adding dd 

Thanks [InstaFix](http://handlebarsjs.com/](https://github.com/Wikidepia/InstaFix)) for developing this project 
and [python-telegram-bot](https://docs.python-telegram-bot.org/en/v21.9/index.html) for adding additional tools

This is an example of a bot which allows Instagram user's to see reels without adding additional URL.  <img width="439" alt="Снимок экрана 2024-12-11 в 15 21 28" src="https://github.com/user-attachments/assets/706f23c1-3a93-4bf8-89e9-9fc820f0f938" />


https://github.com/user-attachments/assets/5e83fc8d-f518-4829-99ed-405a19701f0e

# Installation
## Locally - using Docker
1. Generate token from [BotFather](https://telegram.me/BotFather)
2. Create the `.env` file for storing the Telegram token - use `.env.dist` as example
3. Use `SERVER_URL=https://www.ddinstagram.com/` for testing and development purposes if you do not have your server url yet
1. `docker build --tag insta-bot  . `
2. `docker run -d -p 5001:5000 insta-bot`

## Cloud - using the Fly.io 
1. Generate a token from [BotFather](https://telegram.me/BotFather)
2. Use an example from [InstaFix](http://handlebarsjs.com/](https://github.com/Wikidepia/InstaFix)) of deploying your own ddinstagram
3. For the deploying your telegram bot using fly.io install `flyctl` and run `fly launch`
4. Use `fly.toml` config for telegram bot
5. Use `SERVER_URL=<provided from Fly.io>` and put the required env parameters to the Fly.io [secrets](https://fly.io/docs/apps/secrets/)
6. Run `fly deploy`
