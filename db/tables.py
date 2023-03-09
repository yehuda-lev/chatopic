from pony.orm import (Database, Required, Optional)

db = Database()


class Manager(db.Entity):
    admin_id = Required(str, unique=True)
    group_id = Required(str, unique=True)


class Users(db.Entity):
    tg_id = Required(str, unique=True)
    topic_id = Required(int, unique=True)
    name_user = Optional(str)
    bio_user = Optional(str)


class Ids(db.Entity):
    tg_id = Required(str, unique=True)
    topic_id = Required(int, unique=True)
    user_msg_id = Required(int)
    topic_msg_id = Required(int)




db.bind(provider='sqlite', filename='chat_bot.sqlite', create_db=True)
db.generate_mapping(create_tables=True)