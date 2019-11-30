import base64
import random
import string

from Utils.config import *
from django.core.files.base import ContentFile
from kavenegar import *


def send_pattern(template, token, receptor=CREATOR_PHONE, token2=None, print_debug=False):
    try:
        api = KavenegarAPI(KAVENEGAR_API)
        params = {
            'receptor': receptor,
            'template': template,
            'token': token,
            'type': 'sms',  # sms vs call
        }
        if token2:
            params['token2'] = token2
        response = api.verify_lookup(params)
        if print_debug:
            print(response)
        return True

    except Exception as e:
        if print_debug:
            print(e)
        return False


def send_message(message, receptor=CREATOR_PHONE, print_debug=False):
    try:
        api = KavenegarAPI(KAVENEGAR_API)
        params = {
            'receptor': receptor,
            'message': message,
            'sender': '10000022000330',
        }
        response = api.sms_send(params)
        if print_debug:
            print(response)
        return True

    except Exception as e:
        if print_debug:
            print(e)
        return False


def id_generator(size=65, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def make_output(error_code=0, error_text=""):
    return {
        'error_code': error_code,
        'error_text': error_text
    }


def copy_obj_to_dic(dic, obj, fields):
    for field in fields:
        dic[field] = getattr(obj, field)


def get_image(image, sub_name):
    name, image_str = image.split(';base64,')
    ext = name.split('/')[-1]
    return ContentFile(base64.b64decode(image_str), name=sub_name + '.' + ext)
