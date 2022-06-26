from django.db import models
from django.template.defaultfilters import slugify

from accounts.models import User

# Create your models here.

STATUS = (
    ("draft", "Draft"),
    ("published", "Published"),
)

TYPES = (
    ("freemium", "Freemium"),
    ("premium", "Premium"),
)


class DraftManager(models.Manager):
    def get_queryset(self):
        return super(DraftManager, self).get_queryset().filter(status="draft")


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")


class ValidToPublishManager(models.Manager):
    def get_queryset(self):
        return super(ValidToPublishManager, self).\
            get_queryset().filter(summary__isnull=False, body__isnull=False,
                                  cover_picture__isnull=False, status="draft")


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tags(BaseModel):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Post(BaseModel):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    summary = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    cover_picture = models.ImageField(upload_to='cover-picture/', max_length=100, null=True)
    status = models.CharField(choices=STATUS, default="draft", max_length=20)
    type = models.CharField(choices=TYPES, default="freemium", max_length=20)
    pub_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    tags = models.ManyToManyField(Tags, blank=True)

    objects = models.Manager()
    draft_objects = DraftManager()
    published_objects = PublishedManager()
    valid_to_publish = ValidToPublishManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    @property
    def author_email_address(self):
        return self.author.email


class PostEdit(BaseModel):
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
