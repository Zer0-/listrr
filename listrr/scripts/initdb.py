from bricks import Settings
from common_components.db import PostgresThreadPool, DatabaseComponent
from listrr.logger import setup_logger
from listrr.sql import CREATE_LIST_ITEM_TABLE
from listrr.listid import gen_list_uuid
import logging

def setup():
    settings = Settings("../")
    setup_logger(settings['logfile_path'])
    db = DatabaseComponent(PostgresThreadPool(settings))
    return settings, db

def create_table(db, settings):
    id_size = settings['list_uuid_size']
    id_size = len(gen_list_uuid(id_size))
    with db.cursor as cursor:
        logging.info("Creating list items table if not exists...")
        cursor.execute(CREATE_LIST_ITEM_TABLE, (id_size, id_size))
        logging.info("OK")

if __name__ == "__main__":
    settings, db = setup()
    create_table(db, settings)
