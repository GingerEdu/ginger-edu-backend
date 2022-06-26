import datetime
from django.test import Client, TestCase

from accounts.models import User
from blog.models import Post
from blog.tasks import publish_premium_posts, publish_freemium_posts


class BlogTaskTests(TestCase):
    def setUp(self):
        self.client = Client()
        admin = User.objects.create(username="admin", is_admin=True,
                                    email='admin1@tell-all.com')
        for i in range(50):
            Post.objects.create(title=f"title-{i}",
                                summary=f"summarized-{i}",
                                body="<h1>Body</h1>",
                                cover_picture="http://yourstoryherinspo.com/wp-content/uploads/2021/11/PIC_TEST.png",
                                author=admin)

    def test_publish_freemium_posts(self):
        for post in Post.objects.all()[:10]:
            post.pub_date = datetime.datetime.today().date()
            post.save()

        publish_freemium_posts()

        self.assertEqual(Post.published_objects.filter(type="freemium").count(), 10)
        self.assertEqual(Post.draft_objects.filter(type="freemium").count(), 40)

    def test_publish_premium_posts(self):
        for post in Post.objects.all()[:20]:
            post.type = "premium"
            post.pub_date = datetime.datetime.today().date()
            post.save()
        
        for post in Post.objects.all()[20:30]:
            post.type = "premium"
            post.pub_date = datetime.date(2020, 12, 2)
            post.save()

        publish_premium_posts()

        self.assertEqual(Post.published_objects.filter(type="premium").count(), 20)
        self.assertEqual(Post.draft_objects.filter(type="premium").count(), 10)
