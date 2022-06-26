import datetime
import tempfile

from PIL import Image
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from accounts.models import User
from blog.models import Post


class BlogPostTests(APITestCase):
    def setUp(self):
        admin = User.objects.create(username="admin", is_admin=True, email='admin1@tell-all.com')
        User.objects.create(username="reader", email='reader@gmail.com')
        Post.objects.create(title="Test-1", summary="summarized-1",
                            body="<h1>Body</h1>", author=admin)

    def test_create_blog_post(self):
        """
        Ensure we can create a new blog post
        """

        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        url = reverse('post_add')
        data = {
            'title': 'Testing-1',
            'summary': 'summarized testing-1',
            'body': '<h1>Body</h1>',
            'pub_date': '2022-11-02'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.first().slug, 'testing-1')

        # test a post with cover picture is created
        cover_picture = Image.new('RGB', (150, 150))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        cover_picture.save(tmp_file)

        with open(tmp_file.name, 'rb') as data:
            self.client.post(url, {
                'title': 'Test-2',
                'summary': 'summarized test-2',
                'body': '<h1>Body</h1>',
                'pub_date': '2022-11-02',
                'cover_picture': data
            })

        self.assertEqual(Post.objects.count(), 3)
        self.assertIsNotNone(Post.objects.last().cover_picture)

        # test a post with no title is not created
        no_title_response = self.client.post(url, {
            'title': '',
            'summary': 'summarized test-1',
            'body': '<h1>Body</h1>',
            'pub_date': '2022-11-02'
        })

        self.assertEqual(no_title_response.status_code, 400)

        # test a post with an existing title is not created
        title_exist_response = self.client.post(url, {
            'title': 'Test-1',
            'summary': 'summarized test-1',
            'body': '<h1>Body</h1>',
            'pub_date': '2022-11-02'
        })

        self.assertEqual(title_exist_response.status_code, 400)

        # test a post with pub_date <= today is not created
        pub_date_response = self.client.post(url, {
            'title': 'Test-1',
            'summary': 'summarized test-1',
            'body': '<h1>Body</h1>',
            'pub_date': '2022-1-02'
        })

        self.assertEqual(pub_date_response.status_code, 400)

    def test_edit_blog_post(self):
        """
        Ensure we can edit an existing blog post
        """

        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        url = reverse('post_edit', kwargs={'slug': 'test-1'})
        data = {
            'title': 'Edited-Test-1',
            'summary': 'summarized test-editing-1',
            'body': '<h1>Body</h1><body></body>',
            'pub_date': '2022-12-02'
        }
        self.client.put(url, data)

        # check that a title cannot be edited
        self.assertEqual(Post.objects.get(slug='test-1').title, 'Test-1')
        self.assertEqual(Post.objects.get(slug='test-1').summary, 'summarized test-editing-1')
        self.assertEqual(Post.objects.get(slug='test-1').body, '<h1>Body</h1><body></body>')
        self.assertEqual(Post.objects.get(slug='test-1').pub_date, datetime.date(2022, 12, 2))

    def test_get_all_post(self):
        """
        Ensure we can get all post
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        url = reverse('post_list_all')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('data')), 1)
        self.assertIsNotNone(response.data.get('count'))
        self.assertIsNotNone(response.data.get('message'))

    def test_get_post(self):
        """
        Ensure the endpoint returns only published post
        """
        admin = User.objects.get(username='admin')
        for i in range(1, 4):
            Post.objects.create(title=f"Unpublished-{i}",
                                summary=f"summarized-unpublished-{i}",
                                body="<h1>Hello</h1>", author=admin)

        last_post = Post.objects.first()
        last_post.status = "published"
        last_post.save()
        url = reverse('post_list_published')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('data')), 1)
        self.assertIsNotNone(response.data.get('count'))
        self.assertIsNotNone(response.data.get('message'))

    def test_delete_post(self):
        """
        Ensure we can delete an existing blog post
        """

        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)
        url = reverse('post_delete', kwargs={'slug': 'test-1'})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

        url = reverse('post_delete', kwargs={'slug': 'test-20'})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_permission(self):
        admin = User.objects.get(username='admin')
        reader = User.objects.get(username='reader')
        data = {
            'title': 'Edited-Test-1',
            'summary': 'summarized test-editing-1',
            'body': '<h1>Body</h1><body></body>',
            'pub_date': '2022-12-02'
        }

        # test all endpoint that requires authentication
        create_post_url = reverse('post_add')
        response = self.client.post(create_post_url, data)
        self.assertEqual(response.status_code, 401)

        edit_post_url = reverse('post_edit', kwargs={'slug': 'test-1'})
        response = self.client.put(edit_post_url, data)
        self.assertEqual(response.status_code, 401)

        all_post_url = reverse('post_list_all')
        response = self.client.get(all_post_url, data)
        self.assertEqual(response.status_code, 401)

        delete_post_url = reverse('post_delete', kwargs={'slug': 'test-1'})
        response = self.client.delete(delete_post_url, data)
        self.assertEqual(response.status_code, 401)

        post_url = reverse('post_list_published')
        response = self.client.get(post_url, data)
        self.assertEqual(response.status_code, 200)

        Token.objects.create(user=admin)
        token = Token.objects.get(user=admin)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        create_post_url = reverse('post_add')
        response = client.post(create_post_url, data)
        self.assertEqual(response.status_code, 201)

        edit_post_url = reverse('post_edit', kwargs={'slug': 'test-1'})
        response = client.put(edit_post_url, data)
        self.assertEqual(response.status_code, 200)

        all_post_url = reverse('post_list_all')
        response = client.get(all_post_url, data)
        self.assertEqual(response.status_code, 200)

        delete_post_url = reverse('post_delete', kwargs={'slug': 'test-1'})
        response = client.delete(delete_post_url, data)
        self.assertEqual(response.status_code, 204)

        # test with an authenticated non admin user
        Token.objects.create(user=reader)
        token = Token.objects.get(user=reader)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        create_post_url = reverse('post_add')
        response = client.post(create_post_url, data)
        self.assertEqual(response.status_code, 403)

        edit_post_url = reverse('post_edit', kwargs={'slug': 'test-1'})
        response = client.put(edit_post_url, data)
        self.assertEqual(response.status_code, 403)

        all_post_url = reverse('post_list_all')
        response = client.get(all_post_url, data)
        self.assertEqual(response.status_code, 403)

        delete_post_url = reverse('post_delete', kwargs={'slug': 'test-1'})
        response = client.delete(delete_post_url, data)
        self.assertEqual(response.status_code, 403)
