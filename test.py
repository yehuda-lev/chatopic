from pyrogram import Client, filters, types
from pyrogram.raw import functions
from pyrogram.raw.functions.channels import create_forum_topic
from pyrogram.types import InlineKeyboardButton, KeyboardButton, Message
from db import filters


# from config import Config
import pyrogram.raw
from pyrogram.raw.types import (KeyboardButtonRequestPeer, RequestPeerTypeUser, ReplyKeyboardMarkup,
                                KeyboardButtonRow, UpdateNewMessage, RequestPeerTypeChat, RequestPeerTypeBroadcast,
                                ChatAdminRights, UpdateChannelUserTyping, UpdateChatParticipantAdd,
                                UpdateNewChannelMessage, InputChannel, Channel)
from pyrogram.raw.functions.messages import SendMessage
from pyrogram.raw.base import ChatAdminRights as Base_ChatAdminRights, KeyboardButton, InputPeer

from db.filters import is_tg_id_exists

# import pyrogram.raw.functions.channels.create_forum_topic
bot = Client("my_bot")


def teeee(_, __, msg: types.Message) -> bool:
    print(msg.chat.type.PRIVATE)
    if msg.chat.type.PRIVATE:
        return True
    return False


async def create_topic(cli: Client, msg: Message):
    name = msg.from_user.first_name + (" " + msg.from_user.last_name if msg.from_user.last_name else "")
    peer = await cli.resolve_peer(msg.chat.id)
    from pyrogram.raw.types import InputChannel
    create = await cli.invoke(functions.channels.CreateForumTopic(
        channel=InputChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
        title=name,
        random_id=1000,
        icon_color=None,
        icon_emoji_id=5312016608254762256,
        send_as=None
        )
    )
    return create.updates[1].message

@bot.on_message()
async def is_user_exists(c: Client, msg: Message):
    name = msg.from_user.first_name + (" " + msg.from_user.last_name if msg.from_user.last_name else "")
    tg_id = msg.from_user.id
    print(filters.is_tg_id_exists(tg_id=tg_id))
    if filters.is_tg_id_exists(tg_id=tg_id):
        return
    else:
        create = await create_topic(cli=c, msg=msg)
        group_id = int("-100" + str(create.peer_id.channel_id))
        topic_id = create.id
        print(group_id, topic_id, tg_id, msg.chat.id)
        filters.create_user(tg_id=tg_id, group_id=group_id, topic_id=topic_id, name=name)


# @bot.on_message(filters.text)
async def start(c: Client, msg: types.Message):
    # print("################\n\n\n\n\n\n\n#############")
    # print(m)
    if msg.reply_to_top_message_id:
        print(f"id: {msg.id}, chat: {msg.chat.id} {msg.chat.type}, reply_top: {msg.reply_to_top_message_id}")
    else:
        print(f"id: {msg.id}, chat: {msg.chat.id} {msg.chat.type}, reply: {msg.reply_to_message_id}")
    # test = await create_topic(cli=c, msg=msg)
    # print(test)
    name = msg.from_user.first_name + (" " + msg.from_user.last_name if msg.from_user.last_name else "")
    print(name)



    # peer = await bot.resolve_peer(m.chat.id)

    # peer = await bot.resolve_peer(m.chat.id)
    #
    # create_topic = await bot.invoke(functions.channels.CreateForumTopic(
    #     channel=InputChannel(channel_id=peer.channel_id, access_hash=peer.access_hash),
    #     title="test",
    #     random_id=1000,
    #     icon_color=None,
    #     icon_emoji_id=5312016608254762256,
    #     send_as=None
    #     )
    # )
    # print(create_topic)
    # print("############")
    # print(create_topic.updates)
    # print(create_topic.updates[1])
    # print("@@@@@")
    # print(create_topic.updates[1].message)

    # print(create_topic.updates[1].message.id)
    # print(create_topic.updates[1].message.peer_id.channel_id)
    # print(create_topic.updates[1].message.action.title)
    # print(create_topic.updates[1].message.action.icon_color)
    # print(create_topic.updates[1].message.action.icon_emoji_id)



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