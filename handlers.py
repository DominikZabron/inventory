import json

from db import db


def create_product(event, *args, **kwargs):
    db.execute("""
        INSERT INTO Products (id, parent_id) 
        VALUES (:id, :parent_id);
    """, event)
    if not event['parent_id']:
        db.execute("""
            INSERT INTO Stocks (product_id, stock)
            VALUES (:id, :stock);
        """, event)


def update_product(event, *args, **kwargs):
    def _update(product_id):
        db.execute("""
            UPDATE Stocks SET stock = ? WHERE product_id = ?;
        """, (stock, product_id))

    def _get_parent_id():
        db.execute("""
            SELECT parent_id FROM Products WHERE id = :id;
        """, event)
        return db.fetchone()['parent_id'] or event['id']

    def _get_stock():
        db.execute("""
            SELECT stock FROM Stocks WHERE product_id = ?;
        """, (parent_id,))
        return db.fetchone()['stock']

    def _notify():
        def _send(pid):
            output = {'type': 'UpdateProduct', 'id': pid, 'stock': stock}
            json.dump(output, file)
            file.write('\n')

        db.execute("""
            SELECT id FROM Products WHERE parent_id = ?
            UNION ALL
            SELECT id FROM Products WHERE id = ?;
        """, (parent_id, parent_id))
        with open('output.txt', 'a') as file:
            [_send(p['id']) for p in db.fetchall() if p['id'] != event['id']]

    stock = event['stock']
    parent_id = _get_parent_id()
    current_stock = _get_stock()

    if current_stock != stock:
        _update(parent_id)
        _notify()


def stock_summary(*args, **kwargs):
    db.execute("""
        SELECT p.id, s.stock
        FROM Products p
        INNER JOIN Stocks s
            ON p.parent_id = s.product_id
        WHERE p.parent_id IS NOT NULL
        UNION ALL
        SELECT p.id, s.stock
        FROM Products p
        INNER JOIN Stocks s
            ON p.id = s.product_id
        WHERE p.parent_id IS NULL
    """)
    summary = {d['id']: d['stock'] for d in db.fetchall()}
    output = {'stocks': summary, 'type': 'StockSummary'}
    with open('output.txt', 'a') as f:
        json.dump(output, f)
        f.write('\n')
