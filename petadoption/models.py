from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os

class MyUser(AbstractUser):
    username = models.CharField(primary_key=True, max_length=128)
    email = models.EmailField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    address = models.TextField(max_length=1024)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Pet(models.Model):
    dog = 'D'
    cat = 'C'
    pet_choices = [
        (dog, 'Dog'),
        (cat, 'Cat'),
    ]
    yes = 'Y'
    no = 'N'
    adoption_choices = [
        (yes, 'Yes'),
        (no, 'No'),
    ]
    male = 'M'
    female = 'F'
    other = 'O'
    gender_choices = [
        (male, 'Male'),
        (female, 'Female'),
        (other, 'Other'),
    ]
    pet_name = models.CharField(max_length=128, null=False, blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    animal_type = models.CharField(max_length=1, choices=pet_choices)
    up_for_adoption = models.CharField(max_length=1, choices=adoption_choices, default='N')
    pet_profile_image = models.ImageField(upload_to = os.path.join(settings.MEDIA_ROOT,'pet_profile_image'))
    description = models.TextField(max_length=1024)
    created = models.DateField(auto_now_add=True)
    breed = models.CharField(max_length=128)
    gender = models.CharField(max_length=1, choices=gender_choices)
    age = models.IntegerField()

    def __str__(self):
        return self.pet_name


class Pet_Photos(models.Model):
    pet= models.ForeignKey('Pet', on_delete=models.CASCADE)
    pet_image = models.ImageField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(max_length=256)

    def __str__(self):
        return self.id


class Comments(models.Model):
    pet_id = models.ForeignKey('Pet', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    comment_writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024, null=False, blank=False)

    def __str__(self):
        return self.comment


class Adoption_requests(models.Model):
    request_no = models.AutoField(max_length=128, primary_key=True)
    phone_no = models.CharField(max_length=10, null=False, blank=False)
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description_message = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.request_no
