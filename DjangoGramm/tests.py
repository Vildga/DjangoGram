from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Post, Like, Dislike, Tags, PostHasTag
from django.contrib.auth.models import User
import uuid


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(
            id=1,
            count_likes=0,
            count_dislikes=0,
            description='Test Description',
            publication_date=timezone.now(),
            images='test_image.jpg',
            author_id=self.user,
        )
        self.tag = Tags.objects.create(name='Test Tag', link='test-tag', count_users=0)
        self.post_has_tag = PostHasTag.objects.create(post=self.post, tag=self.tag)

    def test_registration_model(self):
        unique_username = f"testuser_{uuid.uuid4().hex[:10]}"
        registration = User.objects.create_user(
            username=unique_username,
            password='testpassword',
            first_name='Test',
            last_name='User',
        )
        self.assertEqual(registration.username, unique_username)

    def test_post_model(self):
        self.assertEqual(self.post.description, 'Test Description')

    def test_like_model(self):
        like = Like.objects.create(user=self.user, post=self.post)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.post, self.post)

    def test_dislike_model(self):
        dislike = Dislike.objects.create(user=self.user, post=self.post)
        self.assertEqual(dislike.user, self.user)
        self.assertEqual(dislike.post, self.post)

    def test_tags_model(self):
        self.assertEqual(self.tag.name, 'Test Tag')


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(
            id=1,
            count_likes=0,
            count_dislikes=0,
            description='Test Description',
            publication_date=timezone.now(),
            images='test_image.jpg',
            author_id=self.user,
        )
        self.tag = Tags.objects.create(name='Test Tag', link='test-tag', count_users=0)
        self.post_has_tag = PostHasTag.objects.create(post=self.post, tag=self.tag)

    def test_post_view(self):
        response = self.client.get(reverse('post_detail', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_upload_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('upload'), {
            'photo': 'test_photo.jpg',
            'description': 'Test Upload Description'
        })
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.post(reverse('registration'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)

    def test_like_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('like_post', args=[self.post.id]))
        self.assertEqual(response.json()['status'], 'success')

    def test_dislike_post(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('dislike_post', args=[self.post.id]))
        self.assertEqual(response.json()['status'], 'success')
