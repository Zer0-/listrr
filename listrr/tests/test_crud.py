import unittest
from listrr.sql import CREATE_ROOT_NODE
from bricks import Settings
from common_components.db import PostgresThreadPool, DatabaseComponent

from listrr.crud_api import (
    get_root_node,
    create_root_node,
    add_list_item,
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

    def testRootNodeNonexist(self):
        self.assertEqual(get_root_node(self.db), None)

    def testRootNodeCreation(self):
        node_id = create_root_node(self.db, self.uuid_size)
        fetched_node_id = get_root_node(self.db)[0]
        self.assertEqual(node_id, fetched_node_id)

        #teardown
        clear_list_table(self.db)

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
            cursor.execute("SELECT parent_id, title, uuid FROM list_item"
                           " WHERE parent_id IS NOT NULL")
            results = cursor.fetchall()
        for pid, title, uuid in results:
            self.assertEqual(pid, rootnode)
            self.assertTrue(title.isdigit())
            self.assertTrue(uuid in uuids)
        #teardown
        clear_list_table(self.db)

    @classmethod
    def tearDownClass(self):
        from listrr.scripts.deltable import drop_list_table
        drop_list_table(self.db)

if __name__ == "__main__":
    unittest.main()
