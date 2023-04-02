import pyrogram
from pyrogram import Client
from pyrogram.errors import BadRequest
from pyrogram.raw import functions
from pyrogram.raw import types as raw_types
from pyrogram.types import Message

from db import filters as filters_db
from tg.filters import is_admin


# @app.on_message(pyrogram.filters.command("info") & pyrogram.filters.group)
def get_info_command(c: Client, msg: Message):
    ban = "בשביל לחסום משתמש עליך לשלוח את הפקודה /ban"
    unban = "בשביל לשחרר את החסימה עליך לשלוח את הפקודה /unban"
    protect = "בשביל שהמשתמש לא יוכל להעתיק את ההודעות מעתה ואילך עליך לשלוח את הפקודה /protect"
    unprotect = "בשביל שהמשתמש יוכל לחזור להעתיק הודעות עליך לשלוח את הפקודה /unprotect"
    msg.reply(text=f"{ban}\n{unban}\n{protect}\n{unprotect}")
    return


# @app.on_message(pyrogram.filters.command(["protect", "unprotect"]) & pyrogram.filters.group)
def protect(c: Client, msg: Message):
    topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
    tg_id = filters_db.get_tg_id_by_topic(topic_id=topic_id)
    if msg.command[0] == "protect":
        is_protect = True
    else:
        is_protect = False
    filters_db.change_protect(tg_id=tg_id, is_protect=is_protect)
    msg.reply("Done")


# @app.on_message(pyrogram.filters.command(["ban", "unban"]) & pyrogram.filters.group)
def ban_users(c: Client, msg: Message):
    topic_id = topic if (topic := msg.reply_to_top_message_id) else msg.reply_to_message_id
    tg_id = filters_db.get_tg_id_by_topic(topic_id=topic_id)
    try:
        if msg.command[0] == "ban":
            filters_db.change_banned(tg_id=tg_id, is_banned=True)
            msg.reply("banned \nYou can unban him by sending the /unban command")
            closed = True
        else:
            filters_db.change_banned(tg_id=tg_id, is_banned=False)
            msg.reply("unbanned \nYou can block it again by sending the /ban command")
            closed = False
        peer = c.resolve_peer(msg.chat.id)
        c.invoke(functions.channels.EditForumTopic(
            channel=raw_types.InputChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
            topic_id=topic_id, closed=closed
        )
        )
    except BadRequest as e:
        print(e)


# @app.on_message(pyrogram.filters.command("add_group") & pyrogram.filters.create(is_admin))
async def request_group(c: Client, msg: Message):
    peer = await c.resolve_peer(msg.chat.id)
    await c.invoke(
        functions.messages.SendMessage(peer=peer, message="אנא לחץ על הכפתור למטה כדי להוסיף את הבוט לקבוצה עם נושאים",
                                       random_id=c.rnd_id(),
                                       reply_markup=reply_markup())
    )


def reply_markup():
    return raw_types.ReplyKeyboardMarkup(rows=[
        raw_types.KeyboardButtonRow(
            buttons=[
                raw_types.KeyboardButtonRequestPeer(
                    text='הוסף אותי לקבוצה עם נושאים', button_id=1,
                    peer_type=raw_types.RequestPeerTypeChat(
                        forum=True, bot_participant=True,
                        user_admin_rights=raw_types.ChatAdminRights(
                            add_admins=True, delete_messages=True,
                            manage_topics=True, change_info=True
                        ),
                        bot_admin_rights=raw_types.ChatAdminRights(
                            change_info=True,
                            delete_messages=True,
                            manage_topics=True,
                        )
                    )
                )
            ]
        )
    ], resize=True)


# @app.on_raw_update()
async def create_group(c: Client, update: raw_types.UpdateNewMessage, users, chats):
    if filters_db.check_if_have_a_group():
        return
    if not update.message:
        return
    # print(update)
    try:
        if not update.message.action:
            return
        tg_id = update.message.peer_id.user_id
        if filters_db.is_admin_exists(tg_id=tg_id):
            first_group_id = update.message.action.peer.channel_id
            group_id = int(f"-100{first_group_id}")
            info = await c.get_chat(chat_id=group_id)
            print(info)
            group_name = info.title
            filters_db.create_group(group_id=group_id, name=group_name)
            text = f"הקבוצה [{group_name}](t.me/c/{first_group_id}) נוספה בהצלחה"
            await c.send_message(chat_id=tg_id, reply_to_message_id=update.message.id, text=text,
                                 reply_markup=pyrogram.types.ReplyKeyboardRemove(selective=True))
    except AttributeError as e:
        print(e)
        # await c.send_message(chat_id=tg_id, reply_to_message_id=update.message.id,
        #                      text="הבוט בתחזוקה אנא חזור שנית בהמשך היום")
        return
