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
   
2. להתקנת הספריות הנדרשות הריצו את הפקודה:

   ```bash
   pip3 install -r requirements.txt
   
3. העתיקו את קובץ ה `.env_example` וצרו קובץ חדש בשם `.env`
    ```bash
   cp .env_example .env

4. ערכו את קובץ ה `.env`:
    ```bash
   nano .env
   
5. מלאו את הפרטים הבאים:

   - את ה `API_ID` ואת ה `API_HASH` תוכלו להשיג מ 
   [https://my.telegram.org](https://my.telegram.org)
   - את ה `TOKEN` של הבוט תוכלו לקבל מ
   [https://t.me/BotFather](https://t.me/BotFather)
   - עליכם להכניס את מזהה הטלגרם (ID) של המנהל.
   - בחירת שפה - הבוט תומך בשפה העברית (HE) ובשפה האנגלית (EN).

6. 
    בכדי לשמור את הקובץ לחצו `ctrl + s` ולאחר מכן `ctrl + x`
    
7. יצירת סביבת עבודה ויטואלית `venv`:
   ```bash
   python3 -m venv venv
   
8. הפעלת הסביבה הויטואלית:

   ```bash
   sourve venv/bin/activate
   
9. הרצת הבוט:

   ```bash
   python3 main.py

# קרדיט
הקוד נכתב על ידי
[@Yehudalev](https://t.me/Yehudalev)

</div>
