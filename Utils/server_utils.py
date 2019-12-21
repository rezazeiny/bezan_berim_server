import base64
import random
import string
import sys

from Utils.config import *
from django.core.files.base import ContentFile
from kavenegar import *


def send_pattern(template, token, receptor=CREATOR_PHONE, token2=None, token3=None, print_debug=False):
    if print_debug:
        print("Sending SMS to " + receptor, file=sys.stderr)
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
        if token3:
            params['token3'] = token3
        response = api.verify_lookup(params)
        if print_debug:
            print("Sent SMS to " + receptor, file=sys.stderr)
            print(response)
        return True

    except Exception as e:
        if print_debug:
            print("Error in sending SMS to " + receptor, file=sys.stderr)
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


def make_output(result_code=0, error_text=""):
    return {
        'result_code': result_code,
        'error_text': error_text,
        # 'cache_time': time.time()
    }


def copy_obj_to_dic(dic, obj, fields):
    for field in fields:
        dic[field] = getattr(obj, field)


def get_image(image, sub_name):
    name, image_str = image.split(';base64,')
    ext = name.split('/')[-1]
    return ContentFile(base64.b64decode(image_str), name=sub_name + '.' + ext)
