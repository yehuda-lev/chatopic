from typing import Optional

from pony.orm import db_session, select
from db.tables import Users, Ids


# @db_session
# def show_all_user(tg_id: int): # del
#     return select(i for i in Users if i.tg_id == tg_id).show()


@db_session
def get_user_from_tg_id(tg_id: int):
    return Users.get(tg_id=str(tg_id))


@db_session
def get_user_from_topic(topic_id: int):
    return Users.get(topic_id=topic_id)

@db_session
def is_tg_id_exists(tg_id: int) -> bool:
    return Users.exists(tg_id=str(tg_id))


def get_topic_id(tg_id: int):
    if get_user_from_tg_id(tg_id=tg_id) is None:
        return None
    return get_user_from_tg_id(tg_id=tg_id).topic_id


def get_tg_id(topic_id: int):
    if get_user_from_topic(topic_id=topic_id) is None:
        return None
    return get_user_from_topic(topic_id=topic_id).tg_id


@db_session
def create_user(tg_id: int, topic_id: int, name_user: Optional[str], bio_user: Optional[str]):
    return Users(tg_id=str(tg_id), topic_id=topic_id, name_user=name_user, bio_user=bio_user)


# @db_session
# def get_topic_msg_id_from_msg_tg_id(tg_id: int, msg_id):
#     return Ids.get()