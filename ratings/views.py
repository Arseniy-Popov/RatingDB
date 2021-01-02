from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import TitleFilter
from .models import Category, Comment, Genre, Review, Title
from .permissions import Any, Create, Delete, List, Read, Retrieve, Update
from .roles import IsAdmin, IsAny, IsAuthenticated, IsAuthor, IsModerator, IsStaff
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializerRead,
    TitleSerializerWrite,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = [Any(IsAdmin) | Read(IsAny)]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    permission_classes = [Any(IsStaff) | Read(IsAny)]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [Any(IsStaff) | Read(IsAny)]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializerRead
        return TitleSerializerWrite


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        Create(IsAuthenticated)
        | Update(IsAuthor)
        | Delete(IsStaff | IsAuthor)
        | Read(IsAny)
    ]

    def get_queryset(self):
        title = self._get_title()
        return super().get_queryset().filter(**{"title": title})

    def perform_create(self, serializer):
        self._check_single_review()
        serializer.save(**{"title": self._get_title(), "author": self.request.user})

    def _get_title(self):
        return get_object_or_404(Title, id=self.kwargs["title_id"])

    def _check_single_review(self):
        title = get_object_or_404(Title, id=self.kwargs["title_id"])
        if Review.objects.filter(author=self.request.user, title=title).exists():
            raise serializers.ValidationError(
                "You can only leave one review per title."
            )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        Create(IsAuthenticated)
        | Update(IsAuthor)
        | Delete(IsStaff | IsAuthor)
        | Read(IsAny)
    ]

    def get_queryset(self):
        review = self._get_review()
        return super().get_queryset().filter(**{"review": review})

    def perform_create(self, serializer):
        serializer.save(**{"review": self._get_review(), "author": self.request.user})

    def _get_review(self):
        return get_object_or_404(Review, id=self.kwargs["review_id"])
