import sys

from django.db import models


# class Group(models.Model):
#     name = models.CharField(max_length=125, blank=True, default="")
#     number = models.CharField(max_length=20, blank=True, default="")
#     image = models.ImageField(upload_to="group_image/", blank=True, default="default_group_image.png")
#
#     def __str__(self):
#         return self.name
#
#
# class MainAccess(models.Model):
#     name = models.CharField(max_length=125, blank=True, default="")
#
#     def __str__(self):
#         return self.name


class User(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=False, unique=True)
    score = models.IntegerField(blank=False, default=0)
    name = models.CharField(max_length=125, blank=True, default="")
    email = models.EmailField(max_length=125, blank=True, default="", unique=True)
    email_random = models.CharField(max_length=6, blank=True, default="")
    email_validation = models.BooleanField(blank=False, default=False)
    phone_number = models.CharField(max_length=20, blank=True, default="")
    phone_random = models.CharField(max_length=6, blank=True, default="")
    phone_validation = models.BooleanField(blank=False, default=False)
    register_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

# class MarketRate(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     star = models.PositiveSmallIntegerField(default=0)
#     register_data = models.DateTimeField(auto_now_add=True)
#     last_edit_data = models.DateTimeField(auto_now=True)


# class MarketComment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.CharField(max_length=5000, blank=True, default="")
#     register_data = models.DateTimeField(auto_now_add=True)
#     last_edit_data = models.DateTimeField(auto_now=True)


# class ModelRate(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     star = models.PositiveSmallIntegerField(default=0)
#     register_data = models.DateTimeField(auto_now_add=True)
#     last_edit_data = models.DateTimeField(auto_now=True)


# class ModelComment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.CharField(max_length=5000, blank=True, default="")
#     register_data = models.DateTimeField(auto_now_add=True)
#     last_edit_data = models.DateTimeField(auto_now=True)


# class RoleMarket(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=125)
#     register_data = models.DateTimeField(auto_now_add=True)
#     last_edit_data = models.DateTimeField(auto_now=True)
