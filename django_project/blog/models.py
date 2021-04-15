from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.

# each class is a table in the DB
class Post(models.Model):
    # each attribute is a field in the DB
    business_name = models.CharField(max_length = 100)
    country = models.CharField(max_length=100)
    state_or_province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    additional_address_info = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(max_length=2000)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_email = models.EmailField(null=True, blank=True)
    tags = TaggableManager()

    def __str__(self):
        return self.business_name
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})