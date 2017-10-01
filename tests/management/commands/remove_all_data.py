from django.core.management.base import BaseCommand
import announcements.models as announcement_models
import challenges.models    as challenge_models
import teams.models         as team_models

class Command(BaseCommand):
    help = 'Remove all data from the current database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep-superusers'   ,
            action='store_true'  ,
            dest='keep_superusers',
            default=False        ,
            help='Don\'t delete any superusers.'
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

        team_models.Team  .objects.all().delete()

        keep_superusers = kwargs.get('keep_superusers')
        if keep_superusers:
            team_models.Player.objects.all().exclude(is_superuser=True).delete()
        else:
            team_models.Player.objects.all().delete()

