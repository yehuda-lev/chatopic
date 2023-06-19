from typing import Optional
from pony.orm import db_session, select, delete
from db.tables import TgGroup, TgTopic, TgUser, Message, Admin
from cache_memory import MemoryCache

cache = MemoryCache()


@cache.cachable(cache_name='is_have_a_group')
@db_session
def check_if_have_a_group() -> bool:
    """
    check if have a group
    """

    # print(check_if_have_a_group.__name__)
    return TgGroup.exists()


@cache.cachable(cache_name='group_exists', params='group_id')
@db_session
def is_group_exists(*, group_id: int) -> bool:
    """
    is group exists
    """

    # print(is_group_exists.__name__)
    return TgGroup.exists(id=str(group_id))


@cache.cachable(cache_name='admin_exists', params='tg_id')
@db_session
def is_admin_exists(*, tg_id: int) -> bool:
    """
    is admin exists
    """

    # print(is_admin_exists.__name__)
    return Admin.exists(id=str(tg_id))


@cache.cachable(cache_name='tg_id_exists', params='tg_id')
@db_session
def is_tg_id_exists(*, tg_id: int) -> bool:
    """
    is tg_id exists
    """

    # print(is_tg_id_exists.__name__)

    return TgUser.exists(id=str(tg_id))


@cache.cachable(cache_name='topic_exists', params='topic_id')
@db_session
def is_topic_id_exists(*, topic_id: int) -> bool:
    """
    is topic_id exists
    """

    # print(is_topic_id_exists.__name__)
    return TgTopic.exists(id=topic_id)


@cache.invalidate(cache_name='admin_exists', params='tg_id')
@db_session
def create_admin(*, tg_id: int):
    return Admin(id=str(tg_id))


@db_session
def create_group(*, group_id: int, name: str):

    # del cache
    cache.delete(cache_name='is_have_a_group')
    # print(create_group.__name__)

    # create group
    return TgGroup(id=str(group_id), name=name)


@db_session
def create_user(*, tg_id: int, group_id: int, topic_id: int, name: Optional[str]):

    # del cache
    cache.delete(cache_name='tg_id_exists', cache_id=cache.build_cache_id(tg_id=tg_id))
    # print(create_user.__name__)

    # create user
    tg_group = TgGroup[str(group_id)]
    topic = TgTopic(id=topic_id, group=str(group_id), name=name)
    return TgUser(id=str(tg_id), topic=topic, group=str(group_id))


@db_session
def get_my_group() -> None | str:
    try:
        return select(i.id for i in TgGroup)[:][0]
    except IndexError:
        return None


@cache.cachable(cache_name='tg-users', params='tg_id')
@db_session
def get_user_by_tg_id(*, tg_id: int) -> TgUser:
    """
    get TgUser by tg_id
    """

    # print(get_user_by_tg_id.__name__)
    return TgUser.get(id=str(tg_id))


@cache.invalidate(cache_name='topic_id-tg_user', params='topic_id')
@db_session
def change_protect(*, topic_id: int, is_protect: bool):
    # print(change_protect.__name__)

    user = TgTopic.get(id=topic_id).user
    user.protect = is_protect


@cache.invalidate(cache_name='topic_id-tg_user', params='topic_id')
@db_session
def change_banned(*, topic_id: int, is_banned: bool):
    # print(change_banned.__name__)
    user = TgTopic.get(id=topic_id).user

    # del cache
    tg_id = int(user.id)
    cache.delete(cache_name='tg-users', cache_id=cache.build_cache_id(tg_id=tg_id))

    user.ban = is_banned


@cache.cachable(cache_name='topic_id-tg_user', params='topic_id')
@db_session
def get_user_by_topic_id(*, topic_id: int) -> TgUser:
    """
    get TgUser by topic_id
    """

    # print(get_user_by_topic_id.__name__)
    return TgTopic.get(id=topic_id).user


@db_session
def create_message(tg_id_or_topic_id: int, is_topic_id: bool, user_msg_id: int, topic_msg_id: int):
    if is_topic_id:
        topic_id, tg_id = tg_id_or_topic_id, TgTopic.get(id=tg_id_or_topic_id).user.id
    else:
        tg_id, topic_id = tg_id_or_topic_id, TgUser.get(id=str(tg_id_or_topic_id)).topic.id

    return Message(tg_id=str(tg_id), topic_id=topic_id, user_msg_id=user_msg_id, topic_msg_id=topic_msg_id)


# @cache.cachable(cache_name='topic_msg_id_by_user_msg_id', params=('tg_id', 'msg_id'))
@db_session
def get_topic_msg_id_by_user_msg_id(*, tg_id: int, msg_id: int) -> Optional[int]:
    """
    tg_id + msg_id > topic.msg_id
    """

    # print(get_topic_msg_id_by_user_msg_id.__name__)
    user = Message.get(tg_id=str(tg_id), user_msg_id=msg_id)
    if user is None:
        return None
    return user.topic_msg_id


@cache.cachable(cache_name='user_by_topic_msg_id', params='msg_id')
@db_session
def get_user_by_topic_msg_id(*, msg_id: int) -> Message:
    """
    msg_id (topic) > message
    """

    # print(get_user_by_topic_msg_id.__name__)
    return Message.get(topic_msg_id=msg_id)


@cache.cachable(cache_name='is_active', params='tg_id')
@db_session
def is_user_active(*, tg_id: int) -> bool:
    # print(is_user_active.__name__)

    return TgUser.get(id=str(tg_id)).active


@cache.invalidate(cache_name='is_active', params='tg_id')
@db_session
def change_active(*, tg_id: int, active: bool):
    # print(change_active.__name__)

    user = TgUser.get(id=str(tg_id))
    user.active = active


@db_session
def get_all_users() -> list[int]:
    return select(int(i.id) for i in TgUser if not i.ban and i.active)[:]


@db_session
def del_all():
    """
    delete all DB
    """

    # del cache
    cache.clear()
    # print(del_all.__name__)

    # Warning ⚠
    delete(u for u in TgUser)
    delete(g for g in TgGroup)


@db_session
def del_topic(*, topic_id: int):
    """
    delete topic and user
    """

    topic = TgTopic.get(id=topic_id)
    user = topic.user

    # del cache
    cache.delete(cache_name='tg-users', cache_id=cache.build_cache_id(tg_id=int(user.id)))
    cache.delete(cache_name='tg_id_exists', cache_id=cache.build_cache_id(tg_id=int(user.id)))

    user.delete()

    topic.delete()

