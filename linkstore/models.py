from django.db import models
from django.utils import timezone
from django.conf import settings
import allauth
#from django.conf import settings #to import custom user model
# Create your models here.
class Link(models.Model):
    #owner = models.ForeignKey(allauth.account.EmailAddress, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default='example User')
    link = models.CharField(max_length=500)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    favorite = models.BooleanField(default=False)
    access_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.category = self.category.lower()
        return super(Link, self).save(*args, **kwargs)

    def add_link(self):
        pass

    def delete_link(self):
        pass

    def __str__(self):
        return self.title

