from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from tasks.models import Goal, Task
from tasks.serializers import GoalSerializer, TaskSerializer


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.goals.all()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.tasks.all()
