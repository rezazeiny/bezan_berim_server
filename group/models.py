from django.db import models
from user.models import User


class GroupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    remain = models.BigIntegerField(default=0, blank=False)
    register_date = models.DateTimeField(auto_now_add=True)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.id) + " " + str(self.delete)


class TransactionMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contribution = models.BigIntegerField(default=0, blank=False)

    def __str__(self):
        return self.user.id


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cost = models.BigIntegerField(default=0, blank=False)
    members = models.ManyToManyField(TransactionMember, blank=False)
    register_date = models.DateTimeField(auto_now_add=True)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return self.user.id


class Group(models.Model):
    # id = models.BigIntegerField(primary_key=True, blank=False, unique=True)
    chat_id = models.BigIntegerField(default=0, blank=False)
    chat_block = models.BooleanField(default=False)
    message_id = models.BigIntegerField(default=0, blank=False)
    # invite = models.BooleanField(default=False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    # score = models.IntegerField(blank=False, default=0)
    members = models.ManyToManyField(GroupMember, blank=False)
    transactions = models.ManyToManyField(Transaction, blank=True)
    name = models.CharField(max_length=125, blank=False, default="")
    register_date = models.DateTimeField(auto_now_add=True)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + " " + self.name
