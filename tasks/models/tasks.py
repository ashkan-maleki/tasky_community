from datetime import datetime, timedelta

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeOneToOneField

DAY_OF_THE_WEEK = {
    1: _(u'Monday'),
    2: _(u'Tuesday'),
    3: _(u'Wednesday'),
    4: _(u'Thursday'),
    5: _(u'Friday'),
    6: _(u'Saturday'),
    7: _(u'Sunday')
}


# Create your models here.
class TaskCore(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(default=1)
    time = models.DateTimeField()
    goal = models.ForeignKey(
        'Goal',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    estimate_time = models.IntegerField(blank=True, null=True)
    completed_time = models.IntegerField(blank=True, null=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    @property
    def week_day(self):
        return DAY_OF_THE_WEEK[self.time.weekday() + 1]

    class Status(models.IntegerChoices):
        NEW = 1
        ACTIVE = 2
        DONE = 3
        POSTPONED = 4
        CONTINUED = 5
        IGNORED = 6

    status = models.IntegerField(choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ['status', 'time', '-priority']


class Task(TaskCore, MPTTModel):
    parent = TreeOneToOneField(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child'
    )

    class MPTTMeta:
        order_insertion_by = ['title']


def get_beginning_ending_of_week(date=None):
    if date is None:
        date = timezone.now().today().date()
    today_weekday = date.weekday()
    if today_weekday == 0:
        week_beginning = date
    else:
        week_beginning = date - timedelta(days=today_weekday)

    week_ending = date + timedelta(days=7 - today_weekday)
    return week_beginning, week_ending


class ThisWeekTaskManager(models.Manager):
    def get_queryset(self):
        this_week_beginning, this_week_ending = get_beginning_ending_of_week()
        return super().get_queryset().filter(Q(time__gte=this_week_beginning)
                                             & Q(time__lt=this_week_ending))


class ThisWeekTask(Task):
    object = ThisWeekTaskManager()

    class Meta:
        proxy = True


class NextWeekTaskManager(models.Manager):
    def get_queryset(self):
        date = timezone.now().today().date() + timedelta(days=7)
        next_week_beginning, next_week_ending = get_beginning_ending_of_week(date)
        return super().get_queryset().filter(Q(time__gte=next_week_beginning)
                                             & Q(time__lt=next_week_ending))


class NextWeekTask(Task):
    object = NextWeekTaskManager()

    class Meta:
        proxy = True


class TodayTaskManager(models.Manager):
    def get_queryset(self):
        date = timezone.now().today().date()
        return super().get_queryset().filter(Q(time__date=date))


class TodayTask(Task):
    object = TodayTaskManager()

    class Meta:
        proxy = True
        ordering = ['status', '-priority']


class OlderTaskManager(models.Manager):
    def get_queryset(self):
        date = timezone.now().today().date()
        return super().get_queryset().filter(Q(time__date__lt=date))


class OlderTask(Task):
    object = OlderTaskManager()

    class Meta:
        proxy = True
