from listrr.sql import (
    CREATE_ROOT_NODE,
    GET_ROOT_NODE,
    ADD_LIST_ITEM,
)
from listrr.listid import gen_list_uuid

def create_root_node(db, uuid_size):
    with db.cursor as cursor:
        cursor.execute(CREATE_ROOT_NODE, (uuid_size,))
        return cursor.fetchone()[0]

def get_root_node(db):
    with db.cursor as cursor:
        cursor.execute(GET_ROOT_NODE)
        return cursor.fetchone()

def add_list_item(db, uuid_size, parent_id, title):
    uuid = gen_list_uuid(uuid_size)
    with db.cursor as cursor:
        cursor.execute(ADD_LIST_ITEM, (parent_id, uuid, title))
    return uuid
