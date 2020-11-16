from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core.model import exercise,routine,workout
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields':  ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (
            _('Important Dates'), {
                'fields': ('last_login',)
            }
        )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(exercise.Exercise)
admin.site.register(workout.Set)
admin.site.register(workout.Workout)
admin.site.register(workout.Serie)
admin.site.register(routine.RoutineDay)
admin.site.register(routine.Routine)
admin.site.register(routine.SetRoutine)
admin.site.register(routine.SerieRoutine)
