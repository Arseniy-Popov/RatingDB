import pytest

from ratings.models import User

from .conftest import URL_BASE, TestsBase


@pytest.mark.django_db
class TestsUser(TestsBase):
    def test_user_retrieve(self):
        """
        GET user/{username}/
        """
        url = f"{URL_BASE}/user/{self.user_4_plain.username}/"
        response = self._client(self.user_3_admin).get(url)
        assert response.data["username"] == self.user_4_plain.username

    def test_user_partial_update(self):
        """
        PATCH user/{username}/
        """
        url = f"{URL_BASE}/user/{self.user_4_plain.username}/"
        body = {"is_moderator": True}
        response = self._client(self.user_3_admin).patch(url, body)
        assert response.data["is_moderator"] is True
        assert User.objects.get(username=self.user_4_plain.username).is_moderator
