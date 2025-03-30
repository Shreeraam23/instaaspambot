# Instagram Spam Bot (telegram version)

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
Here’s a professional and user-friendly README for your second project, tailored to the provided code. This README is designed to help anyone set up and use your "Instagram Multiple Message Sender" script effectively.

---

# Instagram Spam Bot (Basic v1 python version)

A Python script that allows you to send multiple direct messages (DMs) to an Instagram user or group using the `instagrapi` library. This command-line tool supports 2FA authentication and includes robust error handling and logging for a smooth experience.

---

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

---

## Features
- **Flexible Messaging**: Send multiple custom messages to a single user or group.
- **2FA Support**: Handles Instagram two-factor authentication with OTP prompts.
- **Target Selection**: Send messages to either a user (by username) or a group (by thread ID).
- **Error Handling**: Comprehensive try-catch blocks for login, connection, and sending errors.
- **Logging**: Detailed logs saved to `instagram_message_sender.log` and printed to the console.
- **Delay Management**: Built-in random delays (1-3 seconds) to avoid rate limits.

---

## Prerequisites
- **Python 3.8+**: Ensure Python is installed on your system.
- **Instagram Account**: You’ll need a valid Instagram username and password.
- **Target Info**: 
  - For users: Know the target username.
  - For groups: Know the group thread ID (found in the Instagram group chat URL).

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/instagram-message-sender.git
   cd instagram-message-sender
   ```

2. **Install Dependencies**:
   Install the required Python package:
   ```bash
   pip install instagrapi
   ```
   Alternatively, if you create a `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   (Contents of `requirements.txt`: `instagrapi`)

---

## Usage

1. **Run the Script**:
   Start the script from your terminal:
   ```bash
   python main.py
   ```

2. **Follow the Prompts**:
   - Enter your Instagram username and password.
   - If 2FA is enabled, provide the verification code when prompted.
   - Choose to send messages to a user or group.
   - Input your messages (type `DONE` to finish).
   - Confirm to send the messages.

3. **Check Logs**:
   - Logs are saved to `instagram_message_sender.log` in the project directory and also displayed in the terminal.

### Example Run
```
Instagram Multiple Message Sender
--------------------------------
Enter your Instagram username: myusername
Enter your Instagram password: [hidden input]

Choose where to send messages:
1. Send to a user
2. Send to a group
Enter your choice (1 or 2): 1
Enter target username: targetuser

Enter the messages you want to send (type 'DONE' on a new line when finished):
> Hello there!
> How are you?
> DONE

About to send 2 messages to user targetuser
Are you sure you want to proceed? (yes/no): yes
```

---

## How It Works

1. **Login**: Authenticate with Instagram using your credentials, handling 2FA if required.
2. **Target Selection**: Choose a user (by username) or group (by thread ID) to message.
3. **Message Input**: Enter multiple messages interactively, ending with `DONE`.
423. **Sending**: Messages are sent with random delays to avoid Instagram’s rate limits, with full error logging.

### Log Output
Logs are written to both the console and `instagram_message_sender.log`. Example:
```
2025-03-30 10:00:00,123 - __main__ - INFO - Attempting to login as myusername
2025-03-30 10:00:01,456 - __main__ - INFO - Login successful!
2025-03-30 10:00:02,789 - __main__ - INFO - Sent message 1: Hello there!...
```

---

## Contributing

Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Submit a pull request.

Suggestions:
- Add retry logic for connection errors.
- Implement challenge resolution for `ChallengeRequired` exceptions.
- Add a config file for default settings.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Credits

Created by [Your Name] - A simple tool for Instagram messaging enthusiasts!

---

### Notes
- Replace `your-username` in the clone URL with your GitHub username.
- Be cautious with Instagram automation—excessive use may lead to temporary or permanent account restrictions.
- The script currently lacks session persistence; each run requires a new login.

Let me know if you’d like to adjust anything or add more details!
