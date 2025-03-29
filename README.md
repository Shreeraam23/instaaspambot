# Project Name

## Overview
This project automates interactions with a Telegram bot and integrates with an Instagram scraping tool. The bot allows users to scrape Instagram data such as posts, hashtags, bios, and complete user details.

## Features
- **Telegram Bot Integration** using `TeleBot`
- **Instagram Scraper** with `Instaloader`
- **Command-Based Interaction**
  - `/posts` - Scrape all posts
  - `/hashtag` - Scrape posts related to a specific hashtag
  - `/bio` - Scrape Instagram bio
  - `/all` - Scrape all details (posts, bio, followers, followings, etc.)
  - `/stop` - Stop all scraping processes

## Project Structure
```
📂 project-root/
├── 📂 scripts/
│   ├── instagram_scraper.py  # Handles Instagram scraping
│   ├── telegram_bot.py       # Telegram bot logic
│   ├── utils.py              # Utility functions
│
├── 📂 data/
│   ├── scraped_data.json     # Stores extracted data
│
├── requirements.txt          # List of required dependencies
├── config.py                 # Configuration file
├── README.md                 # Project documentation
```

## Installation
### Prerequisites
- Python 3.x
- `pip` (Python package manager)
- Telegram bot token

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/repo-name.git
   cd repo-name
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure the bot:
   - Edit `config.py` to add your Telegram bot token.

## Usage
Run the Telegram bot:
```sh
python scripts/telegram_bot.py
```

The bot will listen for user commands and respond accordingly. Use the commands listed in the Features section.

## Stopping the Bot
Use the `/stop` command to halt all ongoing scraping operations.

## License
This project is licensed under the MIT License.

