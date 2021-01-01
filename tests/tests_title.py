import pytest

from .conftest import TestsBase

from ratings.models import Title


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
        GET /titles/?year={year}&genre={genre}&category={category}&name={name}
        """
        query = "year=
        path, method, body = "/api/v1/categories/?search=sci-fi", "get", None
        response = getattr(self._client(None), method)(path, body)
        assert response.data["count"] == 1
        assert response.data["results"][0]["slug"] == "sci-fi"

    # def test_title_retrive(self):
    #     """
    #     GET /titles/{title_slug}
    #     """
    #     path, method, body = "/api/v1/titles/sci-fi/", "get", None
    #     self._assert_allowed_for(
    #         path,
    #         method,
    #         body,
    #         (None, self.user_1_plain, self.user_2_moderator, self.user_3_admin),
    #     )
    #     response = getattr(self._client(None), method)(path, body)
    #     assert response.data["slug"] == "sci-fi"

    # def test_title_create(self):
    #     """
    #     POST /titles
    #     """
    #     path, method, body = (
    #         "/api/v1/titles/",
    #         "post",
    #         {"name": "Acion", "slug": "action"},
    #     )
    #     self._assert_allowed_for(
    #         path, method, None, [self.user_2_moderator, self.user_3_admin]
    #     )
    #     self._assert_not_allowed_for(path, method, None, [None, self.user_1_plain])
    #     response = getattr(self._client(self.user_3_admin), method)(path, body)
    #     assert response.data["slug"] == "action"
    #     assert Title.objects.filter(slug="action").exists()

    # def test_title_update(self):
    #     """
    #     PUT /titles/{title_slug}
    #     """
    #     path, method, body = (
    #         "/api/v1/titles/sci-fi/",
    #         "put",
    #         {"name": "Sci-fii", "slug": "sci-fii"},
    #     )
    #     self._assert_allowed_for(
    #         path, method, None, [self.user_2_moderator, self.user_3_admin]
    #     )
    #     self._assert_not_allowed_for(path, method, None, [None, self.user_1_plain])
    #     response = getattr(self._client(self.user_3_admin), method)(path, body)
    #     assert response.data["slug"] == "sci-fii"
    #     assert not Title.objects.filter(slug="sci-fi").exists()
    #     assert Title.objects.filter(slug="sci-fii").exists()

    # def test_title_partial_update(self):
    #     """
    #     PATCH /titles/{title_slug}
    #     """
    #     path, method, body = ("/api/v1/titles/sci-fi/", "patch", {"slug": "sci-fii"})
    #     self._assert_allowed_for(
    #         path, method, None, [self.user_2_moderator, self.user_3_admin]
    #     )
    #     self._assert_not_allowed_for(path, method, None, [None, self.user_1_plain])
    #     response = getattr(self._client(self.user_3_admin), method)(path, body)
    #     assert response.data["slug"] == "sci-fii"
    #     assert not Title.objects.filter(slug="sci-fi").exists()
    #     assert Title.objects.filter(slug="sci-fii").exists()
