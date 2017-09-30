from challenges.models          import Hint, Flag
from django.contrib.auth.models import AbstractUser
from django.core.validators     import MaxValueValidator
from django.db                  import models
from uuid                       import uuid4


class Team(models.Model):
    name   = models.CharField           (unique=True, max_length=64)
    points = models.PositiveIntegerField(default=0)
    notes  = models.TextField           (blank=True)

    points.help_text = "There's no need to manually change a team's points. This option is solely available for circumstantial penalties or bonuses."

    slug     = models.SlugField      (unique=True   , editable=False, default=uuid4)
    password = models.CharField      (max_length=128, editable=False)
    hints    = models.ManyToManyField(Hint          , editable=False)
    flags    = models.ManyToManyField(Flag          , editable=False)

    def __str__(self):
        return self.name


    class Meta:
        ordering = ['-points', 'slug']


class Player(AbstractUser):
    team = models.ForeignKey(Team, blank=True, null=True)

    PLAYER    = 0
    MODERATOR = 1
    CAPTAIN   = 2
    STANDING_CHOICES = [
        (PLAYER   , 'Player'   ),
        (MODERATOR, 'Moderator'),
        (CAPTAIN  , 'Captain'  ),
    ]
    standing = models.PositiveIntegerField(choices=STANDING_CHOICES, default=PLAYER, validators=[MaxValueValidator(3)])

    slug = models.SlugField(unique=True, editable=False, default=uuid4)


    class Meta:
        verbose_name = 'player'
        ordering = ['-standing', 'slug']

