from challenges.forms               import RevealHintForm, SubmitFlagForm
from challenges.models              import Level, Category, Challenge, Hint
from common.helper_functions        import issue_errors
from django.contrib                 import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins     import LoginRequiredMixin
from django.http                    import HttpResponseRedirect
from django.urls                    import reverse
from django.views.generic           import ListView, DetailView


BAD_FLAG  = 'Incorrect flag!'
GOOD_FLAG = 'Well done!'
NO_TEAM   = 'You must join a team in order to participate!'
PENALTY   = ' {} points removed from {}!'


class LevelListView(ListView):
    model = Level
    context_object_name = 'levels'


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'


class ChallengeListView(ListView):
    model = Challenge
    context_object_name = 'challenges'


class LevelDetailView(DetailView):
    model = Level
    context_object_name = 'level'


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'


class ChallengeDetailView(LoginRequiredMixin, DetailView):
    model = Challenge
    context_object_name = 'challenge'


@login_required()
def reveal_hint(request):
    form = RevealHintForm(request.POST or None, player=request.user)

    hint = Hint.objects.filter(pk=form.data.get('hint_id')).first()
    if form.is_valid():
        # Validating team here (rather than in forms.py) because we're redirecting,
        # rather than just displaying form errors on the same challenge page.
        team = request.user.team
        if not team:
            messages.error(request, NO_TEAM)
            return HttpResponseRedirect(reverse('player', args=[request.user.slug]))

        team.hints.add(hint)
        if team.points and hint.penalty:
            team.points -= hint.penalty

        team.save()

    else:
        issue_errors(request, form)

    if hint is not None:
        return HttpResponseRedirect(reverse('challenge', args=[hint.challenge.slug]))
    return HttpResponseRedirect(reverse('challenges'))


@login_required()
def submit_flag(request):
    form = SubmitFlagForm(request.POST or None, player=request.user)

    challenge = Challenge.objects.filter(pk=form.data.get('challenge_id')).first()
    if form.is_valid():
        attempted_flag = form.cleaned_data['attempted_flag']

        # Validating team here (rather than in forms.py) because we're redirecting,
        # rather than just displaying form errors on the same challenge page.
        team = request.user.team
        if not team:
            messages.error(request, NO_TEAM)
            return HttpResponseRedirect(reverse('player', args=[request.user.slug]))

        challenge_flags = [flag.value for flag in challenge.flag_set.all()]

        if attempted_flag in challenge_flags:
            team.points += challenge.points

            if challenge.bonus_limit:
                team.points += challenge.bonus_points
                challenge.bonus_limit -= 1

            if challenge.points:
                challenge.points -= challenge.depreciation
            challenge.save()

            for flag in challenge.flag_set.all():
                team.flags.add(flag)

            messages.success(request, GOOD_FLAG)

        # Wrong flag
        else:
            error_msg = BAD_FLAG
            if team.points:
                error_msg += PENALTY.format(challenge.penalty, team.name)
                team.points -= challenge.penalty
            messages.error(request, error_msg)

        team.save()

    # Form invalid
    else:
        issue_errors(request, form)

    if challenge is not None:
        return HttpResponseRedirect(reverse('challenge', args=[challenge.slug]))
    return HttpResponseRedirect(reverse('challenges'))

