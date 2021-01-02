import pytest

from .conftest import TestsBase

from ratings.models import Title, Comment, Review


@pytest.mark.django_db
class TestsComment(TestsBase):
    def test_comment_list(self):
        """
        GET titles/{title_id}/reviews/{review_id}/comments/
        """
        title_id, review_id = (
            Title.objects.get(name="Star Wars IV").id,
            Review.objects.get(text="Okay.").id,
        )
        path, method, body = (
            f"/api/v1/titles/{title_id}/reviews/{review_id}/comments/",
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
        assert response.data["results"][1]["text"] == "Not true."

    def test_comment_retrive(self):
        """
        GET titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
        """
        title_id, review_id, comment_id = (
            Title.objects.get(name="Star Wars IV").id,
            Review.objects.get(text="Okay.").id,
            Comment.objects.get(text="Not true.").id,
        )
        path, method, body = (
            f"/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/",
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
        assert response.data["text"] == "Not true."

    def test_comment_create(self):
        """
        POST titles/{title_id}/reviews/{review_id}/comments/
        """
        review = Review.objects.get(text="Okay.")
        title_id, review_id = (Title.objects.get(name="Star Wars IV").id, review.id)
        path, method, body = (
            f"/api/v1/titles/{title_id}/reviews/{review_id}/comments/",
            "post",
            {"text": "Agree."},
        )
        self._assert_allowed_for(
            path,
            method,
            None,
            [self.user_1_plain, self.user_2_moderator, self.user_3_admin],
        )
        self._assert_not_allowed_for(path, method, None, [None])
        response = getattr(self._client(self.user_1_plain), method)(path, body)
        assert response.data["text"] == "Agree."
        assert Comment.objects.filter(review=review, text="Agree.").exists()

    def test_comment_update(self):
        """
        PUT /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
        """
        title_id, review_id, comment_id = (
            Title.objects.get(name="Star Wars IV").id,
            Review.objects.get(text="Okay.").id,
            Comment.objects.get(text="Not true.").id,
        )
        path, method, body = (
            f"/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/",
            "put",
            {"text": "Maybe true."},
        )
        self._assert_allowed_for(path, method, None, [self.user_1_plain])
        self._assert_not_allowed_for(
            path,
            method,
            None,
            [None, self.user_2_moderator, self.user_3_admin, self.user_4_plain],
        )
        response = getattr(self._client(self.user_1_plain), method)(path, body)
        assert response.data["text"] == "Maybe true."
        assert not Comment.objects.filter(text="Not true.").exists()
        assert Comment.objects.filter(text="Maybe true.").exists()

    def test_comment_partial_update(self):
        """
        PATCH /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
        """
        title_id, review_id, comment_id = (
            Title.objects.get(name="Star Wars IV").id,
            Review.objects.get(text="Okay.").id,
            Comment.objects.get(text="Not true.").id,
        )
        path, method, body = (
            f"/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/",
            "patch",
            {"text": "Maybe true."},
        )
        self._assert_allowed_for(path, method, None, [self.user_1_plain])
        self._assert_not_allowed_for(
            path,
            method,
            None,
            [None, self.user_2_moderator, self.user_3_admin, self.user_4_plain],
        )
        response = getattr(self._client(self.user_1_plain), method)(path, body)
        assert response.data["text"] == "Maybe true."
        assert not Comment.objects.filter(text="Not true.").exists()
        assert Comment.objects.filter(text="Maybe true.").exists()

    def test_comment_partial_update(self):
        """
        DELETE /titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
        """
        title_id, review_id, comment_id = (
            Title.objects.get(name="Star Wars IV").id,
            Review.objects.get(text="Okay.").id,
            Comment.objects.get(text="Not true.").id,
        )
        path, method, body = (
            f"/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/",
            "delete",
            None,
        )
        self._assert_not_allowed_for(path, method, None, [None, self.user_4_plain])
        response = getattr(self._client(self.user_1_plain), method)(path, body)
        assert not Comment.objects.filter(text="Not true.").exists()
