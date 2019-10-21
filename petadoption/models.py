from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os

class MyUser(AbstractUser):
    username = models.CharField(primary_key=True, max_length=128)
    email = models.EmailField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    address = models.TextField(max_length=1024, default="address")
    password = models.CharField(max_length=128)

    def __str__(self):
    #    return self.fname + " " + self.lname
        return self.username
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
    pet_name = models.CharField(max_length=128, null=False, blank=False)
    male = 'M'
    female = 'F'
    other = 'O'
    gender_choices = [
        (male, 'Male'),
        (female, 'Female'),
        (other, 'Other'),
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    animal_type = models.CharField(max_length=1, choices=pet_choices)
    gender = models.CharField(max_length=1, choices=gender_choices, default='M')
    age = models.IntegerField(default="0")
    breed = models.CharField(max_length=128, default="breed")
    up_for_adoption = models.CharField(max_length=1, choices=adoption_choices, default='N')
    pet_profile_image = models.ImageField(upload_to = os.path.join(settings.MEDIA_ROOT,'pet_profile_image'))
    description = models.TextField(max_length=1024)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.pet_name


class Pet_Photos(models.Model):
    photo_id = models.ForeignKey('Pet', on_delete=models.CASCADE)
    photo_no = models.CharField(max_length=128, primary_key=True)
    pet_image = models.ImageField(null=False)

    def __str__(self):
        return self.photo_id


class Comments(models.Model):
    pet_id = models.ForeignKey('Pet', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    comment_writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024, null=False, blank=False)

    def __str__(self):
        return self.comment


class Adoption_requests(models.Model):
    request_no = models.AutoField(max_length=128, primary_key=True)
    phone_no = models.CharField(max_length=10, null=False, blank=False, default="Phone Number")
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description_message = models.TextField(max_length=500)

    def __str__(self):
        return self.request_no
