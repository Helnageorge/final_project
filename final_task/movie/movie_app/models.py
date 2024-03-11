from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name




class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    genres = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='poster')
    description = models.TextField(max_length=100)
    release_date = models.IntegerField()
    lead_actor = models.TextField(max_length=100)
    lead_actress = models.TextField(max_length=100)
    trailer_link = models.URLField(max_length=200)
    RELEASE_STATUSES = (
        ('latest', 'Latest'),
        ('upcoming', 'Upcoming'),
    )
    release_status = models.CharField(max_length=20, choices=RELEASE_STATUSES)

    def __str__(self):
        return self.title

class ReviewRating(models.Model):

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.movie.title} - {self.user.username}"



