
# Chat Bot with Topics


This bot allows you to chat with people on Telegram conveniently 
and anonymously by correspondence in the group arranged by topic.


---
[![שנה לעברית](https://img.shields.io/badge/🇮🇱_לחצו_כאן_לקריאה_בעברית_🇮🇱-blue)](README.he.md)

---

## Features

_Click [here](#installation-instructions) to skip to installing the project_

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


## Commands

### Commands and Functions for Users in the Admin Group

#### Commands
- `/info` - Display information about available commands.
- `/protect` - Activate message protection. Any message sent to the user will be protected from copying, ensuring higher privacy.
- `/unprotect` - Disable message protection. Messages will no longer be protected from copying (disabled by default).
- `/delete` - Delete a message you sent.

#### Functions

- Closing a topic = Blocking a user. Any message sent by the user from now on will not be forwarded to the group.


- Opening a topic = Releasing a user. Any message sent by the user from now on will be forwarded to the group.


- Deleting a topic = Deleting the user's history. The next time the user sends a message, a new topic will be created for them.


### Commands for Admins in the Bot

- `/add_group` - Add a new group. Set the group to which the bot will forward messages.
- `/delete_group` - Delete a group. All messages linked to the group and its users will be permanently deleted from memory.
- `/unban` - Unblock a user using their ID. This command is useful when a user is blocked but their topic is deleted.
- `/send` - Send a message to all subscribed users.


## Installation Instructions

### Prerequisites

- Python 3.10

### Installation

1. Run the following command in the command line:

   ```bash
   git clone https://github.com/yehuda-lev/chatopic.git
   
2. Enter the project:
    ```bash
   cd chatopic
   
3. Create a virtual environment named `venv`:
   ```bash
   python3 -m venv venv
   
4. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   
5. Install the required libraries by running the command:

   ```bash
   pip3 install -r requirements.txt

6. Copy the `.env.example` file and create a new file named `.env`:

   ```bash
   cp .env.example .env

7. Edit the `.env` file:

   ```bash
   nano .env
   
8. Fill in the following details:

   - Obtain the `API_ID` and `API_HASH` from [https://my.telegram.org](https://my.telegram.org)
   - Get the `TOKEN` the bot from [https://t.me/BotFather](https://t.me/BotFather)
   - Enter the Telegram user ID of the admin.
   - Choose a language - the bot supports Hebrew (HE) and English (EN).

9. To save the file, press `ctrl + s`, and then `ctrl + x`.

10. Running the bot:

    ```bash
    python3 main.py

# Credit
The code was written by [@Yehudalev](https://t.me/Yehudalev)
