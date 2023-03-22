from pyrogram.types import Message

def is_not_raw(_, __, msg: Message) -> bool:
    if msg.text or msg.game or msg.command or msg.photo or msg.document or msg.voice \
            or msg.service or msg.media or msg.audio or msg.video or msg.contact \
            or msg.location or msg.sticker or msg.poll or msg.animation:
        return True
    return False
