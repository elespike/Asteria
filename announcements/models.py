from django.db import models
from django.utils import timezone


class Announcement(models.Model):
    title     = models.CharField(max_length=64)
    markup    = models.TextField()
    post_time = models.DateTimeField(default=timezone.now)

    post_time.help_text = "This announcement will only appear after the selected date/time"

    def __str__(self):
        return self.title


    class Meta:
        ordering = ['-post_time']

