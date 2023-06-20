# Chat Bot with Topics


## English {#english}


**_[לחץ כאן לגרסה בעברית 🇮🇱](README.md#hebrew)_**


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




---

## עברית {#hebrew}

---

**_[Click here for English version 🇬🇧](README.en.md#english)_**

<div dir="rtl">

# צאט בוט עם נושאים

באמצעות בוט זה תוכלו להתכתב עם אנשים בטלגרם בצורה נוחה ואנונימית
על ידי התכתבות בקבוצה שמחולקת לנושאים.


## תכונות

_לחצו [כאן](#הוראות-התקנה) בכדי לדלג להתקנת הפרויקט_


- על כל משתמש ששולח הודעה לבוט
נוצר נושא מיוחד עבורו וכך תוכלו להתכתב איתו ממש כמו בצאט רגיל בטלגרם.


- כל הודעה שנשלחת לבוט מועברת לנושא המשויך למשתמש.
וכן להפך - כל הודעה שנשלחת בקבוצה בנושא שמשויך למשתמש - 
מועברת אליו בצורה מאובטחת בכדי שהוא לא יידע מי שלח את ההודעה המקורית.


- אם משתמש עורך את ההודעה שלו - 
   ההודעה תיערך גם בנושא המקושר ויתווסף כפתור שאומר שהודעה זו נערכה.
  לעומת זאת אם מנהל בקבוצה עורך את ההודעה שלו - 
 ההודעה תיערך בצאט המקושר אך המשתמש לא יידע שההודעה נערכה.  


- אם משתמש שלח הודעה עם קרדיט היא תועבר לקבוצה עם קרדיט.
 לעומת זאת אם המנהל שלח עם קרדיט ההודעה תועבר למשתמש ללא קרדיט 


- אם משתמש שלח הודעה עם כפתורים - 
  הכפתורים יועתקו אוטומטית אך אם יש בהודעה כפתורים שאינם כפתורי קישור הם לא יועתקו.


- אפשר לשלוח לבוט כל סוג של הודעה !


- זהות המנהלים בקבוצה הינה חסוייה ואיש אינו יכול לדעת מי הם המנהלים.
  לעומת זאת למנהלים יש כלים רבים בכדי לדעת מי מתכתב איתם.


- המשתמשים שבקבוצת הניהול יכולים לחסום את המשתמש/לשחרר את החסימה.


- המשתמשים שבקבוצת הניהול יכולים להגן על ההודעות שנשלחות בקבוצה או לבטל את ההגנת הודעות.


- המשתמשים שבקבוצת הניהול יכולים למחוק הודעות שנשלחו למשתמשים.


- שליחת הודעה לכל המשתמשים בבוט


- פיצרים נוספים...


## פקודות

### פקודות ופונקציות למשתמשים שבקבוצת הניהול

#### פקודות
- `/info` - הצגת מידע על הפקודות הזמינות.
- `/protect` - הפעלת הגנת הודעות. כל הודעה שתישלח למשתמש תהיה מוגנת מהעתקה, וכך תהיה לכם פרטיות גבוהה יותר.
- `/unprotect` - ביטול הגנת ההודעות. הודעות לא יהיו מוגנות מהעתקה (מבוטל כברירת מחדל).
- `/delete` - מחיקת הודעה ששלחתם.

#### פונקציות

- סגירת נושא = חסימת המשתמש. כל הודעה שתשילח מעכשיו מהשתמש לבוט -  לא תועבר לקבוצה


- פתיחת נושא = שחרור המשתמש. כל הודעה שתשילח מעכשיו מהשתמש לבוט - תועבר לקבוצה


- מחיקת נושא = מחיקת ההיסטוריה של המשתמש. פעם הבאה שהמשתמש ישלח הודעה יווצר לו נושא חדש


### פקודות למנהל בבוט

- `/add_group` - הוספת קבוצה חדשה. הגדרת הקבוצה שהבוט יעביר אליה את ההודעות.
- `/delete_group` - מחיקת קבוצה. כל הודעות המקושרות לקבוצה ולמשתמשיה יימחקו מהזיכרון לצמיתות.
- `/unban` - שחרור משתמש מחסימה באמצעות ID.
 פקודה זו נועדה למקרה בו משתמש מוגדר כחסום אך הנושא שלו נמחק.
- `/send` - שליחת הודעה לכל המשתמשים המנויים.

## הוראות התקנה


### דרישות מוקדמות

- Python 3.10

### התקנה


1. הריצו בשורת הפקודה:

   ```bash
   git clone https://github.com/yehuda-lev/chat_bot.git
   
2. יצירת סביבת עבודה ויטואלית `venv`:
   ```bash
   python3 -m venv venv
   
3. הפעלת הסביבה הויטואלית:

   ```bash
   source venv/bin/activate
   
4. להתקנת הספריות הנדרשות הריצו את הפקודה:

   ```bash
   pip3 install -r requirements.txt
   
5. העתיקו את קובץ ה `.env.example` וצרו קובץ חדש בשם `.env`
    ```bash
   cp .env.example .env

6. ערכו את קובץ ה `.env`:
    ```bash
   nano .env
   
7. מלאו את הפרטים הבאים:

   - את ה `API_ID` ואת ה `API_HASH` תוכלו להשיג מ 
   [https://my.telegram.org](https://my.telegram.org)
   - את ה `TOKEN` של הבוט תוכלו לקבל מ
   [https://t.me/BotFather](https://t.me/BotFather)
   - עליכם להכניס את מזהה הטלגרם (ID) של המנהל.
   - בחירת שפה - הבוט תומך בשפה העברית (HE) ובשפה האנגלית (EN).

8. 
    בכדי לשמור את הקובץ לחצו `ctrl + s` ולאחר מכן `ctrl + x`

9. הרצת הבוט:

   ```bash
   python3 main.py

# קרדיט
הקוד נכתב על ידי
[@Yehudalev](https://t.me/Yehudalev)

</div>
