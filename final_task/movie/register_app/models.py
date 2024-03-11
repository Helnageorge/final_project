from django.db import models
from django.contrib.auth.models import User



class Registration(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)



    def __str__(self):
        return self.username.username