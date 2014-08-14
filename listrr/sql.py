#/* set ft=sql
CREATE_LIST_ITEM_TABLE = """
--*/
CREATE TABLE IF NOT EXISTS list_item(
    id serial PRIMARY KEY,
    parent_id integer REFERENCES list_item(id) ON DELETE CASCADE,
    time_created timestamp with time zone DEFAULT current_timestamp NOT NULL,
    last_modified timestamp with time zone DEFAULT current_timestamp NOT NULL,
    title text NOT NULL,
    uuid char(%s) UNIQUE NOT NULL
);
"""

CREATE_ROOT_NODE = """
INSERT INTO list_item (title, uuid) VALUES (%s, 0)
RETURNING id
"""

GET_ROOT_NODE = """
SELECT id FROM list_item WHERE parent_id IS NULL
"""

ADD_LIST_ITEM = """
INSERT INTO list_item (
    parent_id,
    uuid,
    title
) VALUES (%s, %s, %s)
RETURNING id
"""

UPDATE_LIST_TIMESTAMPS = """
WITH RECURSIVE t(id) AS (                                                          
    SELECT %s
    UNION ALL                                                                      
    SELECT post.parent_id FROM post, t                                             
        WHERE post.id=t.id AND post.parent_id IS NOT NULL                          
)                                                                                  
UPDATE post SET last_reply=DEFAULT WHERE id IN (SELECT id FROM t);
"""

GET_POST_TREE = """
WITH RECURSIVE t(
    id,
    time_created,
    message,
    image_filename,
    image_identifier,
    path,
    depth
) AS (
    SELECT
        id,
        time_created,
        message,
        image_filename,
        image_identifier,
        array[-extract(epoch from last_reply)] AS path,
        0 AS depth
    FROM post
    WHERE id=%s

    UNION ALL

    SELECT
        post.id,
        post.time_created,
        post.message,
        post.image_filename,
        post.image_identifier,
        t.path || -extract(epoch from post.last_reply),
        t.depth + 1
    FROM post, t
    WHERE post.parent_id=t.id
)
SELECT
    id,
    time_created,
    message,
    depth,
    image_filename,
    image_identifier
FROM t ORDER BY path ASC;
"""
