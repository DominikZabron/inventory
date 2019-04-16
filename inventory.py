import json

from dispatcher import Event
from handlers import create_product, update_product, stock_summary


class ProductEvents:
    created = 'ProductCreated'
    updated = 'ProductUpdated'
    summary = 'StockSummary'


def parse_file():
    with open('input.txt') as f:
        lines_amount = int(f.readline())

        for _ in range(lines_amount):
            event = json.loads(f.readline())
            Event.trigger(event)

        Event.trigger({'type': ProductEvents.summary})


if __name__ == "__main__":
    Event.on(ProductEvents.created, create_product)
    Event.on(ProductEvents.created, update_product)
    Event.on(ProductEvents.updated, update_product)
    Event.on(ProductEvents.summary, stock_summary)
    parse_file()
