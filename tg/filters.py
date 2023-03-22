from pyrogram.types import Message

from db.filters import is_admin_exists, check_if_have_a_group


def is_not_raw(_, __, msg: Message) -> bool:
    if msg.text or msg.game or msg.command or msg.photo or msg.document or msg.voice \
            or msg.service or msg.media or msg.audio or msg.video or msg.contact \
            or msg.location or msg.sticker or msg.poll or msg.animation:
        return True
    return False


def is_admin(_, __, msg: Message) -> bool:
    if not is_admin_exists(tg_id=msg.from_user.id):
        msg.reply("אינך מנהל")
        return False
    return True


def is_have_a_group(_, __, msg: Message):
    if not check_if_have_a_group():
        msg.reply("אין עדיין קבוצה, אני שלח את הפקודה /add_group")
        return False
    return True
