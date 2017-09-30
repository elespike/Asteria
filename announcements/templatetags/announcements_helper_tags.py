from common.helper_functions import Events
from datetime                import datetime as dt, timedelta
from django.conf             import settings
from django.template         import Library
from django.utils            import timezone as dtz
from math                    import trunc

register = Library()

@register.simple_tag
def get_title():
    return settings.TITLE

def get_time_til(event):
    if event is not None:
        time_til_event = event.dt - dtz.localtime()
        # Days will be negative if an event has passed
        if time_til_event.days >= 0:
            return time_til_event
    return timedelta()

@register.assignment_tag
def get_days_til(event):
    return trunc(get_time_til(event).total_seconds() / 86400)

@register.assignment_tag
def get_hours_til(event):
    return trunc((get_time_til(event).total_seconds() / 3600) % 24)

@register.assignment_tag
def get_minutes_til(event):
    return trunc((get_time_til(event).total_seconds() / 60) % 60)

@register.assignment_tag
def get_seconds_til(event):
    return trunc(get_time_til(event).total_seconds() % 60)

@register.assignment_tag
def get_total_seconds_til(event):
    return trunc(get_time_til(event).total_seconds())

@register.assignment_tag
def get_next_event(event_type):
    events_dict = {}
    for attr in [a for a in dir(Events) if not a.startswith('__')]:
        event = getattr(Events, attr)
        if event.type != event_type:
            continue
        seconds_til = get_total_seconds_til(event)
        if seconds_til > 0:
            events_dict[event] = seconds_til
    try:
        return sorted(events_dict.items(), key=lambda x: x[1])[0][0]
    except IndexError:
        return None

@register.assignment_tag
def is_ctf_open():
    if get_total_seconds_til(Events.CTF_START)\
    or not get_total_seconds_til(Events.CTF_END):
        return False
    return True

@register.assignment_tag
def is_registration_open():
    if get_total_seconds_til(Events.REGISTRATION_START)\
    or not get_total_seconds_til(Events.REGISTRATION_END):
        return False
    return True

@register.assignment_tag
def should_post_announcement(post_time):
    if post_time < dtz.localtime():
        return True
    return False

