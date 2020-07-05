from announcements.models import Announcement
from django.contrib import admin


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'post_time']
