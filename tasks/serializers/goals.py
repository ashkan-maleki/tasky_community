from rest_framework import serializers

from ..models import Goal


class GoalSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        goal = Goal(**validated_data)
        goal.user = self.context['request'].user
        goal.save()
        return goal

    class Meta:
        model = Goal
        fields = ['id', 'title', 'type', 'time', 'time_unit', 'parent']
        read_only_fields = ['id']
