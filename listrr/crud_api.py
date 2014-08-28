from collections import namedtuple
from listrr.sql import (
    GET_ROOT_NODE,
    ADD_LIST_ITEM,
    GET_LIST_TREE,
    UPDATE_ITEM_TITLE,
    DELETE_LIST_ITEM,
    GET_LIST_ITEM,
    UPDATE_ITEM_DONE_STATE,
)
from listrr.listid import gen_list_uuid
import logging

ListItem = namedtuple('ListItem', 'id, title, time_created, done, replies')
FullListItem = namedtuple('FullListItem', 'id, parent_id, time_created, last_modified, title, done')

class ItemNotFound(Exception):
    pass

def _build_list_tree(db_results):
    depth = db_results[0][4]
    root = []
    path = []
    head = root
    for data in db_results:
        rdepth = data[4]
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

def _traverse_tree(tree, fn):
    for child in tree:
        fn(child)
        _traverse_tree(child.replies, fn)

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
        items_affected = []
        if parent_id is not None:
            items_affected += self.mark_undone(parent_id)
        return uuid, items_affected

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
            if result is None:
                raise ItemNotFound("Item with id {} does not exist."
                                   " Cannot remove.".format(item_id))
        deleted = [item_id]
        try:
            return deleted + self.mark_done(result[0])
        except ValueError:
            return deleted

    def update_list_item_title(self, item_id, newtitle):
        with self.db.cursor as cursor:
            cursor.execute(UPDATE_ITEM_TITLE, (newtitle, item_id))
            result = cursor.fetchone()
            if result is None:
                raise ItemNotFound("Item with id {} does not exist."
                                   " Cannot update title.".format(item_id))

    def get_list_item(self, item_id):
        with self.db.cursor as cursor:
            cursor.execute(GET_LIST_ITEM, (item_id,))
            result = cursor.fetchone()
            if result is None:
                raise ItemNotFound("Item with id {} does not exist."
                                   " Cannot fetch item.".format(item_id))
        return FullListItem._make(result)

    def _mark(self, item_id, new_status):
        """
        Marks an item as done if it's children are marked done.
        Also marks it's parent complete if all of the parent's
        children are now complete.
        """
        item = self.get_list_item(item_id)
        parent_id = item.parent_id
        if parent_id is None:
            return []
        if item.done == new_status:
            return [item_id]
        tree = self.get_list_tree(parent_id)
        parent_item = tree[0]
        for child in parent_item.replies:
            if child.id == item_id:
                our_item = child
                break
        #here we want to see if every child of our item,
        #being the list item with id item_id, is marked done.
        #this makes it safe to mark the item done as well.
        all_done = True
        def also_done(list_item):
            nonlocal all_done
            all_done = all_done and list_item.done
        _traverse_tree(our_item.replies, also_done)
        marked = [item_id]
        if not our_item.replies or all_done == new_status:
            with self.db.cursor as cursor:
                cursor.execute(UPDATE_ITEM_DONE_STATE, (new_status, item_id))
            try:
                marked += self._mark(parent_id, new_status)
            except ValueError:
                pass
        else:
            raise ValueError()
        return marked

    def mark_done(self, item_id):
        return self._mark(item_id, True)

    def mark_undone(self, item_id):
        return self._mark(item_id, False)

