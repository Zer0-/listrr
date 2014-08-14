from initdb import setup
import logging

def drop_list_table(db):
    with db.cursor as cursor:
        logging.warn("Deleting table list_item!")
        cursor.execute("DROP TABLE list_item")
        logging.warn("Table list_item dropped.")

if __name__ == "__main__":
    settings, db = setup()
    drop_list_table(db)
