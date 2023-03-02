from typing import Optional

from pony.orm import db_session
from db.tables import Users


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
    return get_user_from_tg_id(tg_id=tg_id).topic_id


def get_tg_id(topic_id: int):
    return get_user_from_topic(topic_id=topic_id).tg_id


@db_session
def create_user(tg_id: int, topic_id: int, name_user: Optional[str], bio_user: Optional[str]):
    return Users(tg_id=str(tg_id), topic_id=topic_id, name_user=name_user, bio_user=bio_user)
