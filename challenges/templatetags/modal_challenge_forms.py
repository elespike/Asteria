from challenges.forms          import RevealHintForm, SubmitFlagForm
from django.template           import Library

register = Library()

@register.inclusion_tag('challenges/reveal_hint.html')
def show_reveal_hint_form(_id):
    return {'reveal_hint_form': RevealHintForm(initial={'hint_id': _id})}

@register.inclusion_tag('challenges/submit_flag.html')
def show_submit_flag_form(_id):
    return {'submit_flag_form': SubmitFlagForm(initial={'challenge_id': _id})}

