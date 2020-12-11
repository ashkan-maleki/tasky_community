from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.core.paginator import Paginator
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from tasks.models import Goal, goals
from tasks.serializers import GoalSerializer

GOAL_URL = reverse('api:goal-list')


def detail_url(goal_id):
    """Return goal detail URL"""
    return reverse('api:goal-detail', args=[goal_id])


def sample_goal(title, type=goals.Type.LONG_TERM, time=2, parent=None):
    """Create and return a sample tag"""
    return Goal.objects.create(title=title, type=type, time=time, parent=parent)


class PublicGoalsApiTests(TestCase):
    """Test the publicly availaable goals API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(GOAL_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateGoalsApiTests(TestCase):
    """Test the private goals API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'me@jc.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_goal_list(self):
        """Test retrieving a list of goals"""
        Goal.objects.create(title='Buying a house')
        Goal.objects.create(title='Being a billion dollars')

        res = self.client.get(GOAL_URL + '?page=1')

        goals = Goal.objects.all().order_by('title')
        p = Paginator(goals, 10)
        serializer = GoalSerializer(p.page(1), many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_retrieve_goal_list_page_2(self):
        """Test retrieving a list of goals"""
        Goal.objects.create(title='Buying a house')
        Goal.objects.create(title='Being a billionaire')

        res = self.client.get(GOAL_URL + '?page=2')

        goals = Goal.objects.all()
        p = Paginator(goals, 10)
        self.assertEqual(p.num_pages, 1)
        if p.num_pages > 1:
            serializer = GoalSerializer(p.page(2), many=True)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data['results'], serializer.data)
        else:
            self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_goal_successful(self):
        """Test create a new goal"""
        payload = {'title': 'becoming famous', 'type': goals.Type.LONG_TERM, 'time': 2}
        res = self.client.post(GOAL_URL, payload)

        exists = Goal.objects.filter(
            title=payload['title']
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_goal_invalid(self):
        """Test creating invalid goal fails"""
        payload = {'title': ''}
        res = self.client.post(GOAL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_goal_detail(self):
        """Test viewing a goal detail"""
        goal = sample_goal(title="becoming famous")

        url = detail_url(goal.id)
        res = self.client.get(url)

        serializer = GoalSerializer(goal)
        self.assertEqual(res.data, serializer.data)

    def test_partial_update_recipe(self):
        """Test updating a recipe with patch"""
        goal = sample_goal(title='becoming a singer')
        payload = {'title': 'becoming a painter'}
        url = detail_url(goal.id)
        self.client.patch(url, payload)

        goal.refresh_from_db()
        self.assertEqual(goal.title, payload['title'])

    def test_full_update_recipe(self):
        """Test updating a recipe with put"""
        goal = sample_goal(title='becoming a singer')
        payload = {
            'title': 'becoming a painter',
            'type': goal.type,
            'time': goal.time
        }
        url = detail_url(goal.id)
        res = self.client.put(url, payload)

        goal.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(goal.title, payload['title'])

    def test_delete_goal_successful(self):
        """Test delete a new goal"""
        goal = sample_goal(title='becoming a singer')
        goal_id = goal.id
        url = detail_url(goal.id)
        self.client.delete(url)

        exists = Goal.objects.filter(
            id=goal_id
        ).exists()
        self.assertFalse(exists)
