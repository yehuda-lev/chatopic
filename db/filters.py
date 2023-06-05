from typing import Optional

from pony.orm import db_session, select, delete
from db.tables import TgGroup, TgTopic, TgUser, Message, Admin


@db_session
def check_if_have_a_group() -> bool:
    return TgGroup.exists()


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
    print(f'added group: name={name}, id={group_id}')
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
def get_my_group() -> None | str:
    try:
        return select(i.id for i in TgGroup)[:][0]
    except IndexError:
        return None


@db_session
def get_user_by_tg_id(tg_id: int) -> TgUser:
    return TgUser.get(id=str(tg_id))


@db_session
def change_protect(tg_id: int, is_protect: bool):
    user = TgUser.get(id=str(tg_id))
    user.protect = is_protect


@db_session
def change_banned(tg_id: int, is_banned: bool):
    user = TgUser.get(id=str(tg_id))
    user.ban = is_banned


@db_session
def get_topic_by_topic_id(topic_id: int) -> TgTopic:
    return TgTopic.get(id=topic_id)


@db_session
def get_user_by_topic_id(topic_id: int) -> TgUser:
    return get_topic_by_topic_id(topic_id).user


@db_session
def create_message(tg_id_or_topic_id: int, is_topic_id: bool, user_msg_id: int, topic_msg_id: int):
    if is_topic_id:
        topic_id, tg_id = tg_id_or_topic_id, get_user_by_topic_id(topic_id=tg_id_or_topic_id).id
    else:
        tg_id, topic_id = tg_id_or_topic_id, get_user_by_tg_id(tg_id=tg_id_or_topic_id).topic.id
    return Message(tg_id=str(tg_id), topic_id=topic_id, user_msg_id=user_msg_id, topic_msg_id=topic_msg_id)


@db_session
def get_user_by_user_msg_id(tg_id: int, msg_id: int) -> Message:
    """
    tg_id + msg_id > message
    """

    return Message.get(tg_id=str(tg_id), user_msg_id=msg_id)


@db_session
def get_topic_msg_id_by_user_msg_id(tg_id: int, msg_id: int) -> Optional[int]:
    """
    tg_id + msg_id > topic.msg_id
    """

    user = get_user_by_user_msg_id(tg_id=tg_id, msg_id=msg_id)
    if user is None:
        return None
    return user.topic_msg_id


@db_session
def get_user_by_topic_msg_id(topic_id: int, msg_id: int) -> Message:
    """
    topic + msg_id > message
    """

    return Message.get(topic_id=topic_id, topic_msg_id=msg_id)


# new
@db_session
def get_user_by_topic_msg_id2(msg_id: int) -> Message:
    """
    msg_id (topic) > message
    """

    return Message.get(topic_msg_id=msg_id)


@db_session
def is_user_active(tg_id: int) -> bool:
    return get_user_by_tg_id(tg_id).active


@db_session
def change_active(tg_id: int, active: bool):
    user = get_user_by_tg_id(tg_id)
    user.active = active


@db_session
def get_all_users() -> list[int]:
    return select(int(i.id) for i in TgUser if not i.ban and i.active)[:]


@db_session
def del_all():
    # Warning ⚠
    delete(u for u in TgUser)
    delete(g for g in TgGroup)
    print('delete all ⚠')
