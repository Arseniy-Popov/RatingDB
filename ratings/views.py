from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import TitleFilter
from .models import Category, Genre, Title, Review, Comment
from .permissions import (
    List,
    Create,
    Update,
    Delete,
    Retrieve,
    Read,
    IsAny,
    Any,
    IsAdmin,
    IsAuthenticated,
    IsModerator,
    IsStaff,
    IsOwner,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializerRead,
    TitleSerializerWrite,
    ReviewSerializer,
    CommentSerializer,
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
    permission_classes = [Any(IsAdmin) | Read(IsAny)]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializerRead
        return TitleSerializerWrite


class NestedResourceMixin:
    """
    Mixin for ModelViewSet for nested resources. E.g., in /movies/<movie_id>/reviews/ 
    the 'Review.movie' field references 'Movie' objects identified by <movie_id>.
    Requires class attributes parent_object, parent_field, parent_url_id and
    the _serializer_save_fields method.
    """

    _parent_object, _parent_field, _parent_url_id = None, None, None

    def _serializer_save_fields(self):
        return {}

    def _get_parent(self):
        return get_object_or_404(
            self._parent_object, id=self.kwargs[self._parent_url_id]
        )

    def get_queryset(self):
        parent = self._get_parent()
        return super().get_queryset().filter(**{self._parent_field: parent})

    def perform_create(self, serializer):
        parent = self._get_parent()
        serializer.save(
            **{self._parent_field: parent}, **self._serializer_save_fields()
        )


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        Create(IsAuthenticated)
        | Update(IsOwner)
        | Delete(IsStaff | IsOwner)
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
        | Update(IsOwner)
        | Delete(IsStaff | IsOwner)
        | Read(IsAny)
    ]

    def get_queryset(self):
        review = self._get_review()
        return super().get_queryset().filter(**{"review": review})

    def perform_create(self, serializer):
        serializer.save(**{"review": self._get_review(), "author": self.request.user})

    def _get_review(self):
        return get_object_or_404(Review, id=self.kwargs["review_id"])
