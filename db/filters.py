from typing import Optional

from pony.orm import db_session, select
from db.tables import TgGroup, TgTopic, TgUser


# @db_session
# def show_all_user(tg_id: int): # del
#     return select(i for i in Users if i.tg_id == tg_id).show()


@db_session
def get_user_from_tg_id(tg_id: int):
    return TgUser.get(tg_id=str(tg_id))


@db_session
def get_user_from_topic(topic_id: int):
    return TgUser.get(topic_id=topic_id)

@db_session
def is_tg_id_exists(tg_id: int) -> bool:
    return TgUser.exists(tg_id=str(tg_id))

@db_session
def is_topic_id_exists(topic_id: int) -> bool:
    return TgUser.exists(topic_id=topic_id)


def get_topic_id(tg_id: int):
    if get_user_from_tg_id(tg_id=tg_id) is None:
        return None
    return get_user_from_tg_id(tg_id=tg_id).topic_id


def get_tg_id(topic_id: int):
    if get_user_from_topic(topic_id=topic_id) is None:
        return None
    return get_user_from_topic(topic_id=topic_id).tg_id


@db_session
def create_user(tg_id: int, group_id: int, topic_id: int, name: Optional[str]) -> TgUser:
    group = TgGroup(id=str(group_id))
    topic = TgTopic(id=topic_id, group=group, name=name)
    return TgUser(id=str(tg_id), topic=topic, group=group)

@db_session
def get_topic_msg_id_from_user_msg_id(tg_id: int, msg_id: int):
    return Ids.get(tg_id=str(tg_id), user_msg_id=msg_id).topic_msg_id


@db_session
def get_tg_id_msg_id_from_topic_msg_id(topic_id: int, msg_topic_id: int):
    return Ids.get(topic_id=topic_id, topic_msg_id=msg_topic_id).user_msg_is


@db_session
def create_ids(tg_id: int, topic_id: int, user_msg_id: int, topic_msg_id):
    return Ids(tg_id=str(tg_id), topic_id=topic_id, user_msg_id=user_msg_id, topic_msg_id=topic_msg_id)