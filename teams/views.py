import teams.forms as team_forms

from common.helper_functions import (
    issue_errors
)
from django.contrib import (
    messages
)
from django.contrib.auth.decorators import (
    login_required
)
from django.contrib.auth.hashers import (
    make_password
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin
)
from django.http import (
    HttpResponseRedirect
)
from django.shortcuts import (
    render
)
from django.urls import (
    reverse
)
from django.utils.text import (
    slugify
)
from django.views.generic import (
    DetailView,
    ListView,
)
from teams.models import (
    Player,
    Team,
)


def register(request):
    register_form = team_forms.RegisterForm(request.POST or None)
    team_form = team_forms.JoinTeamForm(request.POST or None)

    if register_form.is_valid() and team_form.is_valid():
        register_form.save()

        player = Player.objects.get(
            username=register_form.cleaned_data['username']
        )
        player.slug = slugify(player.username)

        request.user = player
        join_team(request, player)

        messages.success(request, 'Successfully registered! Please log in.')
        return HttpResponseRedirect(reverse('login'))

    joined_fields = list(register_form.visible_fields())
    joined_fields.extend(team_form.visible_fields())

    context = {
        'register_form': register_form,
        'team_form': team_form,
        'joined_fields': joined_fields,
    }

    return render(request, 'registration/register.html', context)


@login_required
def join_team(request, player=None):
    form = team_forms.JoinTeamForm(
        request.POST or None,
        player=request.user
    )

    if form.is_valid():
        if player is None:
            player = request.user

        team_name = form.cleaned_data['team_name']
        team_password = form.cleaned_data['team_password']
        previous_team = player.team

        team = Team.objects.filter(name=team_name).first()

        if team is None:
            team = Team(
                name=team_name,
                slug=slugify(team_name),
                password=make_password(team_password)
            )
        if len(team.player_set.all()) == 0:
            team.password = make_password(team_password)
            player.standing = Player.CAPTAIN
        else:
            player.standing = Player.PLAYER

        player.save()
        team.save()

        # Assign player to new team
        team.player_set.add(player)

        # Remove player's old team if no one is left
        if (previous_team
        and len(previous_team.player_set.all()) == 0):
            previous_team.delete()

        return HttpResponseRedirect(reverse('team', args=[team.slug]))

    return render(request, 'registration/join_team.html', {'form': form})


@login_required
def change_team_name(request):
    form = team_forms.ChangeTeamName(
        request.POST or None,
        player=request.user
    )

    if form.is_valid():
        new_team_name = form.cleaned_data['new_team_name']

        team = request.user.team
        team.name = new_team_name
        team.slug = slugify(new_team_name)
        team.save()

    else:
        issue_errors(request, form)

    return HttpResponseRedirect(
        reverse('team', args=[request.user.team.slug])
    )


@login_required
def change_team_password(request):
    form = team_forms.ChangeTeamPassword(
        request.POST or None,
        player=request.user
    )

    if form.is_valid():
        new_team_password = form.cleaned_data['new_team_password']

        team = request.user.team
        team.password = make_password(new_team_password)
        team.save()

    else:
        issue_errors(request, form)

    return HttpResponseRedirect(
        reverse('team', args=[request.user.team.slug])
    )


@login_required
def promote_demote(request):
    form = team_forms.PromoteOrDemotePlayer(
        request.POST or None,
        player=request.user
    )

    if form.is_valid():
        target_username = form.cleaned_data['target_username']
        promote = form.cleaned_data['promote']

        target_player = Player.objects.get(username=target_username)

        if promote:
            target_player.standing = Player.MODERATOR
        else:
            target_player.standing = Player.PLAYER

        target_player.save()

    else:
        issue_errors(request, form)

    return HttpResponseRedirect(
        reverse('team', args=[request.user.team.slug])
    )


@login_required
def appoint_captain(request):
    form = team_forms.AppointNewCaptain(
        request.POST or None,
        player=request.user
    )

    if form.is_valid():
        target_username = form.cleaned_data['target_username']

        target_player = Player.objects.get(username=target_username)
        old_captain = request.user

        target_player.standing = Player.CAPTAIN
        old_captain  .standing = Player.MODERATOR

        target_player.save()
        old_captain  .save()

    else:
        issue_errors(request, form)

    return HttpResponseRedirect(
        reverse('team', args=[request.user.team.slug])
    )


class PlayerView(LoginRequiredMixin, DetailView):
    model = Player
    context_object_name = 'player'


class TeamView(LoginRequiredMixin, DetailView):
    model = Team
    context_object_name = 'team'


class ScoreboardView(ListView):
    model = Team
    context_object_name = 'teams'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(points__gt=0)
