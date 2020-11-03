from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """
    Movie, series, play, book, etc.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Action, comedy, drama, horror, etc.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    

class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.CharField(max_length=1000, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="titles",
    )
    genre = models.ManyToManyField(Genre, related_name="titles")

    def __str__(self):
        return f"{self.name}, {self.year}"