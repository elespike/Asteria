import challenges.models as challenge_models

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create dummy test data in the current database.'

    def handle(self, *args, **kwargs):
        for i in range(1, 5):
            category = challenge_models.Category.objects.create(
                title=F"category {i}",
                slug=F"category-{i}",
                description=F"this is category {i}",
            )

            level = challenge_models.Level.objects.create(
                number=i,
                description=F"this is level {i}",
                points_required=(i - 1) * 10,
                percentage_required=50 if i > 1 else 0,
            )

            start = 1 + ((i - 1) * 4)
            end = start + 4
            for x in range(start, end):
                challenge = challenge_models.Challenge.objects.create(
                    category=category,
                    level=level,
                    points=(x * 10),
                    bonus_points=(x * 2),
                    bonus_limit=x,
                    depreciation=x,
                    penalty=x,
                    title=F"challenge {x}",
                    slug=F"challenge-{x}",
                    description=F"this is challenge {x}",
                )

                flag = challenge_models.Flag.objects.create(
                    challenge=challenge,
                    value=F"flag {x}",
                )
                challenge.flag_set.add(flag)

                for a in range(1, 5):
                    hint = challenge_models.Hint.objects.create(
                        hint_text=F"this is hint {a} for challenge {x}",
                        penalty=a,
                        challenge=challenge,
                    )
                    challenge.hint_set.add(hint)

                    link_url = F"http://127.0.{x}.{a}"
                    link = challenge_models.Link.objects.create(
                        url=link_url,
                        description=link_url,
                        challenge=challenge,
                    )
                    challenge.link_set.add(link)

                challenge.save()
