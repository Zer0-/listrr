from collections import namedtuple
from listrr.sql import (
    GET_ROOT_NODE,
    ADD_LIST_ITEM,
    GET_LIST_TREE,
)
from listrr.listid import gen_list_uuid

ListItem = namedtuple('ListItem', 'id, title, time_created, replies')

def create_root_node(db, uuid_size):
    return add_list_item(db, uuid_size, None, 'www')

def get_root_node(db):
    with db.cursor as cursor:
        cursor.execute(GET_ROOT_NODE)
        return cursor.fetchone()

def add_list_item(db, uuid_size, parent_id, title):
    #WARNING: there is a nonzero chance a non-unique uuid will be generated
    #However the database will not allow us to insert in this case.
    #The chances are so low that this happening means it's very likely that
    #either uuid_size is way too small or the RNG is not working properly
    uuid = gen_list_uuid(uuid_size)
    with db.cursor as cursor:
        cursor.execute(ADD_LIST_ITEM, (uuid, parent_id, title))
    return uuid

def _build_list_tree(db_results):
    depth = db_results[0][3]
    root = []
    path = []
    head = root
    for data in db_results:
        rdepth = data[3]
        if rdepth > depth:
            depth = rdepth
            path.append(head)
            head = last_elem
        elif rdepth < depth:
            for i in range(depth - rdepth):
                head = path.pop()
            depth = rdepth
        post = ListItem._make(data[:-1] + ([],))
        head.append(post)
        last_elem = post.replies
    return root

def get_list_tree(db, parent_id):
    with db.cursor as cursor:
        cursor.execute(GET_LIST_TREE, (parent_id,))
        query_result = cursor.fetchall()
    return _build_list_tree(query_result)
