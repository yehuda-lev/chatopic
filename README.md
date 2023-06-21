
# Chat Bot with Topics


This bot allows you to chat with people on Telegram conveniently 
and anonymously by correspondence in the group arranged by topic.


## Features

- For every user who sends a message to the bot, a dedicated topic is created, allowing you to communicate with them directly, just like in a regular Telegram chat.

- Each message sent to the bot is forwarded to the topic associated with the user. And vice versa - every message sent in the group on a subject associated with the user - is transmitted to him in a secure manner so that he does not know who sent the original message

- If a user edits their message, the message will also be edited in the linked topic, and a button will be added indicating that the message has been edited. On the other hand, if an admin edits their message in the group, the message will be edited in the linked chat, but the user will not know that the message was edited.

- If a user sends a message Forward with quotes, it will be forwarded to the group with the credit. In contrast, if an admin sends a message Forward with quotes, it will be forwarded to the user without the credit.

- If a user sends a message with buttons, the buttons will be automatically copied, but if there are non-url buttons in the message, they will not be copied.

- You can send any type of message to the bot!

- The identities of the admins in the group are kept secret, and no one can know who the admins are. On the other hand, admins have various tools to identify the users they communicate with.

- Users in the management group can block users or release them from blocking.

- Users in the management group can protect the messages sent in the group or cancel the message protection.

- Users in the management group can delete messages sent to users.

- Send a message to all users in the bot.

- Additional features...

## Installation Instructions

### Prerequisites

- Python 3.10

### Installation

1. Run the following command in the command line:

   ```bash
   git clone https://github.com/yehuda-lev/chat_bot.git
   
2. Create a virtual environment named `venv`:
   ```bash
   python3 -m venv venv
   
3. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   
4. Install the required libraries by running the command:

   ```bash
   pip3 install -r requirements.txt

5. Copy the `.env.example` file and create a new file named `.env`:

   ```bash
   cp .env.example .env

6. Edit the `.env` file:

   ```bash
   nano .env
   
7. Fill in the following details:

   - Obtain the `API_ID` and `API_HASH` from [https://my.telegram.org](https://my.telegram.org)
   - Get the `TOKEN` the bot from [https://t.me/BotFather](https://t.me/BotFather)
   - Enter the Telegram user ID of the admin.
   - Choose a language - the bot supports Hebrew (HE) and English (EN).

8. To save the file, press `ctrl + s`, and then `ctrl + x`.

9. Running the bot:

   ```bash
   python3 main.py

# Credit
The code was written by [@Yehudalev](https://t.me/Yehudalev)
