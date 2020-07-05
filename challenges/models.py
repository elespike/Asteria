from django.core.validators import (
    MaxValueValidator
)
from django.db import (
    models
)
from uuid import (
    uuid4
)


HTML_FIELD_HELP_TEXT = 'This field is HTML-formatted'


class Category(models.Model):
    title = models.CharField(unique=True, max_length=64)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    description.help_text = HTML_FIELD_HELP_TEXT

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['title']


class Level(models.Model):
    number = models.PositiveSmallIntegerField(primary_key=True)
    description = models.TextField(blank=True)
    points_required = models.PositiveIntegerField(default=0)
    percentage_required = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(100)]
    )
    challenges_required = models.ManyToManyField(
        'Challenge',
        blank=True,
        related_name='requiring_levels'
    )

    description.help_text = HTML_FIELD_HELP_TEXT
    points_required.help_text = (
        'The amount of points a team must possess'
        ' in order to unlock this level'
    )
    percentage_required.help_text = (
        'The percentage of challenges in the previous level'
        ' which a team must solve in order to unlock this level'
    )
    challenges_required.help_text = (
        'Individual challenges from previous levels'
        ' which a team must solve in order to unlock this level'
    )

    def __str__(self):
        return 'Level {}'.format(self.number)

    class Meta:
        ordering = ['number']


class Challenge(models.Model):

    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    bonus_limit = models.PositiveSmallIntegerField(default=0)
    bonus_points = models.PositiveSmallIntegerField(default=0)
    depreciation  = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(blank=True)
    penalty = models.PositiveSmallIntegerField(default=0)
    points = models.PositiveSmallIntegerField(default=0)
    slug = models.SlugField(unique=True)
    times_solved = models.PositiveSmallIntegerField(default=0, editable=False)
    title = models.CharField(unique=True, max_length=64)

    bonus_points.help_text = (
        'Award these many points to team on correct submission'
    )
    bonus_limit.help_text = (
        'Stop awarding bonus points after these many correct submissions'
    )
    depreciation.help_text = (
        'Subtract these many points from challenge on each correct submission'
    )
    penalty.help_text = (
        'Subtract these many points from team on each incorrect submission'
    )
    description.help_text = HTML_FIELD_HELP_TEXT

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['level__number', 'points', 'category__slug', 'slug']


class Flag(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    value = models.CharField(unique=True, max_length=128, default=uuid4)

    def __str__(self):
        return self.value


class Hint(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    hint_text = models.TextField()

    penalty = models.PositiveSmallIntegerField(default=0)
    penalty.help_text = (
        'Subtract these many points from team on hint revelation'
    )

    def __str__(self):
        return self.hint_text


class Link(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    url = models.URLField(unique=True)
    description = models.CharField(max_length=64)

    url.help_text = 'FQDN or IP address'

    def __str__(self):
        return self.description


class File(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    uploaded_file = models.FileField(unique=True, upload_to='uploads/')
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.description
