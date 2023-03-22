from typing import Optional

from pony.orm import db_session, select
from db.tables import TgGroup, TgTopic, TgUser, Message, Admin


# @db_session
# def show_all_user(tg_id: int): # del
#     return select(i for i in Users if i.tg_id == tg_id).show()
@db_session
def check_if_have_a_group() -> bool:
    group = select(i for i in TgGroup)
    if group:
        return True
    return False

@db_session
def is_group_exists(group_id: int) -> bool:
    return TgGroup.exists(id=str(group_id))

@db_session
def is_admin_exists(tg_id: int) -> bool:
    return Admin.exists(id=str(tg_id))

@db_session
def is_tg_id_exists(tg_id: int) -> bool:
    return TgUser.exists(id=str(tg_id))

@db_session
def is_topic_id_exists(topic_id: int) -> bool:
    return TgTopic.exists(id=topic_id)

@db_session
def create_admin(tg_id: int):
    return Admin(id=str(tg_id))

@db_session
def create_group(group_id: int, name: str):
    return TgGroup(id=str(group_id), name=name)

@db_session
def create_user(tg_id: int, group_id: int, topic_id: int, name: Optional[str]):
    if not is_group_exists(group_id=group_id):
        TgGroup(id=str(group_id))
    if is_tg_id_exists(tg_id=tg_id):
        return
    if is_topic_id_exists(topic_id=topic_id):
        return
    tg_group = TgGroup[str(group_id)]
    topic = TgTopic(id=topic_id, group=str(group_id), name=name)
    return TgUser(id=str(tg_id), topic=topic, group=str(group_id))

@db_session
def get_my_group() -> TgGroup.id:
    return select(i.id for i in TgGroup)[:]

@db_session
def get_user_by_tg_id(tg_id: int):
    return TgUser.get(id=str(tg_id))


def get_group_by_tg_id(tg_id: int):
    user = get_user_by_tg_id(tg_id=tg_id)
    if user is None:
        return None
    return user.group.id


def get_topic_id_by_tg_id(tg_id: int):
    user = get_user_by_tg_id(tg_id=tg_id)
    if user is None:
        return None
    return user.topic.id

def get_is_protect(tg_id: int):
    return get_user_by_tg_id(tg_id=tg_id).protect

@db_session
def change_protect(tg_id: int, is_protect: bool):
    user = TgUser.get(id=str(tg_id))
    user.protect = is_protect

def get_is_banned(tg_id: int):
    return get_user_by_tg_id(tg_id=tg_id).ban

@db_session
def change_banned(tg_id: int, is_banned: bool):
    user = TgUser.get(id=str(tg_id))
    user.ban = is_banned

@db_session
def get_user_by_topic(topic_id: int):
    return TgUser.get(topic=topic_id)


def get_tg_id_by_topic(topic_id: int):
    user = get_user_by_topic(topic_id=topic_id)
    if user is None:
        return None
    return user.id


@db_session
def create_message(tg_id_or_topic_id: int, is_topic_id: bool, user_msg_id: int, topic_msg_id: int):
    if is_topic_id:
        topic_id, tg_id = tg_id_or_topic_id, get_tg_id_by_topic(topic_id=tg_id_or_topic_id)
    else:
        tg_id, topic_id = tg_id_or_topic_id, get_topic_id_by_tg_id(tg_id=tg_id_or_topic_id)
    return Message(tg_id=str(tg_id) ,topic_id=topic_id, user_msg_id=user_msg_id, topic_msg_id=topic_msg_id)


@db_session
def get_user_by_user_msg_id(tg_id: int, msg_id: int):
    return Message.get(tg_id=str(tg_id), user_msg_id=msg_id)

@db_session
def get_topic_msg_id_by_user_msg_id(tg_id: int, msg_id: int):
    user = get_user_by_user_msg_id(tg_id=tg_id, msg_id=msg_id)
    if user is None:
        return None
    return user.topic_msg_id


@db_session
def get_user_by_topic_msg_id(topic_id: int, msg_id: int):
    return Message.get(topic_id=topic_id, topic_msg_id=msg_id)


def get_user_msg_id_by_topic_msg_id(topic_id: int, msg_id: int):
    user = get_user_by_topic_msg_id(topic_id=topic_id, msg_id=msg_id)
    if user is None:
        return None
    return user.user_msg_id