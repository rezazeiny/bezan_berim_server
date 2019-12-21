from django.db import models


class User(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=False, unique=True)
    # score = models.IntegerField(blank=False, default=0)
    name = models.CharField(max_length=125, blank=True, default="")
    # email = models.EmailField(max_length=125, blank=True, default="", unique=False)
    # email_random = models.CharField(max_length=6, blank=True, default="")
    # email_validation = models.BooleanField(blank=False, default=False)
    phone_number = models.CharField(max_length=20, blank=True, default="")
    phone_validation = models.CharField(max_length=20, blank=True, default="")
    phone_random = models.CharField(max_length=6, blank=True, default="")
    register_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
