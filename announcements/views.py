from announcements.models    import Announcement
from common.helper_functions import Events
from django.conf             import settings
from django.views.generic    import ListView


class AnnouncementListView(ListView):
    model = Announcement
    context_object_name = 'announcements'

