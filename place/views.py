from django.shortcuts import render

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from user.views import check_user_id, get_user_data
from .serializers import *
from Utils.server_utils import *
from group.models import *


class PlaceAdd(generics.CreateAPIView):
    serializer_class = PlaceSerializerEmpty

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
