import pyrogram
from pyrogram import Client
from pyrogram.errors import BadRequest
from pyrogram.raw.functions.channels import EditForumTopic
from pyrogram.raw.functions.messages import SendMessage
from pyrogram.raw.types import InputChannel, ReplyKeyboardMarkup, KeyboardButtonRow, KeyboardButtonRequestPeer, \
    RequestPeerTypeChat, ChatAdminRights, UpdateNewMessage
from pyrogram.types import Message

from db import filters
from db.filters import get_tg_id_by_topic, change_protect, change_banned, check_if_have_a_group, is_admin_exists


@bot.on_message(pyrogram.filters.command("info") & pyrogram.filters.group)
def get_info_command(c: Client, msg: Message):
    ban = "בשביל לחסום משתמש עליך לשלוח את הפקודה /ban"
    unban = "בשביל לשחרר את החסימה עליך לשלוח את הפקודה /unban"
    protect = "בשביל שהמשתמש לא יוכל להעתיק את ההודעות מעתה ואילך עליך לשלוח את הפקודה /protect"
    unprotect = "בשביל שהמשתמש יוכל לחזור להעתיק הודעות עליך לשלוח את הפקודה /unprotect"
    msg.reply(text=f"{ban}\n{unban}\n{protect}\n{unprotect}")
    return

@bot.on_message(pyrogram.filters.command(["protect", "unprotect"]) & pyrogram.filters.group)
def protect(c: Client, msg: Message):
    topic_id = is_topic(msg)
    if topic_id is False:
        return
    tg_id = get_tg_id_by_topic(topic_id=topic_id)
    if msg.command[0] == "protect":
        is_protect = True
    else:
        is_protect = False
    change_protect(tg_id=tg_id, is_protect=is_protect)
    msg.reply("Done")


@bot.on_message(pyrogram.filters.command(["ban", "unban"]) & pyrogram.filters.group)
def ban_users(c: Client, msg: Message):
    topic_id = is_topic(msg)
    if topic_id is False:
        return
    tg_id = get_tg_id_by_topic(topic_id=topic_id)
    try:
        if msg.command[0] == "ban":
            change_banned(tg_id=tg_id, is_banned=True)
            msg.reply("banned \nYou can unban him by sending the /unban command")
            closed = True
        else:
            change_banned(tg_id=tg_id, is_banned=False)
            msg.reply("unbanned \nYou can block it again by sending the /ban command")
            closed = False
        peer = c.resolve_peer(msg.chat.id)
        c.invoke(EditForumTopic(
            channel=InputChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
            topic_id=topic_id, closed=closed
            )
        )
    except BadRequest as e:
        print(e)



@app.on_message(pyrogram.filters.command("add_group") & pyrogram.filters.create(is_admin))
async def request_group(c: Client, msg: Message):
    peer = await bot.resolve_peer(msg.chat.id)
    await bot.invoke(
        SendMessage(peer=peer, message="אנא לחץ על הכפתור למטה כדי להוסיף את הבוט לקבוצה עם נושאים",
                    random_id=bot.rnd_id(),
                    reply_markup=ReplyKeyboardMarkup(rows=[
                        KeyboardButtonRow(
                            buttons=[
                                KeyboardButtonRequestPeer(
                                    text='הוסף אותי לקבוצה עם נושאים', button_id=1,
                                    peer_type=RequestPeerTypeChat(
                                        forum=True, bot_participant=True,
                                        user_admin_rights=ChatAdminRights(
                                            add_admins=True, delete_messages=True,
                                            manage_topics=True, change_info=True
                                            ),
                                        bot_admin_rights=ChatAdminRights(
                                            change_info=True,
                                            delete_messages=True,
                                            manage_topics=True,
                                            )
                                    )
                                )
                            ]
                        )
                    ], resize=True))
    )

@bot.on_raw_update()
async def create_group(client, update: UpdateNewMessage, users, chats):
    if check_if_have_a_group():
        return
    if not update.message:
        return
    print(update)
    tg_id = update.message.peer_id.user_id
    try:
        if is_admin_exists(tg_id=tg_id):
            first_group_id = update.message.action.peer.channel_id
            group_id = int(f"-100{first_group_id}")
            info = await bot.get_chat(chat_id=group_id)
            print(info)
            group_name = info.title
            filters.create_group(group_id=group_id, name=group_name)
            text = f"הקבוצה [{group_name}](t.me/c/{first_group_id}) נוספה בהצלחה"
            await bot.send_message(chat_id=tg_id, reply_to_message_id=update.message.id,
                                   text=text, reply_markup=pyrogram.types.ReplyKeyboardRemove(selective=True))

    except AttributeError:
        await bot.send_message(chat_id=tg_id, reply_to_message_id=update.message.id,
                               text="הבוט בתחזוקה אנא חזור שנית בהמשך היום")
        return
