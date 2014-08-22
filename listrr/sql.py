#/* set ft=sql
CREATE_LIST_ITEM_TABLE = """
--*/
CREATE TABLE IF NOT EXISTS list_item(
    id char(%s) PRIMARY KEY,
    parent_id char(%s) REFERENCES list_item(id) ON DELETE CASCADE,
    time_created timestamp with time zone DEFAULT current_timestamp NOT NULL,
    last_modified timestamp with time zone DEFAULT current_timestamp NOT NULL,
    title text NOT NULL,
    done boolean NOT NULL DEFAULT false
);
"""

GET_ROOT_NODE = """
SELECT id FROM list_item WHERE parent_id IS NULL
"""

GET_LIST_ITEM = """
SELECT * FROM list_item WHERE id = %s
"""

ADD_LIST_ITEM = """
INSERT INTO list_item (
    id,
    parent_id,
    title
) VALUES (%s, %s, %s)
"""

DELETE_LIST_ITEM = """
DELETE FROM list_item WHERE id=%s RETURNING parent_id
"""

UPDATE_LIST_TIMESTAMPS = """
WITH RECURSIVE t(id) AS (                                                          
    SELECT %s
    UNION ALL                                                                      
    SELECT list_item.parent_id FROM list_item, t                                             
        WHERE list_item.id=t.id AND list_item.parent_id IS NOT NULL                          
)                                                                                  
UPDATE list_item SET last_modified=DEFAULT WHERE id IN (SELECT id FROM t);
"""

UPDATE_ITEM_TITLE = """
UPDATE list_item SET title = %s WHERE id = %s RETURNING id
"""

UPDATE_ITEM_DONE_STATE = """
UPDATE list_item SET done = %s WHERE id = %s RETURNING id
"""

GET_LIST_TREE = """
WITH RECURSIVE t(
    id,
    title,
    time_created,
    done,
    path,
    depth
) AS (
    SELECT
        id,
        title,
        time_created,
        done,
        array[extract(epoch from last_modified)] AS path,
        0 AS depth
    FROM list_item
    WHERE id=%s

    UNION ALL

    SELECT
        list_item.id,
        list_item.title,
        list_item.time_created,
        list_item.done,
        t.path || extract(epoch from list_item.last_modified),
        t.depth + 1
    FROM list_item, t
    WHERE list_item.parent_id=t.id
)
SELECT
    id,
    title,
    time_created,
    done,
    depth
FROM t ORDER BY path;
"""
