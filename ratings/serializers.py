from django.db.models import Avg
from rest_framework import permissions, serializers

from .models import Category, Genre, Title, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["id"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ["id"]


class TitleSerializerRead(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = "__all__"

    def get_rating(self, obj):
        return Review.objects.filter(title=obj).aggregate(Avg("score"))["score__avg"]


class TitleSerializerWrite(TitleSerializerRead):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "text", "author", "score", "date"]
        read_only_fields = ["author", "date"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "date"]
        read_only_fields = ["author", "date"]
