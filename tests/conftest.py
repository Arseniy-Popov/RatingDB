import base64

import pytest
from rest_framework.test import APIClient

from ratings.models import Category, Comment, Genre, Review, Title, User

URL_BASE = "/api/v1"


@pytest.mark.django_db
class TestsBase:
    @pytest.fixture(autouse=True)
    def prepopulated_data(self):
        # Categories
        self.category_1 = Category.objects.create(name="Movie", slug="movie")
        self.category_2 = Category.objects.create(name="Series", slug="series")
        # Genres
        self.genre_1 = Genre.objects.create(name="Comedy", slug="comedy")
        self.genre_2 = Genre.objects.create(name="Sci-fi", slug="sci-fi")
        # Titles
        self.title_1 = Title.objects.create(
            name="Star Wars IV", year=1977, category=self.category_1
        )
        self.title_1.genre.add(self.genre_2)
        self.title_2 = Title.objects.create(
            name="The Good Place", year=2016, category=self.category_2
        )
        self.title_2.genre.add(self.genre_1)
        # Users
        self.user_1_plain = User.objects.create_user(
            username="user_1_plain", password="testpswd"
        )
        self.user_2_moderator = User.objects.create_user(
            username="user_2_moderator", password="testpswd", is_moderator=True
        )
        self.user_3_admin = User.objects.create_user(
            username="user_3_admin", password="testpswd", is_admin=True
        )
        self.user_4_plain = User.objects.create_user(
            username="user_4_plain", password="testpswd"
        )
        # Reviews
        self.review_1 = Review.objects.create(
            title=self.title_1, text="Good!", author=self.user_1_plain, score=8
        )
        self.review_2 = Review.objects.create(
            title=self.title_1, text="Okay.", author=self.user_4_plain, score=5
        )
        # Comments
        self.comment_1 = Comment.objects.create(
            review=self.review_2, text="True.", author=self.user_4_plain
        )
        self.comment_2 = Comment.objects.create(
            review=self.review_2, text="Not true.", author=self.user_1_plain
        )

    def _client(self, user):
        """
        Returns a client with attached credentials of the `user`. Represents
        an unauthorized user if `user` is None.
        """
        client = APIClient()
        if user:
            credentials = f"{user.username}:testpswd"
            credentials = credentials.encode()
            client.credentials(
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(credentials).decode()}"
            )
        return client

    def _assert_allowed_for(self, url, method, body, users):
        for user in users:
            response = getattr(self._client(user), method)(url, body)
            assert response.status_code not in (401, 403), f"{user}"

    def _assert_not_allowed_for(self, url, method, body, users):
        for user in users:
            response = getattr(self._client(user), method)(url, body)
            assert response.status_code in (401, 403)
