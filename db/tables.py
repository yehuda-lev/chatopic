from pony.orm import (Database, Required, Optional)

db = Database()

db.bind(provider='sqlite', filename='chat_bot.sqlite', create_db=True)


class Manager(db.Entity):
    admin_id = Required(str, unique=True)
    group_id = Required(str, unique=True)


class Users(db.Entity):
    tg_id = Required(str, unique=True)
    topic_id = Required(str, unique=True)
    name_user = Required(str, Optional)
    bio_user = Required(str, Optional)


db.generate_mapping(create_tables=True)