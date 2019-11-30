import datetime
import string
import sys
from contextlib import contextmanager

from django.core.files import File
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from Utils.server_utils import *
# from user.models import Group
from .serializers import *

import base64


@contextmanager
def check_id(data):
    print(data, file=sys.stderr)
    user = User.objects.filter(id=data["user_id"])
    try:
        if len(user) == 1:
            yield user[0]
        else:
            yield None
    finally:
        pass


@contextmanager
def check_email_api(email, api):
    user = User.objects.filter(email=email, api=api)
    try:
        if len(user) == 1:
            yield user[0]
        else:
            yield None
    finally:
        pass


def get_user_data(user):
    output = make_output()
    copy_obj_to_dic(output, user,
                    ['name', 'score', 'email', 'email_validation', 'phone_number', 'phone_validation'])
    return output


class UserSignup(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        with check_id(data) as user:
            if user:
                return Response(make_output(1, "Duplicate id"), status=status.HTTP_406_NOT_ACCEPTABLE)
            user = User.objects.create(id=data['user_id'], name=data['name'])
            user.save()
            return Response(make_output(), status=status.HTTP_200_OK)


class UserCheckByID(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        with check_id(data) as user:
            if not user:
                return Response(make_output(1, "Unknown ID"), status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response(get_user_data(user), status=status.HTTP_200_OK)


class SendEmailValidate(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data, file=sys.stderr)
        with check_email(data['email']) as user:
            if not user:
                return Response(make_output(1, "Unknown email"), status=status.HTTP_406_NOT_ACCEPTABLE)
            if user.password != data['password']:
                return Response(make_output(2, "Password incorrect."), status=status.HTTP_406_NOT_ACCEPTABLE)
            if user.email_validation:
                return Response(make_output(3, "Email is verify."), status=status.HTTP_406_NOT_ACCEPTABLE)

            user.email_random = id_generator(6, string.digits)
            # send_mail(user[0].email, rand)
            send_mail(
                'کد فعال سازی برای تایید ایمیل',
                'کد فعال سازی شما ' + user.email_random + ' می‌باشد',
                'zeiny.r@yaftar.ir',
                [data['email']],
                fail_silently=False,
            )
            user.save()
            return Response(make_output(), status=status.HTTP_200_OK)


class CheckEmailValidate(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data, file=sys.stderr)
        with check_email(data['email']) as user:
            if not user:
                return Response(make_output(1, "Unknown email"), status=status.HTTP_406_NOT_ACCEPTABLE)
            if user.password != data['password']:
                return Response(make_output(2, "Password incorrect."), status=status.HTTP_406_NOT_ACCEPTABLE)
            if user.email_validation:
                return Response(make_output(3, "Email is verify."), status=status.HTTP_406_NOT_ACCEPTABLE)
            if user.email_random != data['email_random']:
                return Response(make_output(4, "Not match code."), status=status.HTTP_406_NOT_ACCEPTABLE)
            user.email_validation = True
            user.save()
            return Response(make_output(), status=status.HTTP_200_OK)


class ForgotPassEmailValidate(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data, file=sys.stderr)
        with check_email(data['email']) as user:
            if not user:
                return Response(make_output(1, "Unknown email"), status=status.HTTP_406_NOT_ACCEPTABLE)

            user.forgot_password_random = id_generator(6, string.digits)
            # send_mail(user[0].email, rand)
            send_mail(
                'فراموشی گذرواژه',
                'کد مورد نظر برای بازنشانی گذرواژه ' + user.forgot_password_random + ' می‌باشد',
                'zeiny.r@yaftar.ir',
                [data['email']],
                fail_silently=False,
            )
            user.save()
            return Response(make_output(), status=status.HTTP_200_OK)


class ForgotPassCodeCheck(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data, file=sys.stderr)
        with check_email(data['email']) as user:
            if not user:
                return Response(make_output(1, "Unknown email"), status=status.HTTP_406_NOT_ACCEPTABLE)
            if user.forgot_password_random != data['forgot_password_random']:
                return Response(make_output(2, "Not match code."), status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response(make_output(), status=status.HTTP_200_OK)


class ForgotPassChangePass(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data, file=sys.stderr)
        with check_email(data['email']) as user:
            if not user:
                return Response(make_output(1, "Unknown email"), status=status.HTTP_406_NOT_ACCEPTABLE)
            if user.forgot_password_random != data['forgot_password_random']:
                return Response(make_output(2, "Not match code."), status=status.HTTP_406_NOT_ACCEPTABLE)
            user.password = data['password']
            user.save()
            return Response(make_output(), status=status.HTTP_200_OK)


class CheckUserAPI(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data, file=sys.stderr)
        now = datetime.datetime.now()
        with check_email(data['email']) as user:
            if not user:
                return Response(make_output(1, "Unknown email"), status=status.HTTP_406_NOT_ACCEPTABLE)
            if user.api != data['api']:
                return Response(make_output(2, "Not match API."), status=status.HTTP_406_NOT_ACCEPTABLE)
            print(user.api_expire_data, now, file=sys.stderr)
            if max(now, user.api_expire_data) == now:
                return Response(make_output(3, "Expire API."), status=status.HTTP_406_NOT_ACCEPTABLE)
            user.api_expire_data = now + datetime.timedelta(days=5)
            # user.api_expire_data = now
            user.save()
            return Response(make_output(), status=status.HTTP_200_OK)


class SendPhoneValidate(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data, file=sys.stderr)
        with check_email_api(data['email'], data['api']) as user:
            if not user:
                return Response(make_output(1, "Unknown email or API"), status=status.HTTP_406_NOT_ACCEPTABLE)

            user.phone_random = id_generator(6, string.digits)
            user.phone_number = data['phone_number']
            user.phone_validation = False
            # send_mail(user[0].email, rand)
            send_sms(
                data['phone_number'],
                'کد فعال سازی شما ' + user.phone_random + ' می باشد',
            )
            user.save()
            return Response(get_user_data(user), status=status.HTTP_200_OK)


class CheckPhoneValidate(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data, file=sys.stderr)
        with check_email_api(data['email'], data['api']) as user:
            if not user:
                return Response(make_output(1, "Unknown email or API"), status=status.HTTP_406_NOT_ACCEPTABLE)
            if user.phone_random != data['phone_random']:
                return Response(make_output(2, "Not match code."), status=status.HTTP_406_NOT_ACCEPTABLE)
            if user.phone_number != data['phone_number']:
                return Response(make_output(3, "Not match number."), status=status.HTTP_406_NOT_ACCEPTABLE)
            user.phone_validation = True
            user.save()
            return Response(get_user_data(user), status=status.HTTP_200_OK)


class ChangePasswordProfile(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data, file=sys.stderr)
        with check_email_api(data['email'], data['api']) as user:
            if not user:
                return Response(make_output(1, "Unknown email or API"), status=status.HTTP_406_NOT_ACCEPTABLE)
            if user.password != data['password']:
                return Response(make_output(2, "Not match password."), status=status.HTTP_406_NOT_ACCEPTABLE)
            user.password = data['new_password']
            user.save()
            return Response(get_user_data(user), status=status.HTTP_200_OK)


class ChangeNameProfile(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data, file=sys.stderr)
        with check_email_api(data['email'], data['api']) as user:
            if not user:
                return Response(make_output(1, "Unknown email or API"), status=status.HTTP_406_NOT_ACCEPTABLE)
            user.name = data['name']
            user.save()
            return Response(get_user_data(user), status=status.HTTP_200_OK)


class ProfileUploadImage(generics.CreateAPIView):
    serializer_class = UserSerializerEmpty

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data, file=sys.stderr)
        with check_email_api(data['email'], data['api']) as user:
            if not user:
                return Response(make_output(1, "Unknown email or api"), status=status.HTTP_406_NOT_ACCEPTABLE)
            user.image = get_image(data['file'], data['email'].split("@")[0] + "_" +
                                   str(datetime.datetime.now()).replace(" ", "-").split(".")[0])
            user.save()
            # if user.forgot_password_random != data['forgot_password_random']:
            #     return Response(make_output(2, "Not match code."), status=status.HTTP_406_NOT_ACCEPTABLE)
            # user.password = data['password']
            # user.save()
            return Response(get_user_data(user), status=status.HTTP_200_OK)
