from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """
    E.g. movie, series, play, book, etc.
    """

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    E.g. action, comedy, drama, horror, etc.
    """

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    E.g. Star Wars IV.
    """

    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.CharField(max_length=1000, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="titles"
    )
    genre = models.ManyToManyField(Genre, related_name="titles")

    def __str__(self):
        return f"{self.name}, {self.year}"


class Review(models.Model):
    """
    Review for a Title with a numerical score of 1 to 10.
    """

    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField(max_length=10000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    score = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """
    Comment left on a Review.
    """

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(auto_now_add=True)
