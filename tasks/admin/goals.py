from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from tasks.models import Goal, LongTermGoal, YearlyGoal, MonthlyGoal, WeeklyGoal

class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'time', 'time_unit', 'parent')
    list_editable = ('title', 'type', 'time')
    list_filter = ('type',)

    fieldsets = (
        (None, {
            'fields': ('title', 'type', 'time')
        }),
        ('More options', {
            'classes': ('collapse',),
            'fields': ('parent', 'description'),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(GoalAdmin, self).save_model(request, obj, form, change)


class LimitedGoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time', 'parent')
    list_editable = ('title', 'time')

    fieldsets = (
        (None, {
            'fields': ('title', 'time')
        }),
        ('More options', {
            'classes': ('collapse',),
            'fields': ('parent', 'description'),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(LimitedGoalAdmin, self).save_model(request, obj, form, change)

class LongTermGoalAdmin(LimitedGoalAdmin):
    pass


class YearlyGoalAdmin(LimitedGoalAdmin):
    pass


class MonthlyGoalAdmin(LimitedGoalAdmin):
    pass


class WeeklyGoalAdmin(LimitedGoalAdmin):
    pass