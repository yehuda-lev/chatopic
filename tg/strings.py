DEFAULT_LANG = 'he'

dictionary = {
    'start': {
        'he': 'התחלה',
        'en': 'Start'
    },
    'INFO': {
        'he': 'בשביל לחסום משתמש עליך לסגור את הנושא. \n'
              'בשביל לשחרר את החסימה עליך לפתוח את הנושא. \n\n'
              'בשביל שהמשתמש לא יוכל להעתיק את ההודעות מעתה ואילך עליך לשלוח את הפקודה /protect\n'
              'בשביל שהמשתמש יוכל לחזור להעתיק הודעות עליך לשלוח את הפקודה /unprotect \n\n'
              'בשביל למחוק הודעה בצאט עליך להגיב על ההודעה עם הפקודה /delete',

        'en': 'To block a user you must close the topic. \n'
              'To release the block you must open the topic. \n\n'
              'So that the user cannot copy the messages from now on, you must send the command /protect\n'
              'For the user to be able to copy messages again, you must send the command /unprotect \n\n' 
              'To delete a chat message you must respond to the message with the command /delete',
    },
    'PROTECT': {
        'he': 'בוצע. \nהמשתמש אינו יכול להעתיק את ההודעות עכשיו\nלשינוי שלחו את הפקודה /unprotect',
        'en': 'Done. \nThe user cannot copy the messages now\nTo change send the command /unprotect'
    },
    'UNPROTECT': {
        'he': 'בוצע. \nהמשתמש יכול להעתיק את ההודעות עכשיו\nלשינוי שלחו את הפקודה /protect',
        'en': 'Done. \nThe user can copy the messages now\nTo change send the command /protect'
    },
    'BAN': {
        'he': 'המשתמש נחסם \nלשחרור - פתחו את הנושא (topic).',
        'en': 'The user has been blocked \nTo release - open the topic.'
    },
    'UNBAN': {
        'he': 'המשתמש שוחרר \nלחסימה - סגרו את הנושא (topic).',
        'en': 'The user has been released \nfor blocking - close the topic.'
    },
    'REQUEST': {
        'he': 'אנא לחץ על הכפתור למטה כדי להוסיף את הבוט לקבוצה עם נושאים',
        'en': 'Please click the button below to add the bot to a themed group'
    },
    'REQUEST_IN_GROUP': {
        'he': 'הפקודה הזאת עובדת בפרטי בלבד',
        'en': 'This command only works in private'
    },
    'REQUEST_BUTTON': {
        'he': 'הוסף אותי לקבוצה עם נושאים',
        'en': 'Add me to a group with topics'
    },
    'GROUP_ADD': {
        'he': 'הקבוצה {0} נוספה בהצלחה',
        'en': 'Group {0} successfully added'
    },
    'USER_IS_BANNED': {
        'he': 'המשתמש חסום \nאתה יכול לבטל את החסימה שלו על ידי פתיחת הנושא (topic)',
        'en': 'The user is blocked \nYou can unblock him by opening the topic'
    },
    'INFO_TOPIC': {
        'he': '**פרטים על המשתמש**: \n**שם:** {0}\n**שם משתמש: {1}'
              '\n\u200f**ID:** `{2}` '
              '\n\u200f[#{3}](tg://openmessage?user_id={4})'
              '\nלקבלת מידע על הפקודות הנתמכות בצאט אנא שלח את הפקודה /info',
        'en': '**User details**: \n**Name:** {0}\n**Username: {1}'
              '\n**ID:** `{2}` '
              '\n\u200f[#{3}](tg://openmessage?user_id={4})'
              '\nFor information about the commands '
              'supported in chat please send the command /info'
    },
    'IS_ADMIN': {
        'he': 'אינך מנהל',
        'en': 'You are not a manager'
    },
    'GROUP_NOT_EXISTS': {
        'he': 'אין עדיין קבוצה, אנא שלח את הפקודה /add_group',
        'en': 'No group yet, please send the command /add_group'
    },
    'BOT_NOT_WORKING': {
        'he': 'הבוט לא פועל עדיין אנא חזור שוב בהמשך',
        'en': 'The bot is not working yet please come back later'
    },
    'EDIT': {
        'he': 'נערך',
        'en': 'Edited'
    },
    'COMMAND_INFO': {
        'he': 'מידע על הפעולות בצאט',
        'en': 'Info about the actions in the chat'
    },
    'COMMAND_DELETE': {
        'he': 'מחיקת הודעה בצאט',
        'en': 'delete message in chat'
    },
    'COMMAND_PROTECT': {
        'he': 'לחסום העתקת הודעות',
        'en': 'Block copying of messages'
    },
    'COMMAND_UNPROTECT': {
        'he': 'לאפשר העתקת הודעות',
        'en': 'Allow copying of messages'
    }
}


def resolve_msg(key: str) -> str:
    try:
        return dictionary[key][DEFAULT_LANG]
    except KeyError:
        return 'Error'
