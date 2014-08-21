import unittest
from bricks import Settings
from common_components.db import PostgresThreadPool, DatabaseComponent

from listrr.crud_api import ListApi, ItemNotFound

def clear_list_table(db):
    with db.cursor as cursor:
        cursor.execute("DELETE FROM list_item")

def deep_add(listapi, parent_id, depth, n=3):
    add_count = 0
    if depth < 1:
        return add_count
    for i in range(n):
        list_item_id = listapi.add_list_item(
            parent_id,
            str(depth)*4 + str(i)
        )
        add_count += 1
        add_count += deep_add(listapi, list_item_id, depth-1, n)
    return add_count

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
        root_node = self.listapi.get_root_node()
        self.assertTrue(root_node)

    def testAddToplevelList(self):
        rootnode = self.listapi.get_root_node()
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
        rootnode = self.listapi.get_root_node()
        list_id = self.listapi.add_list_item(
            rootnode,
            'root'
        )
        maxdepth = 4
        add_count = deep_add(self.listapi, list_id, maxdepth)
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
        rootnode = self.listapi.get_root_node()
        list_id = self.listapi.add_list_item(
            rootnode,
            'root'
        )
        self.listapi.update_list_item_title(list_id, "testupdate")
        list_item = self.listapi.get_list_tree(list_id)[0]
        self.assertEqual(list_item.title, "testupdate")

    def tesetFailUpdate(self):
        with self.assertRaises(ItemNotFound):
            self.listapi.update_list_item_title(list_id, "newtitle")

    def testDel(self):
        rootnode = self.listapi.get_root_node()
        list_id = self.listapi.add_list_item(
            rootnode,
            "A test item is a test item"
        )
        self.listapi.remove_list_item(list_id)
        self.assertFalse(self.listapi.get_list_tree(rootnode)[0].replies)

    def testNoDel(self):
        rootnode = self.listapi.get_root_node()
        with self.assertRaises(ItemNotFound):
            self.listapi.remove_list_item('a' * len(rootnode))

    def testGetSingleItem(self):
        rootnode = self.listapi.get_root_node()
        text = "A test item is a test item"
        list_id = self.listapi.add_list_item(
            rootnode,
            text
        )
        item = self.listapi.get_list_item(list_id)
        self.assertEqual(item.title, text)
        self.assertEqual(item.id, list_id)
        self.assertEqual(item.parent_id, rootnode)
        self.assertTrue(item.time_created is not None)
        self.assertTrue(item.last_modified is not None)
        self.assertFalse(item.done)

    def testSimpleMarkDone(self):
        rootnode = self.listapi.get_root_node()
        text = "A test item is a test item"
        list_id = self.listapi.add_list_item(
            rootnode,
            text
        )
        result = self.listapi.mark_done(list_id)
        self.assertEqual(result, [list_id])
        item = self.listapi.get_list_item(list_id)
        self.assertTrue(item.done)

    def testDeepMark(self):
        rootnode = self.listapi.get_root_node()
        list_id = self.listapi.add_list_item(
            rootnode,
            'abbacaa'
        )
        deep_add(self.listapi, list_id, 3, 1)
        tree = self.listapi.get_list_tree(list_id)
        head = tree[0]
        a = head.replies[0]
        b = a.replies[0]
        c = b.replies[0]
        marked = self.listapi.mark_done(c.id)
        self.assertEqual(set(marked), set((list_id, head.id, a.id, b.id, c.id)))
        tree = self.listapi.get_list_tree(list_id)
        head = tree[0]
        a = head.replies[0]
        b = a.replies[0]
        c = b.replies[0]
        self.assertTrue(head.done)
        self.assertTrue(a.done)
        self.assertTrue(b.done)
        self.assertTrue(c.done)

    @classmethod
    def tearDownClass(self):
        from listrr.scripts.deltable import drop_list_table
        drop_list_table(self.db)

if __name__ == "__main__":
    unittest.main()
