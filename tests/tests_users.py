import pytest

from ratings.models import User

from .conftest import URL_BASE, TestsBase


@pytest.mark.django_db
class TestsUser(TestsBase):
    def test_user_list(self):
        """
        GET /users/
        """
        path, method, body = "/api/v1/users/", "get", None
        self._assert_allowed_for(path, method, None, [self.user_3_admin])
        self._assert_not_allowed_for(
            path, method, None, [None, self.user_1_plain, self.user_2_moderator]
        )
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert response.data["count"] == 4
        assert response.data["results"][1]["username"] == self.user_2_moderator.username

    def test_user_list_with_search(self):
        """
        GET /users/?search={username}
        """
        path, method, body = (
            f"/api/v1/users/?search={self.user_4_plain.username}",
            "get",
            None,
        )
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert response.data["count"] == 1
        assert response.data["results"][0]["username"] == self.user_4_plain.username

    def test_user_retrieve(self):
        """
        GET users/{username}/
        """
        path, method, body = f"/api/v1/users/{self.user_4_plain.username}/", "get", None
        self._assert_allowed_for(path, method, None, [self.user_3_admin])
        self._assert_not_allowed_for(
            path, method, None, [None, self.user_1_plain, self.user_2_moderator]
        )
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert response.data["username"] == self.user_4_plain.username

    def test_user_partial_update(self):
        """
        PATCH users/{username}/
        """
        path, method, body = (
            f"/api/v1/users/{self.user_4_plain.username}/",
            "patch",
            {"is_moderator": True},
        )
        self._assert_allowed_for(path, method, None, [self.user_3_admin])
        self._assert_not_allowed_for(
            path, method, None, [None, self.user_1_plain, self.user_2_moderator]
        )
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert response.data["is_moderator"] is True
        assert User.objects.get(username=self.user_4_plain.username).is_moderator

    def test_user_delete(self):
        """
        DELETE users/{username}/
        """
        path, method, body = (
            f"/api/v1/users/{self.user_4_plain.username}/",
            "delete",
            None,
        )
        self._assert_not_allowed_for(
            path, method, None, [None, self.user_1_plain, self.user_2_moderator]
        )
        response = getattr(self._client(self.user_3_admin), method)(path, body)
        assert not User.objects.filter(username=self.user_4_plain.username).exists()
