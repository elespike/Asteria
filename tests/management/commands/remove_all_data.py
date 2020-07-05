import announcements.models as announcement_models
import challenges.models as challenge_models
import teams.models as team_models

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Remove all data from the current database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep-superusers',
            action='store_true',
            dest='keep_superusers',
            default=False,
            help="Don't delete any superusers."
        )
        parser.add_argument(
            '--keep-staff-users',
            action='store_true',
            dest='keep_staff_users',
            default=False,
            help="Don't delete any staff users."
        )

    def handle(self, *args, **kwargs):
        announcement_models.Announcement.objects.all().delete()

        challenge_models.Flag     .objects.all().delete()
        challenge_models.Hint     .objects.all().delete()
        challenge_models.Link     .objects.all().delete()
        challenge_models.File     .objects.all().delete()
        challenge_models.Challenge.objects.all().delete()
        challenge_models.Category .objects.all().delete()
        challenge_models.Level    .objects.all().delete()

        team_models.Team.objects.all().delete()

        players = team_models.Player.objects.all()
        if kwargs.get('keep_superusers', False):
            players = players.exclude(is_superuser=True)
        if kwargs.get('keep_staff_users', False):
            players = players.exclude(is_staff=True)
        players.delete()
