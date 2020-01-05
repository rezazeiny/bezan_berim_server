import sys

from django.db import models

from user.models import User

from group.models import Group


class PlaceUserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    message = models.CharField(max_length=1000, blank=False)
    register_data = models.DateTimeField(auto_now_add=True)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.id) + ": " + self.message


class PlaceGroupFeedback(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=False)
    message = models.CharField(max_length=1000, blank=False)
    register_data = models.DateTimeField(auto_now_add=True)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.group.id) + ": " + self.message


class PlaceTrips(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=False)
    member_len = models.IntegerField(default=0)
    member_cost = models.BigIntegerField(default=0)
    register_data = models.DateTimeField(auto_now_add=True)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.group.id) + ": " + str(self.member_len) + ", " + str(self.member_cost)


class Place(models.Model):
    name = models.CharField(max_length=125, blank=False, default="")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    user_feedback = models.ManyToManyField(PlaceUserFeedback, blank=True)
    group_feedback = models.ManyToManyField(PlaceGroupFeedback, blank=True)
    trips = models.ManyToManyField(PlaceTrips, blank=True)
    average_cost = models.BigIntegerField(default=0)
    x_location = models.FloatField(default=0)
    Y_location = models.FloatField(default=0)
    register_data = models.DateTimeField(auto_now_add=True)
    delete = models.BooleanField(default=False)
    message_id = models.BigIntegerField(default=0, blank=False)

    def __str__(self):
        return self.id
