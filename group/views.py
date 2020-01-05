# from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from user.views import check_user_id, get_user_data
from .serializers import *
from Utils.server_utils import *
from group.models import *


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


class GroupReopen(generics.CreateAPIView):
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
        if group.admin.id != data["user_id"]:
            return Response(make_output(26, "you are not admin of this group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        member = GroupMember.objects.filter(group=group, user=data["member_id"])
        if len(member) == 0:
            return Response(make_output(27, "this id not in group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        member = member[0]
        if data["delete"] and member.delete:
            return Response(make_output(28, "this member was deleted"), status=status.HTTP_406_NOT_ACCEPTABLE)
        if not data["delete"] and not member.delete:
            return Response(make_output(29, "this member was in group"), status=status.HTTP_406_NOT_ACCEPTABLE)
        member.delete = data["delete"]
        member.save()
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
                    "id": transaction.id
                })
        return Response(output, status=status.HTTP_200_OK)


class GroupDeleteTransaction(generics.CreateAPIView):
    serializer_class = GroupSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
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
        transaction = group.transactions.get(id=data["transaction_id"])
        if transaction.delete:
            return Response(make_output(29, "transaction was deleted"), status=status.HTTP_406_NOT_ACCEPTABLE)
        # print(transaction)
        t_member = GroupMember.objects.get(group=group, user=transaction.user)
        # print(t_member)
        # print(t_member.remain, transaction.cost, transaction.delete)
        t_member.remain -= transaction.cost
        # print(t_member.remain, transaction.cost, transaction.delete)
        t_member.save()
        # print(t_member.remain)
        # print(transaction.members.count())
        for i in range(transaction.members.count()):
            t_member = GroupMember.objects.get(group=group, user=transaction.members.all()[i].user)
            # print(t_member)
            # print(t_member.remain, transaction.members.all()[i].contribution)
            t_member.remain += transaction.members.all()[i].contribution
            # print(t_member.remain, transaction.members.all()[i].contribution)
            t_member.save()
            # print(t_member.remain)
        transaction.delete = True
        transaction.save()
        return Response(make_output(), status=status.HTTP_200_OK)


class GroupAddTransaction(generics.CreateAPIView):
    serializer_class = GroupSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        # print(data)
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
        # print("A")
        n1 = User.objects.get(id=data["user_id"])
        group = Group.objects.get(id=data['group_id'])
        # group.transactions.clear()
        # for i in range(len(group.members.all())):
        #     group.members.all()[i].remain = 0
        #     group.members.all()[i].save()
        t1 = group.transactions.create(cost=data["cost"], user=n1)
        m = GroupMember.objects.get(user=n1, group=group)
        m.remain += data["cost"]
        # print(m.user.name, data["cost"])
        m.save()
        for member in data["member_list"]:
            m = GroupMember.objects.get(user_id=int(member), group=group)
            t1.members.create(user=m.user, contribution=int(data["cost"] / len(data["member_list"])))
            if member == data["member_list"][-1]:
                # print(m.user.name,
                #       data["cost"] - (int(data["cost"] / len(data["member_list"])) * (len(data["member_list"]) - 1)),
                #       m.remain)
                m.remain -= data["cost"] - (
                        int(data["cost"] / len(data["member_list"])) * (len(data["member_list"]) - 1))
                # print(m.user.name,
                #       data["cost"] - (int(data["cost"] / len(data["member_list"])) * (len(data["member_list"]) - 1)),
                #       m.remain)
                m.save()
                continue
            # print(m.user.name, int(data["cost"] / len(data["member_list"])), m.remain)

            m.remain -= int(data["cost"] / len(data["member_list"]))
            # print(m.user.name, int(data["cost"] / len(data["member_list"])), m.remain)

            m.save()
        t1.save()

        return Response(make_output(), status=status.HTTP_200_OK)
