import pytest

from rest_framework.test import APIClient

from ratings.models import Genre, Category, User, Title


@pytest.mark.django_db
class TestsBase:
    @pytest.fixture(autouse=True)
    def prepopulated_data(self):
        category_movie = Category.objects.create(name="Movie", slug="movie")
        category_series = Category.objects.create(name="Series", slug="series")
        genre_comedy = Genre.objects.create(name="Comedy", slug="comedy")
        genre_scifi = Genre.objects.create(name="Sci-fi", slug="sci-fi")
        title_1 = Title.objects.create(
            name="Star Wars IV", year=1977, category=category_movie
        )
        title_1.genre.add(genre_scifi)
        title_2 = Title.objects.create(
            name="The Good Place",
            year=1977,
            category=category_movie,
        )
        title_2.genre.add(genre_scifi)
        self.user_1_plain = User.objects.create_user(
            username="user_1_plain", password="testpswd"
        )
        self.user_2_moderator = User.objects.create_user(
            username="user_2_moderator", password="testpswd", is_moderator=True
        )
        self.user_3_admin = User.objects.create_user(
            username="user_3_admin", password="testpswd", is_admin=True
        )

    def _client(self, user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    def _assert_allowed_for(self, url, method, body, users):
        for user in users:
            response = getattr(self._client(user), method)(url, body)
            assert response.status_code not in (401, 403)

    def _assert_not_allowed_for(self, url, method, body, users):
        for user in users:
            response = getattr(self._client(user), method)(url, body)
            assert response.status_code in (401, 403)
