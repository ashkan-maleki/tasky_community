from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Task, ThisWeekTask, Goal, LongTermGoal, YearlyGoal, MonthlyGoal, WeeklyGoal
from .models.tasks import DAY_OF_THE_WEEK, NextWeekTask, TodayTask, OlderTask


class WeekDayListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('week day')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'weekday'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """

        return tuple(DAY_OF_THE_WEEK.items())
        # return (
        #     ('80s', _('in the eighties')),
        #     ('90s', _('in the nineties')),
        # )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() is None:
            return queryset
        return queryset.filter(time__iso_week_day=int(self.value()))


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'time', 'status', 'priority', 'goal', 'week_day', 'parent')
    list_editable = ('title', 'status', 'priority','goal', 'parent')
    list_filter = (WeekDayListFilter, 'status',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(TaskAdmin, self).save_model(request, obj, form, change)


class ThisWeekTaskAdmin(TaskAdmin):
    pass


class NextWeekTaskAdmin(TaskAdmin):
    pass


class TodayTaskAdmin(TaskAdmin):
    list_display = ('id','title', 'status', 'priority', 'goal', 'parent')
    list_filter = ('status',)


class OlderTaskAdmin(TaskAdmin):
    pass


class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'time', 'time_unit', 'parent')
    list_editable = ('title', 'type', 'time', 'parent')
    list_filter = ('type',)


class LimitedGoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time', 'parent')
    list_editable = ('title', 'time', 'parent')
    fields = ('title', 'description', 'time', 'parent')


class LongTermGoalAdmin(LimitedGoalAdmin):
    pass


class YearlyGoalAdmin(LimitedGoalAdmin):
    pass


class MonthlyGoalAdmin(LimitedGoalAdmin):
    pass


class WeeklyGoalAdmin(LimitedGoalAdmin):
    pass


# https://stackoverflow.com/questions/6103672/django-admin-form-how-to-change-select-options-dynamically/6128376
admin.site.register(Task, TaskAdmin)
admin.site.register(ThisWeekTask, ThisWeekTaskAdmin)
admin.site.register(NextWeekTask, NextWeekTaskAdmin)
admin.site.register(TodayTask, TodayTaskAdmin)
admin.site.register(OlderTask, OlderTaskAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(LongTermGoal, LongTermGoalAdmin)
admin.site.register(YearlyGoal, YearlyGoalAdmin)
admin.site.register(MonthlyGoal, MonthlyGoalAdmin)
admin.site.register(WeeklyGoal, WeeklyGoalAdmin)
