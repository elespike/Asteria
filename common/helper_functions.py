from collections    import namedtuple
from django.conf    import settings
from django.contrib import messages


class Events:
    Event = namedtuple('Event', 'type, dt, pretty')

    CTF_START = Event('ctf', settings.CTF_START, 'CTF starts in...')
    CTF_END   = Event('ctf', settings.CTF_END  , 'CTF ends in...'  )

    REGISTRATION_START = Event('registration', settings.REGISTRATION_START, 'Registration opens in' )
    REGISTRATION_END   = Event('registration', settings.REGISTRATION_END  , 'Registration closes in')


def issue_errors(request, form):
    for error in form.non_field_errors():
        messages.error(request, error)
    for field in form.visible_fields():
        if field.errors:
            messages.error(request, field.errors, extra_tags='field_errors {}'.format(field.name))

