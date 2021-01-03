import pytest

from ratings.models import Review, Title

from .conftest import TestsBase


@pytest.mark.django_db
class TestsReview(TestsBase):
    def test_review_list(self):
        """
        GET titles/{title_id}/reviews
        """
        id_title = Title.objects.get(name="Star Wars IV").id
        path, method, body = f"/api/v1/titles/{id_title}/reviews/", "get", None
        self._assert_allowed_for(
            path,
            method,
            body,
            [None, self.user_1_plain, self.user_2_moderator, self.user_3_admin],
        )
        response = getattr(self._client(None), method)(path, body)
        assert response.data["count"] == 2
        assert response.data["results"][1]["text"] == "Okay."

    def test_review_retrive(self):
        """
        GET titles/{title_id}/reviews/{review_id}
        """
        id_title, id_review = (
            Title.objects.get(name="Star Wars IV").id,
            Review.objects.get(text="Okay.").id,
        )
        path, method, body = (
            f"/api/v1/titles/{id_title}/reviews/{id_review}/",
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
        assert response.data["text"] == "Okay."

    def test_review_create(self):
        """
        POST /titles/{title_id}/reviews
        """
        id_title = Title.objects.get(name="The Good Place").id
        path, method, body = (
            f"/api/v1/titles/{id_title}/reviews/",
            "post",
            {"text": "Best!", "score": 10},
        )
        self._assert_allowed_for(
            path,
            method,
            None,
            [self.user_1_plain, self.user_2_moderator, self.user_3_admin],
        )
        self._assert_not_allowed_for(path, method, None, [None])
        response = getattr(self._client(self.user_1_plain), method)(path, body)
        assert response.data["text"] == "Best!"
        assert Review.objects.filter(text="Best!").exists()

    def test_review_update(self):
        """
        PUT /titles/{title_id}/reviews/{review_id}
        """
        id_title, id_review = (
            Title.objects.get(name="Star Wars IV").id,
            Review.objects.get(text="Okay.").id,
        )
        path, method, body = (
            f"/api/v1/titles/{id_title}/reviews/{id_review}/",
            "put",
            {"text": "Reasonable.", "score": 8},
        )
        self._assert_allowed_for(path, method, None, [self.user_4_plain])
        self._assert_not_allowed_for(
            path,
            method,
            None,
            [None, self.user_1_plain, self.user_2_moderator, self.user_3_admin],
        )
        response = getattr(self._client(self.user_4_plain), method)(path, body)
        assert response.data["text"] == "Reasonable."
        assert not Review.objects.filter(text="Okay.").exists()
        assert Review.objects.filter(text="Reasonable.").exists()

    def test_review_partial_update(self):
        """
        PATCH /titles/{title_id}/reviews/{review_id}
        """
        id_title, id_review = (
            Title.objects.get(name="Star Wars IV").id,
            Review.objects.get(text="Okay.").id,
        )
        path, method, body = (
            f"/api/v1/titles/{id_title}/reviews/{id_review}/",
            "patch",
            {"text": "Reasonable."},
        )
        self._assert_allowed_for(path, method, None, [self.user_4_plain])
        self._assert_not_allowed_for(
            path,
            method,
            None,
            [None, self.user_1_plain, self.user_2_moderator, self.user_3_admin],
        )
        response = getattr(self._client(self.user_4_plain), method)(path, body)
        assert response.data["text"] == "Reasonable."
        assert not Review.objects.filter(text="Okay.").exists()
        assert Review.objects.filter(text="Reasonable.").exists()

    def test_review_delete(self):
        """
        DELETE /titles/{title_id}/reviews/{review_id}
        """
        id_title, id_review = (
            Title.objects.get(name="Star Wars IV").id,
            Review.objects.get(text="Okay.").id,
        )
        path, method, body = (
            f"/api/v1/titles/{id_title}/reviews/{id_review}/",
            "patch",
            {"text": "Reasonable."},
        )
        self._assert_not_allowed_for(path, method, None, [None, self.user_1_plain])
        response = getattr(self._client(self.user_4_plain), method)(path, body)
        assert not Review.objects.filter(text="Okay.").exists()
