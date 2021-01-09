from django.db.models import Avg
from rest_framework import permissions, serializers

from .models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["id"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ["id"]


class TitleSerializerWrite(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genres = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )

    class Meta:
        model = Title
        fields = "__all__"


class TitleSerializerRead(TitleSerializerWrite):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = Review.objects.filter(title=obj).aggregate(Avg("score"))["score__avg"]
        return round(rating, 2) if rating else rating


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
