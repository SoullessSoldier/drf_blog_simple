from rest_framework.relations import SlugRelatedField
from api.models import Post
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Category

class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'owner', 'posts']

class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'posts', 'comments', 'categories']


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner', 'comments', 'categories']


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ['id', 'body', 'owner', 'post']

class FilteredPaperSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        # Get the parameter from the URL
        show_published_only = self.context['request'].query_params['show_published_only']

        data = data.filter(is_published=show_published_only)
        return super(FilteredPaperSerializer, self).to_representation(data)

class PostSerializer1(serializers.ModelSerializer):
    post = FilteredPaperSerializer(
        many=True,
        read_only=True,
        source='paper_set'
    )

    class Meta:
        model = Author