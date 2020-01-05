# from django.core.files import File
# from django.core.files.base import ContentFile
# from django.core.mail import send_mail
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
# from contextlib import contextmanager
from Utils.server_utils import *
# from user.models import Group
from .serializers import *
from group.models import GroupMember


# import base64


def check_user_id(data, user_id=0):
    if user_id == 0:
        user_id = data["user_id"]
    print(data, file=sys.stderr)
    user = User.objects.filter(id=user_id)
    if len(user) == 1:
        return user[0]
    else:
        return None


def get_user_data(user):
    output = make_output()
    copy_obj_to_dic(output, user,
                    # ['id', 'name', 'email', 'email_validation', 'phone_number', 'phone_validation'])
                    ['id', 'name', 'phone_number', 'phone_validation'])
    output["remain"] = 0
    groups = GroupMember.objects.filter(user=user, delete=False, group__delete=False)
    output["group_len"] = len(groups)
    for group in groups:
        output["remain"] += group.remain
    return output


class UserSignup(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        user = check_user_id(data)
        if user:
            user.name = data['name']
        else:
            user = User.objects.create(id=data['user_id'], name=data['name'])
        user.save()
        return Response(get_user_data(user), status=status.HTTP_200_OK)


class UserCheckByID(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        user = check_user_id(data)
        if not user:
            return Response(make_output(10, "Unknown ID"), status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(get_user_data(user), status=status.HTTP_200_OK)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerDetail


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerList


class UserPhoneChange(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        user = check_user_id(data)
        if not user:
            return Response(make_output(10, "Unknown ID"), status=status.HTTP_406_NOT_ACCEPTABLE)
        phone = User.objects.filter(phone_number=data['phone_number'])
        if len(phone) > 0:
            return Response(make_output(11, "Duplicate phone number"), status=status.HTTP_406_NOT_ACCEPTABLE)
        user.phone_validation = data['phone_number']
        user.save()
        return Response(get_user_data(user), status=status.HTTP_200_OK)


class UserPhoneSend(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        user = check_user_id(data)
        if not user:
            return Response(make_output(10, "Unknown ID"), status=status.HTTP_406_NOT_ACCEPTABLE)
        if user.phone_validation == "":
            return Response(make_output(12, "Phone not found"), status=status.HTTP_406_NOT_ACCEPTABLE)
        user.phone_random = id_generator(6, string.digits)
        # send_pattern("bezzanberim", user.phone_random, user.phone_validation, print_debug=True)
        # todo: repair this
        user.save()
        return Response(get_user_data(user), status=status.HTTP_200_OK)


class UserPhoneValidate(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        user = check_user_id(data)
        if not user:
            return Response(make_output(10, "Unknown ID"), status=status.HTTP_406_NOT_ACCEPTABLE)
        # if user.phone_random != data['phone_random']:
        #     return Response(make_output(13, "Not match code."), status=status.HTTP_406_NOT_ACCEPTABLE)
        # todo: repair this
        user.phone_number = user.phone_validation
        user.phone_validation = ""
        user.phone_random = ""
        user.save()
        return Response(get_user_data(user), status=status.HTTP_200_OK)
