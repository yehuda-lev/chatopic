import logging
import datetime
from typing import List
from db.tables import User, Topic, Message, get_session

_logger = logging.getLogger(__name__)


def create_user_and_topic(*, tg_id: int, name: str, topic_id: int):
    """
    Create user and topic
    :param tg_id: the id of the user
    :param name: the name of the user and the topic
    :param topic_id: the id of the topic
    """

    _logger.debug(f"create user tg_id:{tg_id}, topic_id:{topic_id}")

    with get_session() as session:
        topic = Topic(
            topic_id=topic_id,
            name=name,
            created_at=datetime.datetime.now(),
        )
        user = User(
            tg_id=tg_id,
            name=name,
            topic=topic,
            created_at=datetime.datetime.now(),
        )

        session.add_all((user, topic))
        session.commit()


def get_user_by_tg_id(*, tg_id: int) -> User:
    """
    Get user by tg_id
    :param tg_id: the id of the user
    """

    with get_session() as session:
        return session.query(User).filter(User.tg_id == tg_id).one()


def get_topic_by_topic_id(*, topic_id: int) -> Topic:
    """
    Get topic by topic_id
    :param topic_id: the id of the topic
    """
    with get_session() as session:
        return session.query(Topic).filter(Topic.topic_id == topic_id).one()


def update_user(*, user_tg_id: int, **kwargs):
    """
    Update user
    :param user_tg_id: the id of the user to update
    :param kwargs: the fields to update
    :return:
    """

    _logger.debug(f"update user user_tg_id:{user_tg_id}, kwargs:{kwargs}")

    with get_session() as session:
        session.query(User).filter(User.tg_id == user_tg_id).update(kwargs)
        session.commit()


def update_topic(*, tg_topic_id: int, **kwargs):
    """
    Update topic
    :param tg_topic_id: the id of the topic
    :param kwargs: the fields to update
    :return:
    """

    _logger.debug(f"update topic tg_topic_id:{tg_topic_id}, kwargs:{kwargs}")

    with get_session() as session:
        session.query(Topic).filter(Topic.topic_id == tg_topic_id).update(kwargs)
        session.commit()


# messages


def create_message(*, tg_id: int, topic_id: int, user_msg_id: int, topic_msg_id: int):
    """
    Create message
    :param tg_id: the id of the user
    :param topic_id: the id of the topic
    :param user_msg_id: the id of the message in whatsapp
    :param topic_msg_id: the id of the message in topic
    """
    _logger.debug(
        f"create message tg_id:{tg_id}, topic_id:{topic_id}, user_msg_id:{user_msg_id}, topic_msg_id:{topic_msg_id}"
    )
    with get_session() as session:
        user = session.query(User).filter(User.tg_id == tg_id).one()
        topic = session.query(Topic).filter(Topic.topic_id == topic_id).one()
        message = Message(
            user_msg_id=user_msg_id,
            topic_msg_id=topic_msg_id,
            topic=topic,
            user=user,
            created_at=datetime.datetime.now(),
        )

        session.add(message)
        session.commit()


def get_message(*, topic_msg_id: int | None, user_msg_id: str | None) -> Message:
    """
    Get message by topic_msg_id or user_msg_id
    :param topic_msg_id: the id of the message in topic
    :param user_msg_id: the id of the message in the bot
    :return: the message
    """
    with get_session() as session:
        return (
            session.query(Message)
            .filter((Message.topic_msg_id == topic_msg_id) if topic_msg_id else True)
            .filter((Message.user_msg_id == user_msg_id) if user_msg_id else True)
            .one()
        )


def get_all_users_active() -> List[User]:
    with get_session() as session:
        return session.query(User).filter(User.active == True).all()  # noqa
