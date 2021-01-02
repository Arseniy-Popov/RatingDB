import pytest

from .conftest import TestsBase

from ratings.models import Category


@pytest.mark.django_db
class TestsCategory(TestsBase):
    def test_category_list(self):
        """
        GET /categories
        """
        path, method, body = "/api/v1/categories/", "get", None
        self._assert_allowed_for(
            path,
            method,
            body,
            [None, self.user_1_plain, self.user_2_moderator, self.user_3_admin],
        )
        response = getattr(self._client(None), method)(path, body)
        assert response.data["count"] == 2
        assert response.data["results"][0]["slug"] == "movie"

    def test_category_list_with_search(self):
        """
        GET /categories/?search={category_name}
        """
        path, method, body = "/api/v1/categories/?search=series", "get", None
        response = getattr(self._client(None), method)(path, body)
        assert response.data["count"] == 1
        assert response.data["results"][0]["slug"] == "series"

    def test_category_retrive(self):
        """
        GET /categories/{category_slug}
        """
        path, method, body = "/api/v1/categories/series/", "get", None
        self._assert_allowed_for(
            path,
            method,
            body,
            (None, self.user_1_plain, self.user_2_moderator, self.user_3_admin),
        )
        response = getattr(self._client(None), method)(path, body)
        assert response.data["slug"] == "series"

    def test_category_create(self):
        """
        POST /categories
        """
        path, method, body = (
            "/api/v1/categories/",
            "post",
            {"name": "Book", "slug": "book"},
        )
        self._assert_allowed_for(path, method, None, [self.user_3_admin])
        self._assert_not_allowed_for(
            path, method, None, [None, self.user_1_plain, self.user_2_moderator]
        )
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert response.data["slug"] == "book"
        assert Category.objects.filter(slug="book").exists()

    def test_category_update(self):
        """
        PUT /categories/{category_slug}
        """
        path, method, body = (
            "/api/v1/categories/series/",
            "put",
            {"name": "Seriess", "slug": "seriess"},
        )
        self._assert_allowed_for(path, method, None, [self.user_3_admin])
        self._assert_not_allowed_for(
            path, method, None, [None, self.user_1_plain, self.user_2_moderator]
        )
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert response.data["slug"] == "seriess"
        assert not Category.objects.filter(slug="series").exists()
        assert Category.objects.filter(slug="seriess").exists()

    def test_category_partial_update(self):
        """
        PATCH /categories/{category_slug}
        """
        path, method, body = (
            "/api/v1/categories/series/",
            "patch",
            {"slug": "seriess"},
        )
        self._assert_allowed_for(path, method, None, [self.user_3_admin])
        self._assert_not_allowed_for(
            path, method, None, [None, self.user_1_plain, self.user_2_moderator]
        )
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert response.data["slug"] == "seriess"
        assert not Category.objects.filter(slug="series").exists()
        assert Category.objects.filter(slug="seriess").exists()

    def test_category_delete(self):
        """
        DELETE /categories/{category_slug}
        """
        path, method, body = ("/api/v1/categories/series/", "delete", None)
        self._assert_not_allowed_for(
            path, method, None, [None, self.user_1_plain, self.user_2_moderator]
        )
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert not Category.objects.filter(slug="series").exists()
