from pony.orm import (Database, Required, Optional, PrimaryKey, Set)

db = Database()

class TgGroup(db.Entity):
    _table_ = 'tg_group'
    id = PrimaryKey(str)
    name = Optional(str)
    topics = Set(lambda: TgTopic, reverse='group')
    admins = Set(lambda: TgUser, reverse='group')


class TgTopic(db.Entity):
    _table_ = 'tg_topic'
    id = PrimaryKey(int)
    group = Required(TgGroup, reverse='topics')
    name = Required(str)
    user = Optional(lambda: TgUser, reverse='topic')
    messages = Set(lambda: Message, reverse='topic_id')


class TgUser(db.Entity):
    _table_ = 'tg_user'
    id = PrimaryKey(str)
    topic = Optional(TgTopic, reverse='user')
    group = Optional(TgGroup, reverse='admins')
    messages = Set(lambda: Message, reverse='tg_id')


class Message(db.Entity):
    _table_ = 'tg_message'
    tg_id = Required(TgUser)
    topic_id = Required(TgTopic)
    user_msg_id = Required(int)
    topic_msg_id = Required(int)


db.bind(provider='sqlite', filename='chat_bot.sqlite', create_db=True)
db.generate_mapping(create_tables=True)