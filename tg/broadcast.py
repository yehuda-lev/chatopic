import os
import time

from pyrogram import Client, types
from pyrogram.errors import PeerIdInvalid, FloodWait, UserIsBlocked, BadRequest, InputUserDeactivated

from db import filters as db_filters
from tg.strings import resolve_msg


# in the admin want to send message for everyone
def get_message_for_subscribe(_, msg: types.Message):
    if msg.command:
        if msg.command[0] == 'send':
            msg.reply(text=resolve_msg(key='REQUEST_SEND'),
                      reply_markup=types.ForceReply(selective=True,
                                                    placeholder=resolve_msg(key='REQUEST_SEND_BY_KEYBOARD')))
    elif isinstance(msg.reply_to_message.reply_markup, types.ForceReply):
        msg.reply(reply_to_message_id=msg.id, text=resolve_msg(key='ASK_SEND'),
                  reply_markup=types.InlineKeyboardMarkup(
                      [[
                          types.InlineKeyboardButton(text=resolve_msg(key='YES_SEND'), callback_data='send_message'),
                          types.InlineKeyboardButton(text=resolve_msg(key='NO_SEND'), callback_data='un_send_message')
                      ]]))


def send_message(c: Client, cbd: types.CallbackQuery):
    tg_id = cbd.from_user.id
    msg_id = cbd.message.id
    reply_msg_id = cbd.message.reply_to_message.id
    if cbd.data == 'un_send_message':
        c.send_message(chat_id=tg_id, text=resolve_msg(key='MSG_NOT_SEND'))
        c.delete_messages(chat_id=tg_id, message_ids=msg_id)

    elif cbd.data == 'send_message':

        log_file = open('logger.txt', 'a+', encoding='utf-8')
        users = db_filters.get_all_users()
        if len(users) < 1:
            c.send_message(chat_id=cbd.from_user.id, text=resolve_msg(key='NOT_SUBSCRIBES'))
            c.delete_messages(chat_id=cbd.from_user.id, message_ids=cbd.message.id)
            return

        sent = 0
        failed = 0

        c.send_message(chat_id=tg_id, text=resolve_msg(key='SEND_BROADCAST').format(len(users)))
        progress = c.send_message(chat_id=tg_id, text=resolve_msg(key='AMOUNT_USERS').format(sent))

        for chat in users:
            try:
                c.copy_message(chat_id=int(chat), from_chat_id=tg_id,
                               message_id=reply_msg_id)
                sent += 1

                c.edit_message_text(chat_id=tg_id, message_id=progress.id,
                                    text=resolve_msg(key='AMOUNT_USERS').format(sent))

                log_file.write(f"sent to {chat} \n")

                time.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)

            except FloodWait as e:
                print(e)
                time.sleep(e.value)

            except InputUserDeactivated:
                db_filters.change_active(tg_id=chat, active=False)
                log_file.write(f"user {chat} is Deactivated\n")
                failed += 1
                continue

            except UserIsBlocked:
                db_filters.change_active(tg_id=chat, active=False)
                log_file.write(f"user {chat} Blocked your bot\n")
                failed += 1
                continue

            except PeerIdInvalid:
                db_filters.change_active(tg_id=chat, active=False)
                log_file.write(f"user {chat} IdInvalid\n")
                failed += 1
                continue

            except BadRequest as e:
                db_filters.change_active(tg_id=chat, active=False)
                log_file.write(f"BadRequest: {e} :{chat}")
                failed += 1
                continue

        c.delete_messages(chat_id=tg_id, message_ids=msg_id)

        text_done = resolve_msg(key='STATS_SEND')\
            .format(users=len(users), sent=sent, failed=failed)

        log_file.write('\n\n' + text_done + '\n')

        c.send_message(chat_id=tg_id, text=text_done)

        log_file.close()
        try:
            c.send_document(chat_id=tg_id, document='logger.txt')
        except Exception as e:
            c.send_message(chat_id=tg_id, text=str(e))
        finally:
            os.remove('logger.txt')
