from announcements.models import Announcement
from django.views.generic import ListView


class AnnouncementListView(ListView):
    model = Announcement
    context_object_name = 'announcements'
