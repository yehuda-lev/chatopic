from pyrogram import Client, filters, types
from pyrogram.raw import functions
from pyrogram.raw.functions.channels import create_forum_topic
from pyrogram.types import InlineKeyboardButton, KeyboardButton, Message
from db import filters

import pyrogram.raw
from pyrogram.raw.types import (KeyboardButtonRequestPeer, RequestPeerTypeUser, ReplyKeyboardMarkup,
                                KeyboardButtonRow, UpdateNewMessage, RequestPeerTypeChat, RequestPeerTypeBroadcast,
                                ChatAdminRights, UpdateChannelUserTyping, UpdateChatParticipantAdd,
                                UpdateNewChannelMessage, InputChannel, Channel)
from pyrogram.raw.functions.messages import SendMessage
from pyrogram.raw.base import ChatAdminRights as Base_ChatAdminRights, KeyboardButton, InputPeer

from db.filters import is_tg_id_exists, get_topic_id_by_tg_id, get_group_by_tg_id, get_my_group

# import pyrogram.raw.functions.channels.create_forum_topic
bot = Client("my_bot")


def teeee(_, __, msg: types.Message) -> bool:
    print(msg.chat.type.PRIVATE)
    if msg.chat.type.PRIVATE:
        return True
    return False

    # @bot.on_message(filters.text)
# async def start(c: Client, msg: types.Message):

    # print("#######################\n", peer)
    # peer1 = m.chat.id
    # peer = await bot.resolve_peer(m.chat.id)
    # await bot.invoke(
    #     SendMessage(peer=peer, message="test", random_id=bot.rnd_id(),
    #                 reply_markup=ReplyKeyboardMarkup(rows=[
    #                     KeyboardButtonRow(
    #                         buttons=[
    #                             KeyboardButtonRequestPeer(text='Request Peer User',
    #                                                       button_id=1,
    #                                                       peer_type=RequestPeerTypeUser()),
    #                             KeyboardButtonRequestPeer(text='Request Peer Chat',
    #                                                       button_id=3,
    #                                                       peer_type=RequestPeerTypeChat(
    #                                                           has_username=False, forum=True, bot_participant=True)),
    #                             KeyboardButtonRequestPeer(text='Request Peer BroadCast',
    #                                                       button_id=4,
    #                                                       peer_type=RequestPeerTypeBroadcast())
    #                         ]
    #                     )
    #
    #                 ],resize=False))
    # )






# @bot.on_raw_update()
# async def raw(client: Client, update: Channel, users, chats):
#     print(update)


# @bot.on_raw_update()
# async def raw(client: Client, update: pyrogram.raw.types.ForumTopic, users, chats):
#     print("########")
#     print(update)




# peer = await bot.resolve_peer(m.chat.id)
#
# test = bot.invoke(functions.channels.CreateForumTopic(
#     channel=InputChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
#     title="test",
#     random_id=100,
#     icon_color=None,
#     icon_emoji_id=5312016608254762256,
#     send_as=InputPeer()
#     )
# )

# result = bot.invoke(
#     functions.phone.EditGroupCallParticipant(
#         call=update.call,
#         participant=bot.resolve_peer(participant.peer.user_id),
#         muted=False
#     )
#     )




bot.run()