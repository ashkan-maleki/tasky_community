from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        task = Task(**validated_data)
        task.user = self.context['request'].user
        task.save()
        return task

    class Meta:
        model = Task
        fields = ['id','title', 'time', 'status', 'priority', 'goal', 'week_day', 'parent']
        read_only_fields = ['id']