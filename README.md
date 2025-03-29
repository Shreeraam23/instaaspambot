# Instagram Auto DM Bot (Controlled via Telegram)

This bot allows you to send automated Instagram DMs using the `instagrapi` library, with a Telegram bot as the control interface. It enables sending messages to multiple recipients while maintaining compliance with rate limits.

## Features
- **Login via Telegram**: Securely log in to your Instagram account through a Telegram bot.
- **Send Mass DMs**: Send messages to multiple users in a controlled manner.
- **Avoid Rate Limits**: Uses delays between actions to reduce detection risk.
- **Easy Setup**: Requires only Python, `instagrapi`, and Telegram Bot API.

## Requirements
- Python 3.8+
- `instagrapi` for Instagram automation
- `pyTelegramBotAPI` for Telegram bot functionality
- `dotenv` (optional) for environment variable management

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up a Telegram bot:
   - Go to [BotFather](https://t.me/BotFather) on Telegram.
   - Create a new bot and get the `BOT_TOKEN`.
   - Update the `.env` file with your token.

4. Set up Instagram credentials securely (DO NOT hardcode them in the script!):
   - Use `.env` file or input them at runtime.

## Usage
1. Start the bot:
   ```bash
   python bot.py
   ```
2. Open Telegram and interact with your bot.
3. Send `/login` to authenticate your Instagram account.
4. Use `/send_message <username> <message>` to send a DM.
5. To send bulk messages, use `/send_bulk <message>` (ensure recipient list is predefined).

## Important Notes
- **Avoid spam!** Instagram may restrict accounts for excessive automated actions.
- **Security**: Do not share credentials publicly or hardcode them in scripts.
- **Use responsibly** to avoid violating Instagram’s policies.

## Contributing
Feel free to submit issues or pull requests to improve the bot.

## License
This project is open-source and available under the MIT License.

