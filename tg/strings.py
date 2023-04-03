from typing import Optional, Union

from pyrogram.raw.types import User
from pyrogram.types import Message

DEFAULT_LANG = 'he'

dictionary = {
    'start': {
        'he': 'התחלה',
        'en': 'Start'
    },
    'INFO': {
        'he': 'בשביל לחסום משתמש עליך לשלוח את הפקודה /ban\n'
              'בשביל לשחרר את החסימה עליך לשלוח את הפקודה /unban\n'
              'בשביל שהמשתמש לא יוכל להעתיק את ההודעות מעתה ואילך עליך לשלוח את הפקודה /protect\n'
              'בשביל שהמשתמש יוכל לחזור להעתיק הודעות עליך לשלוח את הפקודה /unprotect',
        'en': 'To block a user you must send the command /ban\n'
              'To release the block you must send the command /unban\n'
              'So that the user cannot copy the messages from now on, you must send the command /protect\n'
              'For the user to be able to copy messages again, you must send the command /unprotect'
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
        'he': 'המשתמש נחסם\nלשינוי שלחו את הפקודה /unban',
        'en': 'banned \nYou can unban him by sending the /unban command'
    },
    'UNBAN': {
        'he': 'המשתמש שוחרר\nלשינוי שלחו את הפקודה /ban',
        'en': 'unbanned \nYou can block it again by sending the /ban command'
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
        'he': 'המשתמש חסום \nאתה יכול לבטל את החסימה שלו על ידי שליחת הפקודה /unban',
        'en': 'the user is ban\nYou can unban him by sending the /unban command'
    },
    'INFO_TOPIC': {
        'he': '**פרטים על המשתמש**: \n**שם:** {0}\n**שם משתמש: {1}'
              '\n\u200f**ID:** `{2}` \nלקבלת מידע על הפקודות הנתמכות בצאט אנא שלח את הפקודה /info',
        'en': '**User details**: \n**Name:** {0}\n**Username: {1}'
              '\n**ID:** `{2}` \nFor information about the commands '
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
    }
}


def resolve_msg(key: str, msg_or_user: Union[Message, User], is_raw: bool = False) -> str:
    try:
        return dictionary[key][msg_or_user.from_user.language_code if not is_raw else msg_or_user.lang_code]
    except KeyError:
        try:
            return dictionary[key][DEFAULT_LANG]
        except KeyError:
            return 'Error'
