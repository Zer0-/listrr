from collections import namedtuple
from listrr.sql import (
    GET_ROOT_NODE,
    ADD_LIST_ITEM,
    GET_LIST_TREE,
    UPDATE_ITEM_TITLE,
    DELETE_LIST_ITEM,
)
from listrr.listid import gen_list_uuid
import logging

ListItem = namedtuple('ListItem', 'id, title, time_created, replies')

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

class ListApi:
    requires_configured = ['sql_database', 'json_settings']

    def __init__(self, db, settings):
        self.db = db
        self.uuid_size = settings['list_uuid_size']
        rootnode = self._get_raw_root_node()
        if rootnode is None:
            logging.info("Creating root list node www")
            rootnode = self.create_root_node()

    def create_root_node(self):
        return self.add_list_item(None, 'www')

    def _get_raw_root_node(self):
        with self.db.cursor as cursor:
            cursor.execute(GET_ROOT_NODE)
            return cursor.fetchone()

    def get_root_node(self):
        return self._get_raw_root_node()[0]

    def add_list_item(self, parent_id, title):
        #WARNING: there is a nonzero chance a non-unique uuid will be generated
        #However the database will not allow us to insert in this case.
        #The chances are so low that this happening means it's very likely that
        #either uuid_size is way too small or the RNG is not working properly
        uuid = gen_list_uuid(self.uuid_size)
        with self.db.cursor as cursor:
            cursor.execute(ADD_LIST_ITEM, (uuid, parent_id, title))
        return uuid

    def get_list_tree(self, parent_id):
        with self.db.cursor as cursor:
            cursor.execute(GET_LIST_TREE, (parent_id,))
            query_result = cursor.fetchall()
        if query_result:
            return _build_list_tree(query_result)

    def remove_list_item(self, item_id):
        with self.db.cursor as cursor:
            cursor.execute(DELETE_LIST_ITEM, (item_id,))
            result = cursor.fetchone()
        return result is not None

    def update_list_item_title(self, list_id, newtitle):
        with self.db.cursor as cursor:
            cursor.execute(UPDATE_ITEM_TITLE, (newtitle, list_id))
