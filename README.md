<div dir="rtl">

# בוט הצ'אט האנונימי של טלגרם

[![רישיון](https://img.shields.io/badge/רישיון-MIT-blue.svg)](https://github.com/yehuda-lev/chat_bot/blob/main/LICENSE)

בוט הצ'אט האנונימי של טלגרם הוא בוט שפותח בשפת פייתון עבור טלגרם. הבוט מאפשר למשתמשים להתכתב באנונימיות ובצורה מסודרת עם משתמשים אחרים באמצעות מערכת קבוצות שמחולקות לפי נושאים.

## תכונות

- כל הודעה שנשלחת לבוט מועברת באופן אוטומטי לנושא המשויך למשתמש.
- לכל משתמש נוצר נושא מיוחד בשבילו, מה שמאפשר התכתבות מסודרת.
- זהות המנהלים בקבוצה הינה חסוייה ואיש אינו יכול לדעת מי הם המנהלים.
  לעומת זאת למנהלים יש כלים בכדי לדעת מי מתכתב איתם.
- המשתמשים שבקבוצת הניהול יכולים לשלוח פקודות כדי לשלוט בבוט.

## פקודות

### פקודות למשתמשים שבקבוצת הניהול

- `/info` - הצגת מידע על הפקודות הזמינות.
- `/protect` - הפעלת הגנת ההודעות. כל הודעה שתישלח למשתמש תהיה מוגנת מהעתקה, וכך יתאפשר פרטיות גבוהה יותר.
- `/unprotect` - ביטול הגנת ההודעות. הודעות לא יהיו מוגנות מהעתקה (התנהגות ברירת המחדל).
- `/delete` - מחיקת הודעה אחרונה שנשלחה על ידי המשתמש.
- `/delete_all` - מחיקת כל הודעות שהמשתמש שלח בעבר.

### פקודות למנהל בבוט

- `/add_group` - הוספת קבוצה חדשה. הגדרת הקבוצה שהבוט יעביר אליה את ההודעות.
- `/delete_group` - מחיקת קבוצה. כל הודעות המקושרות לקבוצה ולמשתמשיה יימחקו מהזיכרון לצמיתות.
- `/unban` - שחרור משתמש מחסימה באמצעות ID, פקודה זו נועדה למקרה בו חסמת משתמש ומחקת את הנושא שלו.
- `/send` - שליחת הודעה לכל המשתמשים המנויים. שימושי לשידור מידע חשוב.

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
   
3. ערכו את קובץ ה ".env":

   - את ה `API_ID` ואת ה `API_HASH` תוכלו להשיג מ- [https://my.telegram.org](https://my.telegram.org)
   - את הטוקן של הבוט תוכלו לקבל מ- [https://t.me/BotFather](https://t.me/BotFather)
   - עליכם להכניס את מזהה הטלגרם (ID) של המנהל.
   - בחירת שפה - הבוט תומך כרגע בשפה העברית (HE) ובשפה האנגלית (EN).

הרצת הבוט:

   ```bash
   python3 main.py

