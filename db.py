import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_db():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER,
            parent_id INTEGER,
            PRIMARY KEY (id),
            FOREIGN KEY (parent_id) REFERENCES Products (id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Stocks (
            product_id INTEGER UNIQUE,
            stock INTEGER,
            FOREIGN KEY (product_id) REFERENCES Products (id)
        )
    """)
    return cur


db = init_db()
