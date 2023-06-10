import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_LANG = os.environ['DEFAULT_LANGUAGE'].lower()

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
    'EDIT_CBD': {
        'he': 'הודעה זו נערכה !',
        'en': 'This message has been edited!'
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
    },
    'COMMAND_ADD_GROUP': {
        'he': 'הוספת קבוצה',
        'en': 'Added a group'
    },
    'COMMAND_DELETE_GROUP': {
        'he': '⚠ מחיקת הקבוצה ⚠',
        'en': '⚠ delete the group ⚠'
    },
    'COMMAND_UNBAN': {
        'he': 'שחרר משתמש באמצעות ID',
        'en': 'unban user with ID'
    },
    'COMMAND_SEND': {
        'he': 'שליחת הודעה למנויים',
        'en': 'send message for subscribe'
    },
    'ASK_DEL_GROUP': {
        'he': '**⚠⚠ האם אתה בטוח שברצונך למחוק את הקבוצה?\n'
              'זה אומר שכל ההודעות/הנושאים/משתמשים. יימחקו ! ⚠⚠**',
        'en': '**⚠⚠ Are you sure you want to delete the group?\n'
              'This means all messages/topics/users. will be deleted! ⚠⚠**'
    },
    'DEL_GROUP': {
        'he': 'אוקיי, הקבוצה תימחק.',
        'en': 'OK, the group will be deleted.'
    },
    'NOT_DEL_GROUP': {
        'he': 'אוקיי, הקבוצה לא תימחק.',
        'en': 'OK, the group will not be deleted.'
    },
    'YES_DELETE': {
        'he': '⚠⚠ כן, מחק את הקבוצה. ⚠⚠',
        'en': '⚠⚠ Yes, delete the group. ⚠⚠'
    },
    'NO_DELETE': {
        'he': 'ביטול',
        'en': 'Cancel'
    },
    'REQUEST_SEND': {
        'he': 'אנא שלח את ההודעה אותה תרצה להעביר למנויים',
        'en': 'Please send the message you would like to send to subscribers'
    },
    'REQUEST_SEND_BY_KEYBOARD': {
        'he': 'אנא שלח את ההודעה',
        'en': 'Please send the message'
    },
    'ASK_SEND': {
        'he': 'לשלוח את ההודעה?',
        'en': 'Send the message?'
    },
    'YES_SEND': {
        'he': 'כן',
        'en': 'Yes'
    },
    'NO_SEND': {
        'he': 'לא',
        'en': 'No'
    },
    'MSG_NOT_SEND': {
        'he': 'ההודעה לא תישלח למנויים',
        'en': 'The message will not be sent to subscribers'
    },
    'NOT_SUBSCRIBES': {
        'he': 'אין מנויים',
        'en': 'No subscriptions'
    },
    'SEND_BROADCAST': {
        'he': ' **📣 שולח את ההודעה ל {} מנויים**'
              '\nאנא המתן...',
        'en': '**📣 starting broadcast to:** '
              '`{}` users\nPlease Wait..."'
    },
    'AMOUNT_USERS': {
        'he': 'ההודעה נשלחה ל `{}` משתמשים',
        'en': 'Message Sent To: `{}` users'
    },
    'STATS_SEND': {
        'he': "📣 השידור הושלם\n\n🔸 **כמות המנויים היא:** "
              "{users}\n\n🔹 נשלח ל: {sent} משתמשים\n"
              "🔹 נכשל ב: {failed} משתמשים",

        'en': "📣 Broadcast Completed\n\n🔸 **Total Users in db:** "
              "{users}\n\n🔹 Message sent to: {sent} users\n"
              "🔹 Failed to sent: {failed} users"
    },
    'SYNTAX_ID': {
        'he': 'עליך לשלוח הודעה בצורה כזו:\n "/unban 1234"',
        'en': 'You must send a message like this:\n "/unban 1234"'
    },
    'UNBAN_USER': {
        'he': 'המשתמש {} שוחרר',
        'en': 'the user {} unban'
    },
    'USER_NOT_EXISTS': {
        'he': 'המשתמש {} אינו קיים',
        'en': 'The user {} is not exists'
    }
}


def resolve_msg(key: str) -> str:
    try:
        return dictionary[key][DEFAULT_LANG]
    except KeyError:
        return 'Error'
