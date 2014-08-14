from listrr.scripts.initdb import setup
import logging

def drop_list_table(db):
    with db.cursor as cursor:
        logging.warning("Deleting table list_item!")
        cursor.execute("DROP TABLE list_item")
        logging.warning("Table list_item dropped.")

if __name__ == "__main__":
    from listrr.logger import setup_logger
    settings, db = setup()
    setup_logger(settings['logfile_path'])
    drop_list_table(db)
