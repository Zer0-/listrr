import unittest
from bricks import Settings
from common_components.db import PostgresThreadPool, DatabaseComponent

from listrr.crud_api import ListApi

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

    def setUp(self):
        self.listapi = ListApi(self.db, self.settings)

    def tearDown(self):
        clear_list_table(self.db)

    def testRootNodeNonexist(self):
        self.assertEqual(self.listapi.get_root_node(), None)

    def testRootNodeCreation(self):
        node_id = self.listapi.create_root_node()
        fetched_node_id = self.listapi.get_root_node()[0]
        self.assertEqual(node_id, fetched_node_id)

    def testAddToplevelList(self):
        rootnode = self.listapi.create_root_node()
        uuids = set()
        for i in range(4):
            uuids.add(self.listapi.add_list_item(
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
        rootnode = self.listapi.create_root_node()
        list_id = self.listapi.add_list_item(
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
                list_item_id = self.listapi.add_list_item(
                    parent_id,
                    str(n)*4 + str(i)
                )
                add_count += 1
                deep_add(list_item_id, n-1)
        deep_add(list_id, maxdepth)
        tree = self.listapi.get_list_tree(list_id)[0]
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
        rootnode = self.listapi.create_root_node()
        list_id = self.listapi.add_list_item(
            rootnode,
            'root'
        )
        self.listapi.update_list_item_title(list_id, "testupdate")
        list_item = self.listapi.get_list_tree(list_id)[0]
        self.assertEqual(list_item.title, "testupdate")

    @classmethod
    def tearDownClass(self):
        from listrr.scripts.deltable import drop_list_table
        drop_list_table(self.db)

if __name__ == "__main__":
    unittest.main()
