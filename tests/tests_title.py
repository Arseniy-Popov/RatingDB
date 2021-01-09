import pytest

from ratings.models import Title

from .conftest import TestsBase


@pytest.mark.django_db
class TestsTitle(TestsBase):
    def test_title_list(self):
        """
        GET /titles
        """
        path, method, body = "/api/v1/titles/", "get", None
        self._assert_allowed_for(
            path,
            method,
            body,
            [None, self.user_1_plain, self.user_2_moderator, self.user_3_admin],
        )
        response = getattr(self._client(None), method)(path, body)
        assert response.data["count"] == 2
        assert response.data["results"][1]["name"] == "The Good Place"

    def test_title_list_with_search(self):
        """
        GET /titles/?{parameter}={value}
        """
        for parameter, value in (
            ("year", 1977),
            # ("genres", "sci-fi"),
            ("category", "movie"),
            ("name", "Star Wars IV"),
        ):
            path, method, body = f"/api/v1/titles/?{parameter}={value}", "get", None
            response = getattr(self._client(None), method)(path, body)
            assert response.data["count"] == 1, (parameter, value)
            assert response.data["results"][0]["name"] == "Star Wars IV"

    def test_title_retrive(self):
        """
        GET /titles/{title_id}
        """
        id = Title.objects.get(name="Star Wars IV").id
        path, method, body = f"/api/v1/titles/{id}/", "get", None
        self._assert_allowed_for(
            path,
            method,
            body,
            (None, self.user_1_plain, self.user_2_moderator, self.user_3_admin),
        )
        response = getattr(self._client(None), method)(path, body)
        assert response.data["name"] == "Star Wars IV"

    def test_title_create(self):
        """
        POST /titles
        """
        path, method, body = (
            "/api/v1/titles/",
            "post",
            {"name": "Star Wars III", "year": 2005, "category": "movie"},
        )
        self._assert_allowed_for(
            path, method, None, [self.user_2_moderator, self.user_3_admin]
        )
        self._assert_not_allowed_for(path, method, None, [None, self.user_1_plain])
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert response.data["name"] == "Star Wars III"
        assert Title.objects.filter(name="Star Wars III").exists()

    def test_title_update(self):
        """
        PUT /titles/{title_id}
        """
        id = Title.objects.get(name="Star Wars IV").id
        path, method, body = (
            f"/api/v1/titles/{id}/",
            "put",
            {"name": "Star Wars III", "year": 2006, "category": "movie"},
        )
        self._assert_allowed_for(
            path, method, None, [self.user_2_moderator, self.user_3_admin]
        )
        self._assert_not_allowed_for(path, method, None, [None, self.user_1_plain])
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert response.data["year"] == 2006
        assert not Title.objects.filter(name="Star Wars III", year=2005).exists()
        assert Title.objects.filter(name="Star Wars III", year=2006).exists()

    def test_title_partial_update(self):
        """
        PATCH /titles/{title_id}
        """
        id = Title.objects.get(name="Star Wars IV").id
        path, method, body = (f"/api/v1/titles/{id}/", "patch", {"year": 2006})
        self._assert_allowed_for(
            path, method, None, [self.user_2_moderator, self.user_3_admin]
        )
        self._assert_not_allowed_for(path, method, None, [None, self.user_1_plain])
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert response.data["year"] == 2006
        assert not Title.objects.filter(name="Star Wars IV", year=2005).exists()
        assert Title.objects.filter(name="Star Wars IV", year=2006).exists()

    def test_title_delete(self):
        """
        DELETE /titles/{title_id}
        """
        id = Title.objects.get(name="Star Wars IV").id
        path, method, body = (f"/api/v1/titles/{id}/", "delete", None)
        self._assert_not_allowed_for(path, method, None, [None, self.user_1_plain])
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert not Title.objects.filter(name="Star Wars IV").exists()
