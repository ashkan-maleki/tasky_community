from django.urls import include, path
from rest_framework import routers

from tasks.views import GoalViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register(r'goals', GoalViewSet)
router.register(r'tasks', TaskViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]