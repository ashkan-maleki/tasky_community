from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

UNIT_OF_TIME = {
    1: _(u'Year'),
    2: _(u'Month'),
    3: _(u'Day'),
    4: _(u'Day')
}


class Type(models.IntegerChoices):
    LONG_TERM = 1,
    YEARLY = 2,
    MONTHLY = 3,
    WEEKLY = 4


class GoalCore(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    time = models.IntegerField(default=1)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    _default_type = Type.LONG_TERM

    @property
    def time_unit(self):
        unit = UNIT_OF_TIME[self.type]
        if self.time > 1:
            unit = unit + 's'
        return unit

    # _('Long-Term')
    type = models.IntegerField(choices=Type.choices,default=Type.LONG_TERM)

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     if self._state.adding:
    #         self.type = self._default_type
    #     super(GoalCore, self).save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['type', 'time', 'title']
        abstract = True


class Goal(GoalCore, MPTTModel):
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['title']


class LongTermGoalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=1)


class LongTermGoal(Goal):
    object = LongTermGoalManager()
    _default_type = Type.LONG_TERM

    class Meta:
        proxy = True
        verbose_name = "Long-Term Goal"
        verbose_name_plural = "Long-Term Goals"


class YearlyGoalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=2)


class YearlyGoal(Goal):
    object = YearlyGoalManager()
    _default_type = Type.YEARLY

    class Meta:
        proxy = True


class MonthlyGoalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=3)


class MonthlyGoal(Goal):
    object = MonthlyGoalManager()
    _default_type = Type.MONTHLY

    class Meta:
        proxy = True


class WeeklyGoalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=4)


class WeeklyGoal(Goal):
    object = WeeklyGoalManager()
    _default_type = Type.WEEKLY

    class Meta:
        proxy = True
