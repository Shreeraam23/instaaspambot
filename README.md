# Instagram Spam Bot

A Telegram-controlled bot that allows you to log into multiple Instagram accounts and send direct messages (DMs) to users or groups, either as single messages or random messages from a predefined list. Built with Python, this bot leverages the `instagrapi` library for Instagram interactions and `telebot` for Telegram integration.

---

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

---

## Features
- **Multi-Account Support**: Manage multiple Instagram accounts per Telegram user.
- **Message Spamming**: Send single or random messages to Instagram users or groups.
- **Session Persistence**: Save and reload Instagram sessions to avoid repeated logins.
- **Rate Limit Handling**: Uses a queue and random delays to bypass Instagram API limits.
- **Telegram Interface**: Control everything via simple Telegram commands.
- **2FA Support**: Handles Instagram two-factor authentication with OTP verification.
- **Logging**: Detailed debug logs for troubleshooting (`instagrapi_bot.log`).

---

## Prerequisites
- **Python 3.8+**: Ensure Python is installed on your system.
- **Instagram Account(s)**: You’ll need credentials for the accounts you want to use.
- **Telegram Account**: To interact with the bot.
- **Telegram Bot Token**: Create a bot via [BotFather](https://t.me/BotFather) on Telegram.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/instagram-spam-bot.git
   cd instagram-spam-bot
   ```

2. **Install Dependencies**:
   Install the required Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```
   If there’s no `requirements.txt` yet, install these manually:
   ```bash
   pip install telebot instagrapi
   ```

3. **Set Up Your Environment**:
   - Open `main.py` (or whatever you name the script) in a text editor.
   - Configure the `TELEGRAM_BOT_TOKEN` and `OWNER_IDS` (see [Configuration](#configuration)).

---

## Configuration

Edit the following variables in the script:

- **`TELEGRAM_BOT_TOKEN`**:
  - Get this from [BotFather](https://t.me/BotFather) by creating a new bot.
  - Example: `TELEGRAM_BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"`

- **`OWNER_IDS`**:
  - List of Telegram user IDs allowed to use the bot.
  - To find your Telegram ID, send `/start` to [@userinfobot](https://t.me/userinfobot).
  - Example: `OWNER_IDS = [123456789, 987654321]`

Example configuration:
```python
TELEGRAM_BOT_TOKEN = "your-bot-token-here"
OWNER_IDS = [your-telegram-id-here]
```

---

## Usage

1. **Run the Bot**:
   Start the bot by running the script:
   ```bash
   python main.py
   ```

2. **Interact via Telegram**:
   - Open Telegram and message your bot (the one you created with BotFather).
   - Use the commands below to control it.

3. **Logs**:
   - Check `instagrapi_bot.log` in the project directory for detailed debug information.

---

## Commands

| Command       | Description                                      |
|---------------|--------------------------------------------------|
| `/start`      | Start the bot and see the welcome message.       |
| `/login`      | Log in to an Instagram account.                  |
| `/list`       | List logged-in accounts and send random messages.|
| `/send`       | Send single or random messages to a target.      |
| `/logout`     | Log out from all Instagram accounts.             |
| `/help`       | Display the help message with all commands.      |
| `/credits`    | Show the bot creator’s credits.                  |

### Example Workflow
1. Send `/login`, then provide your Instagram username and password.
2. Use `/send`, choose "yes" for random messages, enter `msg1|msg2|msg3`, select a target, and specify how many times to send.
3. Watch the bot queue and send your messages!

---

## Contributing

Contributions are welcome! Here’s how to get involved:
1. Fork this repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure your code follows Python best practices and include comments where necessary.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Credits

Bot created by Ahmed Bhai (@tipsandgamer) - The mastermind behind this spam machine!

---

### Notes
- Replace `your-username` in the clone URL with your actual GitHub username.
- If you plan to share this publicly, consider adding a `requirements.txt` file with `telebot` and `instagrapi` for easier setup.
- Be cautious with Instagram automation—overuse may lead to account restrictions.

Let me know if you’d like to tweak anything further!
