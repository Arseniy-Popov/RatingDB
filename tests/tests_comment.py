import pytest

from ratings.models import Comment, Review, Title

from .conftest import URL_BASE, TestsBase


@pytest.mark.django_db
class TestsComment(TestsBase):
    def test_comment_list(self):
        """
        GET titles/{title_id}/reviews/{review_id}/comments/
        """
        path, method, body = (
            f"{URL_BASE}/titles/"
            f"{self.title_1.id}/reviews/{self.review_2.id}/comments/",
            "get",
            None,
        )
        self._assert_allowed_for(
            path,
            method,
            body,
            [None, self.user_1_plain, self.user_2_moderator, self.user_3_admin],
        )
        response = getattr(self._client(None), method)(path, body)
        assert response.data["count"] == 2
        assert response.data["results"][1]["text"] == self.comment_2.text

    def test_comment_retrive(self):
        """
        GET titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
        """
        path, method, body = (
            f"{URL_BASE}/titles/"
            f"{self.title_1.id}/reviews/{self.review_2.id}/comments/{self.comment_2.id}/",
            "get",
            None,
        )
        self._assert_allowed_for(
            path,
            method,
            body,
            (None, self.user_1_plain, self.user_2_moderator, self.user_3_admin),
        )
        response = getattr(self._client(None), method)(path, body)
        assert response.data["text"] == self.comment_2.text

    def test_comment_create(self):
        """
        POST titles/{title_id}/reviews/{review_id}/comments/
        """
        path, method, body = (
            f"{URL_BASE}/titles/"
            f"{self.title_1.id}/reviews/{self.review_2.id}/comments/",
            "post",
            {"text": (new_text := "Agree.")},
        )
        self._assert_allowed_for(
            path,
            method,
            None,
            [self.user_1_plain, self.user_2_moderator, self.user_3_admin],
        )
        self._assert_not_allowed_for(path, method, None, [None])
        response = getattr(self._client(self.user_1_plain), method)(path, body)
        assert response.data["text"] == new_text
        assert Comment.objects.filter(review=self.review_2, text=new_text).exists()

    def test_comment_update(self):
        """
        PUT /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
        """
        path, method, body = (
            f"{URL_BASE}/titles/"
            f"{self.title_1.id}/reviews/{self.review_2.id}/comments/{self.comment_2.id}/",
            "put",
            {"text": (new_text := "Maybe true.")},
        )
        self._assert_allowed_for(path, method, None, [self.user_1_plain])
        self._assert_not_allowed_for(
            path,
            method,
            None,
            [None, self.user_2_moderator, self.user_3_admin, self.user_4_plain],
        )
        response = getattr(self._client(self.user_1_plain), method)(path, body)
        assert response.data["text"] == new_text
        assert not Comment.objects.filter(text=self.comment_2.text).exists()
        assert Comment.objects.filter(text=new_text).exists()

    def test_comment_partial_update(self):
        """
        PATCH /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
        """
        path, method, body = (
            f"{URL_BASE}/titles/"
            f"{self.title_1.id}/reviews/{self.review_2.id}/comments/{self.comment_2.id}/",
            "patch",
            {"text": (new_text := "Maybe true.")},
        )
        self._assert_allowed_for(path, method, None, [self.user_1_plain])
        self._assert_not_allowed_for(
            path,
            method,
            None,
            [None, self.user_2_moderator, self.user_3_admin, self.user_4_plain],
        )
        response = getattr(self._client(self.user_1_plain), method)(path, body)
        assert response.data["text"] == new_text
        assert not Comment.objects.filter(text=self.comment_2.text).exists()
        assert Comment.objects.filter(text=new_text).exists()

    def test_comment_delete(self):
        """
        DELETE /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
        """
        path, method, body = (
            f"{URL_BASE}/titles/"
            f"{self.title_1.id}/reviews/{self.review_2.id}/comments/{self.comment_2.id}/",
            "delete",
            None,
        )
        self._assert_not_allowed_for(path, method, None, [None, self.user_4_plain])
        response = getattr(self._client(self.user_1_plain), method)(path, body)
        assert not Comment.objects.filter(text=self.comment_2.text).exists()
