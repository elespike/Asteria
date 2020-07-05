from collections import (
    namedtuple
)
from datetime import (
    timedelta
)
from django.conf import (
    settings
)
from django.template import (
    Library
)
from django.utils import (
    timezone as tz
)
from math import (
    trunc
)


Event = namedtuple('Event', 'dt, text')

CTF_EVENTS = (
    Event(
        settings.CTF_START,
        'CTF starts in...'
    ),
    Event(
        settings.CTF_END,
        'CTF ends in...'
    )
)

REGISTRATION_EVENTS = (
    Event(
        settings.REGISTRATION_START,
        'Registration opens in'
    ),
    Event(
        settings.REGISTRATION_END,
        'Registration closes in'
    )
)

TYPE_TO_EVENTS = {
    'ctf': CTF_EVENTS,
    'registration': REGISTRATION_EVENTS
}


register = Library()


@register.simple_tag
def get_title():
    return settings.TITLE


def get_time_til(event):
    if event is not None:
        time_til_event = event.dt - tz.localtime()
        # Days will be negative if an event has passed
        if time_til_event.days >= 0:
            return time_til_event
    return timedelta()


@register.simple_tag
def get_days_til(event):
    return trunc(get_time_til(event).days)


@register.simple_tag
def get_hours_til(event):
    return trunc((get_time_til(event).total_seconds() / 3600) % 24)


@register.simple_tag
def get_minutes_til(event):
    return trunc((get_time_til(event).total_seconds() / 60) % 60)


@register.simple_tag
def get_seconds_til(event):
    return trunc(get_time_til(event).total_seconds() % 60)


@register.simple_tag
def get_total_seconds_til(event):
    return trunc(get_time_til(event).total_seconds())


def get_next_event(event_type):
    for event in filter(
        lambda e: get_total_seconds_til(e),
        TYPE_TO_EVENTS.get(event_type, [])
    ):
        return event
    return None


@register.simple_tag
def get_next_ctf_event():
    return get_next_event('ctf')


@register.simple_tag
def get_next_registration_event():
    return get_next_event('registration')


def is_event_open(event_type):
    events = TYPE_TO_EVENTS.get(event_type, [])
    if not events:
        return False
    elif events[0].dt > events[1].dt:
        return False
    elif ( get_total_seconds_til(events[0])
    or not get_total_seconds_til(events[1]) ):
        return False
    return True


@register.simple_tag
def is_ctf_open():
    return is_event_open('ctf')


@register.simple_tag
def is_registration_open():
    return is_event_open('registration')


@register.simple_tag
def should_post_announcement(post_time):
    if post_time < tz.localtime():
        return True
    return False
