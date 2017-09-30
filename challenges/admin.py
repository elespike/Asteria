from challenges     import models as challenge_models
from django         import forms
from django.contrib import admin
from django.db      import models


class LevelAdminForm(forms.ModelForm):
    # Overriding __init__() in order to only display challenges from previous levels.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        number = self.instance.number
        # In order to avoid errors in the query below.
        if number is None:
            number = 0
        queryset = challenge_models.Challenge.objects.filter(level__number__lt=number)

        self.fields['challenges_required'].queryset = queryset


    class Meta:
        model   = challenge_models.Level
        exclude = []


class ChallengeInline(admin.StackedInline):
    model = challenge_models.Challenge
    extra = 0


@admin.register(challenge_models.Level)
class LevelAdmin(admin.ModelAdmin):
    form    = LevelAdminForm
    inlines = [ChallengeInline]

    list_display  = ['__str__', 'description', 'points_required', 'percentage_required']
    list_editable = list_display[2:]


@admin.register(challenge_models.Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    inlines = [ChallengeInline]
    list_display = ['__str__', 'description']


# In order for the default flag values to always be saved,
# even if unchanged.
class AlwaysChangedModelForm(forms.ModelForm):
    def has_changed(self):
        return True


class FlagInline(admin.TabularInline):
    model   = challenge_models.Flag
    min_num = 1
    extra   = 0
    form    = AlwaysChangedModelForm


class HintInline(admin.TabularInline):
    model = challenge_models.Hint
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(
            attrs={
                'rows' : 1 ,
                'cols' : 32,
                'style': 'height: 18px;'
            }
        )}
    }
    extra = 0


class LinkInline(admin.TabularInline):
    model = challenge_models.Link
    extra = 0


class FileInline(admin.TabularInline):
    model = challenge_models.File
    extra = 0


@admin.register(challenge_models.Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    inlines = [
        FlagInline,
        HintInline,
        LinkInline,
        FileInline,
    ]
    list_display = [
        '__str__'     ,
        'description' ,
        'level'       ,
        'category'    ,
        'points'      ,
        'bonus_points',
        'bonus_limit' ,
        'depreciation',
        'penalty'
    ]
    list_editable = list_display[2:]
    list_filter   = list_display[2:4]

