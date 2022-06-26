from rest_framework import serializers

from datetime import datetime
from .models import Post, Tags


class PostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        queryset=Tags.objects.all(),
        many=True,
        slug_field='name'
    )

    class Meta:
        model = Post
        fields = ['title', 'summary', 'body', 'cover_picture', 'type',
                  'pub_date', 'tags']

    def validate_title(self, title):
        if Post.objects.filter(title=title).exists():
            raise serializers.ValidationError("post with this title exist")
        return title

    def validate_pub_date(self, pub_date):
        if pub_date <= datetime.today().date():
            raise serializers.ValidationError("pub date must be a future date")
        return pub_date


class PostListSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Post
        fields = ['title', 'slug', 'summary', 'cover_picture', 'author_email_address',
                  'status', 'type', 'tags']


class PostEditSerializer(serializers.ModelSerializer):

    tags = serializers.SlugRelatedField(
        queryset=Tags.objects.all(),
        many=True,
        slug_field='name'
    )

    class Meta:
        model = Post
        fields = ['summary', 'body', 'cover_picture', 'type', 'pub_date', 'tags']

    def validate_title(self, title):
        if Post.published_objects.filter(title=title).exists():
            raise serializers.ValidationError("a published post cannot be edited")
        return title

    def validate_pub_date(self, pub_date):
        if pub_date <= datetime.today().date():
            raise serializers.ValidationError("pub date must be a future date")
        return pub_date
