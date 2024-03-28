from django.db import models
from . choices import *
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='profile')
    preference = models.TextField(null=True, blank=True)
    blacklist = models.TextField(null=True, blank=True)
    avatar = models.FileField(upload_to='avatar/', default='avatar/default-avatar.png')
    account_created = models.DateField(null=True, blank=True)

class Series(models.Model):
    title = models.CharField(max_length=60)
    author = models.CharField(max_length=40)
    status = models.CharField(
        max_length=20, 
        null=False,
        choices=SERIES_STATUS
    )
    pub_jp = models.CharField(max_length=20, null=True, blank=True)
    pub_en = models.CharField(max_length=20, null=True, blank=True)
    genre = models.CharField(max_length=110, null=True)
    desc = models.TextField(max_length=300, default='-')

class Volume(models.Model):
    uniq = models.CharField(max_length=20, primary_key=True)
    title = models.ForeignKey('Series', on_delete=models.CASCADE, blank=True, null=True)
    volume = models.IntegerField()
    synopsis = models.TextField(max_length=100)
    status = models.BooleanField(default=False)

class Note(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    volume = models.ForeignKey('Volume', on_delete=models.CASCADE)
    note = models.TextField(max_length=100)

class Review(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    series = models.ForeignKey('Series', on_delete=models.CASCADE)
    review = models.TextField(max_length=300)
    score = models.DecimalField(max_digits=2, decimal_places=1)