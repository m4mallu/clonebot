import os
import threading
from sqlalchemy import create_engine
from sqlalchemy import Column, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


clone_cancel_key = {}       # Clone cancel status key
clone_btn_count = {}        # Clone button single click actuator key
index_skip_key = {}         # Skip indexing function key
purge_skip_key = {}         # Purge function key

custom_caption = {}         # Custom caption key
master_index = []           # Unique id index of cloning medias (including target chat)
file_types = ["document", "video", "audio", "voice", "photo", "text"]

if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from config import Config

def start() -> scoped_session:
    engine = create_engine(Config.DB_URI, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()
INSERTION_LOCK = threading.RLock()


class Clonebot(BASE):
    __tablename__ = "clonebot"
    id = Column(Numeric, primary_key=True)
    s_chat = Column(Numeric)
    d_chat = Column(Numeric)
    from_id = Column(Numeric)
    to_id = Column(Numeric)
    s_chat_msg_id = Column(Numeric)
    d_chat_msg_id = Column(Numeric)
    from_msg_id = Column(Numeric)
    to_msg_id = Column(Numeric)
    delayed_clone = Column(Boolean)
    caption = Column(Boolean)
    file_caption = Column(Boolean)
    last_msg_id = Column(Numeric)

    def __init__(self, id, s_chat, s_chat_msg_id, d_chat, d_chat_msg_id, from_id, from_msg_id, to_id, to_msg_id,
                 delayed_clone, caption, file_caption, last_msg_id):
        self.id = id
        self.s_chat = s_chat
        self.d_chat = d_chat
        self.s_chat_msg_id = s_chat_msg_id
        self.d_chat_msg_id = d_chat_msg_id
        self.from_id = from_id
        self.from_msg_id = from_msg_id
        self.to_id = to_id
        self.to_msg_id = to_msg_id
        self.delayed_clone = delayed_clone
        self.caption = caption
        self.file_caption = file_caption
        self.last_msg_id = last_msg_id


Clonebot.__table__.create(checkfirst=True)


async def add_user(id):
    with INSERTION_LOCK:
        msg = SESSION.query(Clonebot).get(id)
        if not msg:
            usr = Clonebot(id, 0, 0, 0, 0, 0, 0, 0, 0, False, True, False, 0)
            SESSION.add(usr)
            SESSION.commit()
        else:
            pass


async def source_force_reply(id, s_chat_msg_id):
    with INSERTION_LOCK:
        try:
            SESSION.query(Clonebot).filter(Clonebot.id == id).update({'s_chat_msg_id': s_chat_msg_id})
        finally:
            SESSION.commit()

async def source_cnf_db(id, value):
    with INSERTION_LOCK:
        try:
            SESSION.query(Clonebot).filter(Clonebot.id == id).update({'s_chat': value, 'last_msg_id': 0})
        finally:
            SESSION.commit()


async def target_force_reply(id, d_chat_msg_id):
    with INSERTION_LOCK:
        try:
            SESSION.query(Clonebot).filter(Clonebot.id == id).update({'d_chat_msg_id': d_chat_msg_id})
        finally:
            SESSION.commit()


async def target_cnf_db(id, value):
    with INSERTION_LOCK:
        try:
            SESSION.query(Clonebot).filter(Clonebot.id == id).update({'d_chat': value})
        finally:
            SESSION.commit()


async def from_msg_id_force_reply(id, from_msg_id):
    with INSERTION_LOCK:
        try:
            SESSION.query(Clonebot).filter(Clonebot.id == id).update({'from_msg_id': from_msg_id})
        finally:
            SESSION.commit()


async def from_msg_id_cnf_db(id, value):
    with INSERTION_LOCK:
        try:
            SESSION.query(Clonebot).filter(Clonebot.id == id).update({'from_id': value})
        finally:
            SESSION.commit()


async def to_msg_id_force_reply(id, to_id):
    with INSERTION_LOCK:
        try:
            SESSION.query(Clonebot).filter(Clonebot.id == id).update({'to_msg_id': to_id})
        finally:
            SESSION.commit()


async def to_msg_id_cnf_db(id, value):
    with INSERTION_LOCK:
        try:
            SESSION.query(Clonebot).filter(Clonebot.id == id).update({'to_id': value})
        finally:
            SESSION.commit()


async def query_msg(id):
    try:
        query = SESSION.query(Clonebot).filter(Clonebot.id == id).first()
        return query
    finally:
        SESSION.close()


async def del_from_to_ids(id):
    with INSERTION_LOCK:
        try:
            SESSION.query(Clonebot).filter(Clonebot.id == id).update({'from_id': 0, 'to_id': 0, 'last_msg_id': 0})
        finally:
            SESSION.commit()


async def change_delay(id):
    with INSERTION_LOCK:
        try:
            msg = SESSION.query(Clonebot).filter(Clonebot.id == id).first()
            status = bool(msg.delayed_clone)
            if status is True:
                SESSION.query(Clonebot).filter(Clonebot.id == id).update({'delayed_clone': False})
            else:
                SESSION.query(Clonebot).filter(Clonebot.id == id).update({'delayed_clone': True})
        finally:
            SESSION.commit()


async def opt_caption(id):
    with INSERTION_LOCK:
        try:
            msg = SESSION.query(Clonebot).filter(Clonebot.id == id).first()
            status = bool(msg.caption)
            if status is True:
                SESSION.query(Clonebot).filter(Clonebot.id == id).update({'caption': False})
            else:
                SESSION.query(Clonebot).filter(Clonebot.id == id).update({'caption': True, 'file_caption': False})
        finally:
            SESSION.commit()


async def opt_FN_caption(id):
    with INSERTION_LOCK:
        try:
            msg = SESSION.query(Clonebot).filter(Clonebot.id == id).first()
            status = bool(msg.file_caption)
            if status is True:
                SESSION.query(Clonebot).filter(Clonebot.id == id).update({'file_caption': False})
            else:
                SESSION.query(Clonebot).filter(Clonebot.id == id).update({'file_caption': True, 'caption': False})
        finally:
            SESSION.commit()


async def msg_id_limit(id, value):
    with INSERTION_LOCK:
        try:
            SESSION.query(Clonebot).filter(Clonebot.id == id).update({'last_msg_id': value})
        finally:
            SESSION.commit()


async def reset_all(id):
    with INSERTION_LOCK:
        try:
            SESSION.query(Clonebot).filter(Clonebot.id == id).update(
                {
                    's_chat': 0, 's_chat_msg_id': 0, 'd_chat': 0, 'd_chat_msg_id': 0, 'from_id': 0,
                    'from_msg_id': 0, 'to_id': 0, 'to_msg_id': 0, 'delayed_clone': False, 'caption': True,
                    'file_caption': False, "last_msg_id": 0
                }
            )
        finally:
            SESSION.commit()
