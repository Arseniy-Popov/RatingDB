import pytest

from rest_framework.test import APIClient

from ratings.models import Title, Category, Comment, User, Genre, Review


@pytest.mark.django_db
class TestsBase:
    @pytest.fixture(autouse=True)
    def prepopulated_data(self):
        # Categories
        movie = Category.objects.create(name="Movie", slug="movie")
        series = Category.objects.create(name="Series", slug="series")
        # Genres
        comedy = Genre.objects.create(name="Comedy", slug="comedy")
        scifi = Genre.objects.create(name="Sci-fi", slug="sci-fi")
        # Titles
        title_1 = Title.objects.create(name="Star Wars IV", year=1977, category=movie)
        title_1.genre.add(scifi)
        title_2 = Title.objects.create(
            name="The Good Place", year=2016, category=series
        )
        title_2.genre.add(comedy)
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
        review_1 = Review.objects.create(
            title=title_1, text="Good!", author=self.user_1_plain, score=8
        )
        review_2 = Review.objects.create(
            title=title_1, text="Okay.", author=self.user_4_plain, score=5
        )
        # Comments
        self.comment_1 = Comment.objects.create(
            review=review_2, text="True.", author=self.user_4_plain
        )
        self.comment_2 = Comment.objects.create(
            review=review_2, text="Not true.", author=self.user_1_plain
        )

    def _client(self, user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    def _assert_allowed_for(self, url, method, body, users):
        for user in users:
            response = getattr(self._client(user), method)(url, body)
            assert response.status_code not in (401, 403), f"{user}"

    def _assert_not_allowed_for(self, url, method, body, users):
        for user in users:
            response = getattr(self._client(user), method)(url, body)
            assert response.status_code in (401, 403)
