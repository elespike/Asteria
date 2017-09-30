from django.contrib import admin
from django         import forms
from announcements.models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'post_time']

