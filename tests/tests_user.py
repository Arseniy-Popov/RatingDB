import pytest

from ratings.models import User

from .conftest import URL_BASE, TestsBase


@pytest.mark.django_db
class TestsUser(TestsBase):
    url = f"{URL_BASE}/user/"
    
    def test_user_retrieve(self):
        """
        GET user/
        """
        response = self._client(self.user_1_plain).get(self.url)
        assert response.data["username"] == self.user_1_plain.username
        assert response.data["roles"] == []
        response = self._client(self.user_3_admin).get(self.url)
        assert response.data["username"] == self.user_3_admin.username
        assert response.data["roles"] == ["IsAdmin"]
    
    def test_user_create(self):
        """
        POST user/
        """
        body = {
            "username": (new_username:="new_username"),
            "password": "newpswd"
        }
        response = self._client(None).post(self.url, body)
        assert response.data["username"] == new_username
        assert "password" not in response.data
        assert User.objects.filter(username=new_username).exists()
