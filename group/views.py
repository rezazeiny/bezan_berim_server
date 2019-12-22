# from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from user.views import check_user_id, get_user_data
from .serializers import *
from Utils.server_utils import *
from group.models import *


def check_group_id(data, user_id=0):
    print(data, file=sys.stderr)
    # if group_id == 0:
    #     group_id = data["group_id"]
    # group = Group.objects.filter(id=group_id)
    # if len(group) == 1:
    #     return group[0]
    # else:
    return None


def check_group_id_admin(data, group_id=0, user_id=0):
    print(data, file=sys.stderr)
    if group_id == 0:
        group_id = data["group_id"]
    if user_id == 0:
        user_id = data["user_id"]
    group = Group.objects.filter(id=group_id, admin__id=user_id)
    if len(group) == 1:
        return group[0]
    else:
        return None


def check_group_id_user(data, group_id=0, user_id=0):
    print(data, file=sys.stderr)
    if group_id == 0:
        group_id = data["group_id"]
    if user_id == 0:
        user_id = data["user_id"]
    group = Group.objects.filter(id=group_id, members__user__id=user_id)
    if len(group) == 1:
        return group[0]
    else:
        return None


def get_groups_data(data, group_id=0, user_id=0):
    print(data, file=sys.stderr)
    if group_id == 0:
        group_id = data["group_id"]
    if user_id == 0:
        user_id = data["user_id"]
    output = make_output()
    groups = Group.objects.filter(members__user__id=user_id)
    output["group_list"] = []
    output["group_id"] = group_id
    output["remain"] = 0
    for group in groups:
        if group.delete:
            continue
        members = group.members.all()
        remain = 0
        for i in range(len(members)):
            member = members[i]
            if member.user.id == data["user_id"]:
                remain = member.remain
                output["remain"] += remain
                break
        output["group_list"].append({
            "name": group.name,
            "id": group.id,
            "members": len(group.members.all()),
            # "delete": group.delete,
            "admin": {"name": group.admin.name, "id": group.admin.id},
            "remain": remain
        })
    return output


def get_group_data(data, group=None, has_member=False, has_transaction=False):
    print(data, file=sys.stderr)
    output = make_output()
    if not group:
        # group = Group.objects.filter(id=data["group_id"], members__user__id=data["user_id"])
        group = Group.objects.filter(id=data["group_id"])
        if len(group) == 0:
            return make_output(20, "group not exist")
        group = group[0]
    if group.delete:
        return make_output(21, "deleted group")
    members = group.members.all()
    transactions = group.transactions.all()
    output["remain"] = 0
    for i in range(len(members)):
        member = members[i]
        if member.user.id == data["user_id"]:
            output["remain"] = member.remain
            if member.delete:
                return make_output(4, "left group")
            break
    is_admin = data["user_id"] == group.admin.id
    output["name"] = group.name
    output["id"] = group.id
    output["invite"] = group.invite
    # output["delete"] = group.delete
    output["chat_id"] = group.chat_id
    output["register_date"] = group.register_date
    output["admin"] = {"name": group.admin.name, "id": group.admin.id}
    output["member_len"] = len(members)
    output["transaction_len"] = len(transactions)

    if has_member:
        output["member_list"] = []
        for i in range(len(members)):
            member = members[i]
            if is_admin or not member.delete:
                output["member_list"].append({
                    "user": {"name": member.user.name, "id": member.user.id},
                    "remain": member.remain,
                    "delete": member.delete,
                    "register_date": member.register_date,
                })
    if has_transaction:
        output["transaction_list"] = []
        for i in range(len(transactions)):
            transaction = transactions[i]
            if is_admin or not transaction.delete:
                transaction_members = []
                all_member = transaction.members.all()
                for j in range(len(all_member)):
                    member = all_member[j]
                    transaction_members.append({
                        "user": {"name": member.user.name, "id": member.user.id},
                        "contribution": member.contribution,
                    })
                output["transaction_list"].append({
                    "user": {"name": transaction.user.name, "id": transaction.user.id},
                    "cost": transaction.cost,
                    "member_len": len(transaction_members),
                    "member": transaction_members,
                    "delete": transaction.delete,
                    "register_date": transaction.register_date,
                })
    return output


class GroupAdd(generics.CreateAPIView):
    serializer_class = GroupSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        user = check_user_id(data)
        if user is None:
            return Response(make_output(10, "Not valid user"), status=status.HTTP_406_NOT_ACCEPTABLE)
        # todo set limitation for a person add group
        if data["group_id"] == 0:
            group = Group.objects.create(name=data['name'], admin=user)
            group.members.create(user=user)
            group.save()
        else:
            group = Group.objects.filter(id=data["group_id"])
            if len(group) == 0:
                return Response(make_output(20, "group not exist"), status=status.HTTP_406_NOT_ACCEPTABLE)
            group = group[0]
            if group.delete:
                return Response(make_output(21, "deleted group"), status=status.HTTP_406_NOT_ACCEPTABLE)
            member = GroupMember.objects.filter(group=group, user=user)
            if len(member) == 0:
                return Response(make_output(22, "group and user not match"), status=status.HTTP_406_NOT_ACCEPTABLE)
            member = member[0]
            if member.delete:
                return Response(make_output(23, "left group"), status=status.HTTP_406_NOT_ACCEPTABLE)
            group.name = data["name"]
            group.save()
        output = get_user_data(user)
        output["group_id"] = group.id
        return Response(output, status=status.HTTP_200_OK)


class GroupList(generics.CreateAPIView):
    serializer_class = GroupSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        user = check_user_id(data)
        if user is None:
            return Response(make_output(10, "Not valid user"), status=status.HTTP_406_NOT_ACCEPTABLE)
        members = GroupMember.objects.filter(user=user, delete=False, group__delete=False)
        output = make_output()
        output["remain"] = 0
        output["group_list"] = []
        output["group_len"] = len(members)
        for member in members:
            group = member.group_set.all()[0]
            output["group_list"].append(
                {
                    "name": group.name,
                    "id": group.id,
                    "remain": member.remain,
                    "is_admin": group.admin.id == data["user_id"],
                }
            )
            output["remain"] += member.remain

        return Response(output, status=status.HTTP_200_OK)


class GroupCheck(generics.CreateAPIView):
    serializer_class = GroupSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        user = check_user_id(data)
        if user is None:
            return Response(make_output(10, "Not valid user"), status=status.HTTP_406_NOT_ACCEPTABLE)
        group = Group.objects.filter(id=data["group_id"])
        if len(group) == 0:
            return Response(make_output(20, "group not exist"), status=status.HTTP_406_NOT_ACCEPTABLE)
        group = group[0]
        if group.delete:
            return Response(make_output(21, "deleted group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        member = GroupMember.objects.filter(group=group, user=user)
        if len(member) == 0:
            return Response(make_output(22, "group and user not match"), status=status.HTTP_406_NOT_ACCEPTABLE)
        member = member[0]
        if member.delete:
            return Response(make_output(23, "left group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        output = make_output()
        output["remain"] = member.remain
        output["id"] = group.id
        output["name"] = group.name
        output["message_id"] = group.message_id
        output["chat_id"] = group.chat_id
        output["member_len"] = group.members.count()
        output["transaction_len"] = group.transactions.count()
        output["admin"] = {"id": group.admin.id, "name": group.admin.name}
        output["user"] = {"id": user.id, "name": user.name}
        return Response(output, status=status.HTTP_200_OK)


class GroupChangeChatID(generics.CreateAPIView):
    serializer_class = GroupSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        user = check_user_id(data)
        if user is None:
            return Response(make_output(10, "Not valid user"), status=status.HTTP_406_NOT_ACCEPTABLE)
        group = Group.objects.filter(id=data["group_id"])
        if len(group) == 0:
            return Response(make_output(20, "group not exist"), status=status.HTTP_406_NOT_ACCEPTABLE)
        group = group[0]
        if group.delete:
            return Response(make_output(21, "deleted group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        member = GroupMember.objects.filter(group=group, user=user)
        if len(member) == 0:
            return Response(make_output(22, "group and user not match"), status=status.HTTP_406_NOT_ACCEPTABLE)
        member = member[0]
        if member.delete:
            return Response(make_output(23, "left group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        group.chat_id = data["chat_id"]
        group.message_id = data["message_id"]
        group.save()
        return Response(make_output(), status=status.HTTP_200_OK)


class GroupJoin(generics.CreateAPIView):
    serializer_class = GroupSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        user = check_user_id(data)
        if user is None:
            return Response(make_output(10, "Not valid user"), status=status.HTTP_406_NOT_ACCEPTABLE)
        group = Group.objects.filter(id=data["group_id"])
        if len(group) == 0:
            return Response(make_output(20, "group not exist"), status=status.HTTP_406_NOT_ACCEPTABLE)
        group = group[0]
        if group.delete:
            return Response(make_output(21, "deleted group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        member = GroupMember.objects.filter(group=group, user=user)
        if len(member) == 1 and not member[0].delete:
            return Response(make_output(25, "you are in group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        if len(member) == 1 and member[0].delete:
            output = make_output(26, "you was in group")
            member[0].delete = False
            member[0].save()
            output["id"] = group.id
            output["name"] = group.name
            output["chat_id"] = group.chat_id
            output["user"] = {"id": user.id, "name": user.name}
            return Response(output, status=status.HTTP_406_NOT_ACCEPTABLE)
        group.members.create(user=user)
        group.save()
        output = make_output()
        output["id"] = group.id
        output["name"] = group.name
        output["user"] = {"id": user.id, "name": user.name}
        output["chat_id"] = group.chat_id
        return Response(output, status=status.HTTP_200_OK)


class GroupLeft(generics.CreateAPIView):
    serializer_class = GroupSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        user = check_user_id(data)
        if user is None:
            return Response(make_output(10, "Not valid user"), status=status.HTTP_406_NOT_ACCEPTABLE)
        group = Group.objects.filter(id=data["group_id"])
        if len(group) == 0:
            return Response(make_output(20, "group not exist"), status=status.HTTP_406_NOT_ACCEPTABLE)
        group = group[0]
        if group.delete:
            return Response(make_output(21, "deleted group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        member = GroupMember.objects.filter(group=group, user=user)
        if len(member) == 0:
            return Response(make_output(22, "group and user not match"), status=status.HTTP_406_NOT_ACCEPTABLE)
        member = member[0]
        if member.delete:
            return Response(make_output(23, "left group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        if data["user_id"] == group.admin.id:
            group.delete = True
            group.save()
        else:
            member.delete = True
            member.save()
        return Response(make_output(), status=status.HTTP_200_OK)


class GroupMembers(generics.CreateAPIView):
    serializer_class = GroupSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        user = check_user_id(data)
        if user is None:
            return Response(make_output(10, "Not valid user"), status=status.HTTP_406_NOT_ACCEPTABLE)
        group = Group.objects.filter(id=data["group_id"])
        if len(group) == 0:
            return Response(make_output(20, "group not exist"), status=status.HTTP_406_NOT_ACCEPTABLE)
        group = group[0]
        if group.delete:
            return Response(make_output(21, "deleted group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        member = GroupMember.objects.filter(group=group, user=user)
        if len(member) == 0:
            return Response(make_output(22, "group and user not match"), status=status.HTTP_406_NOT_ACCEPTABLE)
        member = member[0]
        if member.delete:
            return Response(make_output(23, "left group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        output = make_output()
        members = group.members.all()
        output["member_list"] = []
        is_admin = data["user_id"] == group.admin.id
        for i in range(len(members)):
            member = members[i]
            if is_admin or not member.delete:
                output["member_list"].append({
                    "user": {"name": member.user.name, "id": member.user.id},
                    "remain": member.remain,
                    "delete": member.delete,
                    "register_date": member.register_date,
                    "selected": False,
                })
        return Response(output, status=status.HTTP_200_OK)


class GroupTransactions(generics.CreateAPIView):
    serializer_class = GroupSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        user = check_user_id(data)
        if user is None:
            return Response(make_output(10, "Not valid user"), status=status.HTTP_406_NOT_ACCEPTABLE)
        group = Group.objects.filter(id=data["group_id"])
        if len(group) == 0:
            return Response(make_output(20, "group not exist"), status=status.HTTP_406_NOT_ACCEPTABLE)
        group = group[0]
        if group.delete:
            return Response(make_output(21, "deleted group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        member = GroupMember.objects.filter(group=group, user=user)
        if len(member) == 0:
            return Response(make_output(22, "group and user not match"), status=status.HTTP_406_NOT_ACCEPTABLE)
        member = member[0]
        if member.delete:
            return Response(make_output(23, "left group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        output = make_output()
        transactions = group.transactions.all()
        output["transaction_list"] = []
        is_admin = data["user_id"] == group.admin.id
        for i in range(len(transactions)):
            transaction = transactions[i]
            if is_admin or not transaction.delete:
                transaction_members = []
                all_member = transaction.members.all()
                for j in range(len(all_member)):
                    member = all_member[j]
                    transaction_members.append({
                        "user": {"name": member.user.name, "id": member.user.id},
                        "contribution": member.contribution,
                    })
                output["transaction_list"].append({
                    "user": {"name": transaction.user.name, "id": transaction.user.id},
                    "cost": transaction.cost,
                    "member_len": len(transaction_members),
                    "member": transaction_members,
                    "delete": transaction.delete,
                    "register_date": transaction.register_date,
                })
        return Response(output, status=status.HTTP_200_OK)
