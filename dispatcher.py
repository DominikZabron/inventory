from collections import defaultdict


class Event:
    __events = defaultdict(list)

    @staticmethod
    def on(event_type, func):
        Event.__events[event_type].append(func)

    @staticmethod
    def trigger(event, *args, **kwargs):
        for func in Event.__events[event['type']]:
            func(event, *args, **kwargs)
