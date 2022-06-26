from datetime import datetime
from celery import shared_task

from utils import send_mail

from .models import Post


@shared_task(name='publish_premium_posts')
def publish_premium_posts():
    posts = Post.valid_to_publish.filter(pub_date=datetime.today().date(), type="premium").select_related('author')

    author_emails = set([post.author_email_address for post in posts])

    posts.update(status="published")

    if author_emails:
        send_mail(
            author_emails,
            'Published premium posts',
            f'Hello, your pending premium posts have been published'
        )


@shared_task(name='publish_freemium_posts')
def publish_freemium_posts():
    posts = Post.valid_to_publish.filter(pub_date=datetime.today().date(), type="freemium").select_related('author')

    author_emails = set([post.author_email_address for post in posts])

    posts.update(status="published")

    if author_emails:
        send_mail(
            author_emails,
            'Published freemium posts',
            f'Hello, your pending freemium posts have been published'
        )
