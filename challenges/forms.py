from challenges.models                              import Challenge, Hint
from challenges.templatetags.challenges_helper_tags import is_locked, is_solved
from django                                         import forms


class RevealHintForm(forms.Form):
    hint_id = forms.IntegerField(widget=forms.HiddenInput(), min_value=1)

    def __init__(self, *args, **kwargs):
        self.player = kwargs.pop('player', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        hint_id = self.cleaned_data.get('hint_id')
        hint = Hint.objects.filter(pk=hint_id).first()

        if hint is None:
            raise forms.ValidationError('Invalid hint specified!')

        if hint in self.player.team.hints.all():
            raise forms.ValidationError('Your team has already revealed this hint!')

        if is_solved(hint.challenge, self.player.team):
            raise forms.ValidationError('Your team has already completed this challenge!')


class SubmitFlagForm(forms.Form):
    challenge_id   = forms.IntegerField(widget=forms.HiddenInput(), min_value=1)
    attempted_flag = forms.CharField   (widget=forms.TextInput(attrs={'style':'width:80%'}), max_length=128)

    def __init__(self, *args, **kwargs):
        self.player = kwargs.pop('player', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        challenge_id = self.cleaned_data.get('challenge_id')
        challenge = Challenge.objects.filter(pk=challenge_id).first()
        if challenge is None:
            raise forms.ValidationError('Invalid challenge specified!')

        if is_locked(challenge, self.player.team):
            raise forms.ValidationError('This level is currently locked or the CTF is not currently active!')

        if is_solved(challenge, self.player.team):
            raise forms.ValidationError('Your team has already completed this challenge!')

