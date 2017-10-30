from announcements.templatetags.announcements_helper_tags import is_registration_open
from django                                               import forms
from django.conf                                          import settings
from django.contrib.auth.forms                            import UserCreationForm
from django.contrib.auth.hashers                          import check_password
from django.contrib.auth.password_validation              import get_password_validators
from django.urls                                          import reverse
from teams.models                                         import Player, Team


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=64, required=False, help_text='Optional for account creation but required for password reset.')

    class Meta(UserCreationForm.Meta):
        model  = Player
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean(self):
        super().clean()
        if not is_registration_open():
            raise forms.ValidationError('Registration is currently closed!')


class JoinTeamForm(forms.Form):
    team_name     = forms.CharField(max_length=64, help_text='Create or join this team. Team name may be changed later.')
    team_password = forms.CharField(max_length=128,
                                    widget=forms.PasswordInput,
                                    help_text='Password to join the team.',
                                    validators=[klass.validate for klass in get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)]
                                   )

    def __init__(self, *args, **kwargs):
        self.player = kwargs.pop('player', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        team_name     = self.cleaned_data.get('team_name')
        team_password = self.cleaned_data.get('team_password')

        if team_name and team_password:
            team = Team.objects.filter(name=team_name).first()
            if team is not None:
                if len(team.player_set.all()) >= settings.MAX_TEAM_SIZE:
                    raise forms.ValidationError('{} is full! Teams can have at most {} players.'.format(team_name, settings.MAX_TEAM_SIZE))
                if not check_password(team_password, team.password):
                    raise forms.ValidationError('Incorrect password for existing team: {}'.format(team_name))

            error_msg = 'You must <a class="alert-anchor" href="{}"><strong>appoint a new team captain</strong></a> before changing teams!'
            if self.player is not None                     \
            and self.player.team is not None               \
            and self.player.is_authenticated()             \
            and len(self.player.team.player_set.all()) > 1 \
            and self.player.standing == Player.CAPTAIN:
                raise forms.ValidationError(error_msg.format(reverse('team', args=[self.player.team.slug])))


class ChangeTeamName(forms.Form):
    new_team_name = forms.CharField(max_length=64)

    def __init__(self, *args, **kwargs):
        self.player = kwargs.pop('player', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        if self.player.standing != Player.CAPTAIN:
            raise forms.ValidationError('Only the Captain can change the team name!')

        new_team_name = self.cleaned_data.get('new_team_name')
        if Team.objects.filter(name=new_team_name).first() is not None:
            raise forms.ValidationError('A team by that name already exists!')


class ChangeTeamPassword(forms.Form):
    new_team_password = forms.CharField(max_length=128,
                                        widget=forms.PasswordInput,
                                        validators=[klass.validate for klass in get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)]
                                       )

    def __init__(self, *args, **kwargs):
        self.player = kwargs.pop('player', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        if self.player.standing != Player.CAPTAIN and self.player.standing != Player.MODERATOR:
            raise forms.ValidationError('Only the Captain or Moderators can change the team password!')


def validate_target_player(player, target_player_username):
    if player.username == target_player_username:
        raise forms.ValidationError('Don\'t be a dick.')

    target_player = Player.objects.filter(username=target_player_username).first()
    if target_player is None:
        raise forms.ValidationError('This player does not exist!')

    if player.team != target_player.team:
        raise forms.ValidationError('This player is not in your team!')


class PromoteOrDemotePlayer(forms.Form):
    target_player_username = forms.CharField   (max_length=32, widget=forms.HiddenInput)
    promote                = forms.BooleanField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.player = kwargs.pop('player', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        if self.player.standing != Player.CAPTAIN:
            raise forms.ValidationError('Only the Captain can appoint or demote moderators!')

        target_player_username = self.cleaned_data.get('target_player_username')
        validate_target_player(self.player, target_player_username)


class AppointNewCaptain(forms.Form):
    target_player_username = forms.CharField(max_length=32, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.player = kwargs.pop('player', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        if self.player.standing != Player.CAPTAIN:
            raise forms.ValidationError('Only the Captain can appoint a new captain!')

        target_player_username = self.cleaned_data.get('target_player_username')
        validate_target_player(self.player, target_player_username)

