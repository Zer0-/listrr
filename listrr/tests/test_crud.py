import unittest
from bricks import Settings
from common_components.db import PostgresThreadPool, DatabaseComponent

from listrr.crud_api import (
    get_root_node,
    create_root_node,
    add_list_item,
    get_list_tree,
    update_list_item_title,
)

def clear_list_table(db):
    with db.cursor as cursor:
        cursor.execute("DELETE FROM list_item")

class TestCrud(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        from listrr.scripts.initdb import create_table
        settings = Settings()
        self.db = DatabaseComponent(PostgresThreadPool(settings))
        create_table(self.db, settings)
        self.settings = settings
        self.uuid_size = settings['list_uuid_size']

    def tearDown(self):
        clear_list_table(self.db)

    def testRootNodeNonexist(self):
        self.assertEqual(get_root_node(self.db), None)

    def testRootNodeCreation(self):
        node_id = create_root_node(self.db, self.uuid_size)
        fetched_node_id = get_root_node(self.db)[0]
        self.assertEqual(node_id, fetched_node_id)

    def testAddToplevelList(self):
        rootnode = create_root_node(self.db, self.uuid_size)
        uuids = set()
        for i in range(4):
            uuids.add(add_list_item(
                self.db,
                self.uuid_size,
                rootnode,
                str(i) * 10
            ))
        self.assertEqual(len(uuids), 4)

        with self.db.cursor as cursor:
            cursor.execute("SELECT parent_id, title, id FROM list_item"
                           " WHERE parent_id IS NOT NULL")
            results = cursor.fetchall()
        for pid, title, uuid in results:
            self.assertEqual(pid, rootnode)
            self.assertTrue(title.isdigit())
            self.assertTrue(uuid in uuids)

    def testAddNestedList(self):
        rootnode = create_root_node(self.db, self.uuid_size)
        list_id = add_list_item(
            self.db,
            self.uuid_size,
            rootnode,
            'root'
        )
        maxdepth = 4
        add_count = 0
        def deep_add(parent_id, n):
            nonlocal add_count
            if n < 1:
                return
            for i in range(3):
                list_item_id = add_list_item(
                    self.db,
                    self.uuid_size,
                    parent_id,
                    str(n)*4 + str(i)
                )
                add_count += 1
                deep_add(list_item_id, n-1)
        deep_add(list_id, maxdepth)
        tree = get_list_tree(self.db, list_id)[0]
        self.assertEqual(tree.title, "root")
        self.assertEqual(tree.id, list_id)
        get_count = 0
        def chk_tree(tree, depth):
            nonlocal get_count
            for li in tree:
                self.assertTrue(li.title.startswith(str(maxdepth - depth)*4))
                get_count += 1
                chk_tree(li.replies, depth + 1)
        chk_tree(tree.replies, 0)

    def testUpdateTitle(self):
        rootnode = create_root_node(self.db, self.uuid_size)
        list_id = add_list_item(
            self.db,
            self.uuid_size,
            rootnode,
            'root'
        )
        update_list_item_title(self.db, list_id, "testupdate")
        list_item = get_list_tree(self.db, list_id)[0]
        self.assertEqual(list_item.title, "testupdate")

    @classmethod
    def tearDownClass(self):
        from listrr.scripts.deltable import drop_list_table
        drop_list_table(self.db)

if __name__ == "__main__":
    unittest.main()
