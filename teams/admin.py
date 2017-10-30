from django.contrib            import admin
from django.contrib.auth.admin import Group, UserAdmin
from teams.models              import Player, Team


class PlayerInLine(admin.TabularInline):
    model = Player
    extra = 0

    fields          = ['username', 'email', 'standing']
    readonly_fields = ['username', 'email']

    can_delete = False

    def has_add_permission(self, request):
        return False


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [PlayerInLine]
    list_display = ['__str__', 'team_size', 'points', 'team_captain']
    search_fields = ['name']

    def team_size(self, obj):
        return len(obj.player_set.all())

    def team_captain(self, obj):
        for player in obj.player_set.all():
            if player.standing == Player.CAPTAIN:
                return player.username
        return '-'


@admin.register(Player)
class PlayerAdmin(UserAdmin):
    fieldset  = ('Team membership', {'fields': ['team', 'standing']})
    fieldsets = list(UserAdmin.fieldsets)
    fieldsets.insert(1, fieldset)
    exclude = ['groups']

    list_display  = ['username', 'email', 'team', 'standing', 'is_superuser', 'is_active']
    list_editable = list_display[1:]
    list_filter   = list_display[3:]
    search_fields = ['username', 'email', 'team__name']

    def save_model(self, request, obj, form, change):
        obj.is_staff = obj.is_superuser
        if obj.team and obj.standing == Player.CAPTAIN:
            for player in obj.team.player_set.all():
                if player.username != obj.username and player.standing == Player.CAPTAIN:
                    player.standing = Player.MODERATOR
                    player.save()
        super().save_model(request, obj, form, change)


admin.site.unregister(Group)

