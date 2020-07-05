from announcements.templatetags.announcements_helper_tags import is_ctf_open
from challenges.models import Level

from django.contrib.auth.models import AnonymousUser
from django.template import Library


register = Library()


@register.simple_tag
def divide(dividend, divisor, percentage=False):
    if divisor == 0:
        return divisor

    quotient = dividend / divisor
    if percentage:
        quotient *= 100
    return int(quotient)


@register.simple_tag
def get_previous_level(current_level):
    previous_level = Level.objects.filter(
        number__lt=current_level.number
    ).last()
    return previous_level


@register.simple_tag
def get_cols(num_elements):
    cols = 12 // num_elements
    if cols < 2:
        return 2
    else:
        return cols


@register.simple_tag
def any_bonus(challenge_list):
    for challenge in challenge_list:
        if challenge.bonus_points > 0 and challenge.bonus_limit > 0:
            return True
    return False


@register.simple_tag
def any_depreciation(challenge_list):
    for challenge in challenge_list:
        if challenge.depreciation > 0:
            return True
    return False


@register.simple_tag
def any_penalty(challenge_list):
    for challenge in challenge_list:
        if challenge.penalty > 0:
            return True
    return False


@register.simple_tag
def is_solved(challenge, team):
    if team is None:
        return False
    elif team and any(
        flag in challenge.flag_set.all()
        for flag in team.flags.all()
    ):
        return True
    return False


@register.simple_tag
def percentage_completed(level_or_category, team):
    if team is None or not level_or_category:
        return 0

    completed_challenges = 0
    challenges = level_or_category.challenge_set.all()
    for challenge in challenges:
        if is_solved(challenge, team):
            completed_challenges += 1

    return divide(completed_challenges, len(challenges), percentage=True)


@register.simple_tag
def is_locked(challenge_or_level, user):
    if user.is_staff or user.is_superuser:
        return False

    if isinstance(user, AnonymousUser) or not is_ctf_open():
        return True

    team = user.team
    if team is None:
        return True

    level = challenge_or_level
    if hasattr(challenge_or_level, 'level'):
        level = challenge_or_level.level

    if team and level.points_required > team.points:
        return True

    if level.percentage_required:
        previous_level = Level.objects.filter(number__lt=level.number).last()
        pcent_complete = percentage_completed(previous_level, team)
        if (previous_level is not None
        and pcent_complete < level.percentage_required):
            return True

    for c in level.challenges_required.all():
        if not is_solved(c, team):
            return True

    return False
