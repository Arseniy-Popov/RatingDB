import pytest

from ratings.models import Genre

from .conftest import TestsBase


@pytest.mark.django_db
class TestsGenre(TestsBase):
    def test_genre_list(self):
        """
        GET /genres
        """
        path, method, body = "/api/v1/genres/", "get", None
        self._assert_allowed_for(
            path,
            method,
            body,
            [None, self.user_1_plain, self.user_2_moderator, self.user_3_admin],
        )
        response = getattr(self._client(None), method)(path, body)
        assert response.data["count"] == 2
        assert response.data["results"][1]["slug"] == self.genre_2.slug

    def test_genre_list_with_search(self):
        """
        GET /genres/?search={genre_name}
        """
        path, method, body = "/api/v1/genres/?search=sci-fi", "get", None
        response = getattr(self._client(None), method)(path, body)
        assert response.data["count"] == 1
        assert response.data["results"][0]["slug"] == "sci-fi"

    def test_genre_retrive(self):
        """
        GET /genres/{genre_slug}
        """
        path, method, body = "/api/v1/genres/sci-fi/", "get", None
        self._assert_allowed_for(
            path,
            method,
            body,
            (None, self.user_1_plain, self.user_2_moderator, self.user_3_admin),
        )
        response = getattr(self._client(None), method)(path, body)
        assert response.data["slug"] == "sci-fi"

    def test_genre_create(self):
        """
        POST /genres
        """
        path, method, body = (
            "/api/v1/genres/",
            "post",
            {"name": "Acion", "slug": "action"},
        )
        self._assert_allowed_for(
            path, method, None, [self.user_2_moderator, self.user_3_admin]
        )
        self._assert_not_allowed_for(path, method, None, [None, self.user_1_plain])
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert response.data["slug"] == "action"
        assert Genre.objects.filter(slug="action").exists()

    def test_genre_update(self):
        """
        PUT /genres/{genre_slug}
        """
        path, method, body = (
            "/api/v1/genres/sci-fi/",
            "put",
            {"name": "Sci-fii", "slug": "sci-fii"},
        )
        self._assert_allowed_for(
            path, method, None, [self.user_2_moderator, self.user_3_admin]
        )
        self._assert_not_allowed_for(path, method, None, [None, self.user_1_plain])
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert response.data["slug"] == "sci-fii"
        assert not Genre.objects.filter(slug="sci-fi").exists()
        assert Genre.objects.filter(slug="sci-fii").exists()

    def test_genre_partial_update(self):
        """
        PATCH /genres/{genre_slug}
        """
        path, method, body = ("/api/v1/genres/sci-fi/", "patch", {"slug": "sci-fii"})
        self._assert_allowed_for(
            path, method, None, [self.user_2_moderator, self.user_3_admin]
        )
        self._assert_not_allowed_for(path, method, None, [None, self.user_1_plain])
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert response.data["slug"] == "sci-fii"
        assert not Genre.objects.filter(slug="sci-fi").exists()
        assert Genre.objects.filter(slug="sci-fii").exists()

    def test_genre_delete(self):
        """
        DELETE /genres/{genre_slug}
        """
        path, method, body = ("/api/v1/genres/sci-fi/", "delete", None)
        self._assert_not_allowed_for(path, method, None, [None, self.user_1_plain])
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert not Genre.objects.filter(slug="sci-fi").exists()
