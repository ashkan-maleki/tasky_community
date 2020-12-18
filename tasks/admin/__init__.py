from django.contrib import admin

from tasks.admin.goals import GoalAdmin, LongTermGoalAdmin, YearlyGoalAdmin, MonthlyGoalAdmin, WeeklyGoalAdmin
from tasks.admin.tasks import TaskAdmin, ThisWeekTaskAdmin, NextWeekTaskAdmin, TodayTaskAdmin, OlderTaskAdmin
from tasks.models import Task, ThisWeekTask, Goal, LongTermGoal, YearlyGoal, MonthlyGoal, WeeklyGoal
from tasks.models.tasks import NextWeekTask, TodayTask, OlderTask








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