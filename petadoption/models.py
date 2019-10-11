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

    def __str__(self):
        return self.fname + " " + self.lname
# class MyUser(AbstractUser):
#     username = models.CharField(primary_key=True, max_length=128)
#     email = models.EmailField(max_length=128, null=False, blank=False)
#     first_name = models.CharField(max_length=128, null=False, blank=False, default='fname')
#     last_name = models.CharField(max_length=128, null=False, blank=False, default='lname')
#     password = models.CharField(max_length=128, default='pass')
#     def __str__(self):
#         return self.fname + " " + self.lname


# class User(models.Model):
#     name = models.CharField(max_length=128, null=False, blank=False)
#     phone_no = models.CharField(max_length=10, null=False, blank=False)
#     email = models.EmailField(max_length=128, primary_key=True)
#     profile_image = models.ImageField(null=False)
#     password = models.CharField(max_length=20, null=False, blank=False)

#     def __str__(self):
#         return self.name


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
    #pet_id = models.CharField(max_length=128, primary_key=True)
    pet_name = models.CharField(max_length=128, null=False, blank=False, default='Pets name')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    animal_type = models.CharField(max_length=1, choices=pet_choices)
    up_for_adoption = models.CharField(max_length=1, choices=adoption_choices, default='N')
    pet_profile_image = models.ImageField(upload_to = os.path.join(settings.MEDIA_ROOT,'pet_profile_image'))
    description = models.TextField(max_length=128)

    def __str__(self):
        return self.pet_name


class Pet_Photos(models.Model):
    photo_id = models.ForeignKey('Pet', on_delete=models.CASCADE)
    photo_no = models.CharField(max_length=128, primary_key=True)
    pet_image = models.ImageField(null=False)

    def __str__(self):
        return self.photo_id


class Comments(models.Model):
    picture_id = models.ForeignKey('Pet_Photos', on_delete=models.CASCADE)
    comment_no = models.CharField(max_length=128, primary_key=True)
    comment_writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.CharField(max_length=128, null=False, blank=False, default='Comment')

    def __str__(self):
        return self.comment_no


class Adoption_requests(models.Model):
    request_no = models.CharField(max_length=128, primary_key=True)
    requester_name = models.CharField(max_length=128, null=False, blank=False, default='Your name')
    requester_phone_no = models.CharField(max_length=10, null=False, blank=False, default='Your phone no')
    requester_username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request_description = models.TextField(max_length=500)

    def __str__(self):
        return self.request_no
