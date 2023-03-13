from typing import Optional

from pony.orm import db_session, select
from db.tables import TgGroup, TgTopic, TgUser, Message


# @db_session
# def show_all_user(tg_id: int): # del
#     return select(i for i in Users if i.tg_id == tg_id).show()


@db_session
def is_group_exists(group_id: int) -> bool:
    return TgGroup.exists(id=str(group_id))


@db_session
def is_tg_id_exists(tg_id: int) -> bool:
    return TgUser.exists(id=str(tg_id))

@db_session
def is_topic_id_exists(topic_id: int) -> bool:
    return TgUser.exists(topic=topic_id)

@db_session
def create_user(tg_id: int, group_id: int, topic_id: int, name: Optional[str]) -> TgUser:
    if not is_group_exists(group_id=group_id):
        TgGroup(id=str(group_id))
    topic = TgTopic(id=topic_id, group=str(group_id), name=name)
    return TgUser(id=str(tg_id), topic=topic, group=str(group_id))


@db_session
def get_user_by_tg_id(tg_id: int):
    return TgUser.get(id=str(tg_id))


def get_group_by_tg_id(tg_id: int):
    if get_user_by_tg_id(tg_id=tg_id) is None:
        return None
    return get_user_by_tg_id(tg_id=tg_id).group.id


def get_topic_id_by_tg_id(tg_id: int):
    if get_user_by_tg_id(tg_id=tg_id) is None:
        return None
    return get_user_by_tg_id(tg_id=tg_id).topic.id


@db_session
def get_user_by_topic(topic_id: int):
    return TgUser.get(topic=topic_id)


def get_tg_id_by_topic(topic_id: int):
    if get_user_by_topic(topic_id=topic_id) is None:
        return None
    return get_user_by_topic(topic_id=topic_id).id


@db_session
def create_message(sender: int, user_msg_id: int, topic_msg_id: int):
    user = get_user_by_tg_id(tg_id=sender)
    return Message(sender=user, user_msg_id=user_msg_id, topic_msg_id=topic_msg_id)

@db_session
def get_user_from_user_msg_id(sender: int, msg_id: int):
    return Message.get(sender=str(sender), user_msg_id=msg_id)

@db_session
def get_topic_msg_id_from_user_msg_id(tg_id: int, msg_id: int):
    return get_user_from_user_msg_id(sender=tg_id, msg_id=msg_id).topic_msg_id


@db_session
def get_tg_id_msg_id_from_topic_msg_id(topic_id: int, msg_id: int):
    return get_user_from_user_msg_id(sender=topic_id, msg_id=msg_id)