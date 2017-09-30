from django.template import Library

import django.contrib.auth.forms as auth_forms
import teams.forms               as team_forms

register = Library()

@register.inclusion_tag('registration/register_form.html')
def show_register_form():

    register_form = team_forms.RegisterForm()
    team_form     = team_forms.JoinTeamForm()

    joined_fields = list(register_form.visible_fields())
    joined_fields.extend(team_form.visible_fields())

    context = {
        'register_form': register_form,
        'team_form'    : team_form,
        'joined_fields': joined_fields,
    }

    return context

@register.inclusion_tag('registration/join_team_form.html')
def show_join_team_form():
    return {'form': team_forms.JoinTeamForm()}

@register.inclusion_tag('registration/login_form.html')
def show_login_form():
    return {'form': auth_forms.AuthenticationForm()}

@register.inclusion_tag('registration/password_change_form_only.html')
def show_password_change_form(player):
    return {'form': auth_forms.PasswordChangeForm(user=player)}

@register.inclusion_tag('registration/password_reset_form_only.html')
def show_password_reset_form():
    return {'form': auth_forms.PasswordResetForm()}

@register.inclusion_tag('registration/change_team_name.html', takes_context=True)
def show_change_team_name_form(context):
    context.update({'form': team_forms.ChangeTeamName()})
    return context

@register.inclusion_tag('registration/change_team_password.html', takes_context=True)
def show_change_team_password_form(context):
    context.update({'form': team_forms.ChangeTeamPassword()})
    return context

@register.inclusion_tag('registration/promote_demote.html', takes_context=True)
def show_promote_demote_form(context, target_player_username, promote):
    initial = {'target_player_username': target_player_username, 'promote': promote}
    context.update({'form': team_forms.PromoteOrDemotePlayer(initial=initial)})
    return context

@register.inclusion_tag('registration/appoint_captain.html', takes_context=True)
def show_appoint_captain_form(context, target_player_username):
    initial = {'target_player_username': target_player_username}
    context.update({'form': team_forms.AppointNewCaptain(initial=initial)})
    return context

