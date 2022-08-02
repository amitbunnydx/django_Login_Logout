from django.db import models
from django.contrib.auth import models
from django.contrib.auth.models import *


# Create your models here.
class UserProfileInfo(models.Model):

    user=models.OneToOneField(User,on_delete=models.PROTECT)
    #additional classes
    portfolio_site=models.URLField(blank=True)

    profile_pic=models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username           #username is dfoult atrible from main user



