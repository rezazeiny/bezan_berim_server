import sys

from Utils.company import ADMIN_MAIL
# from app.models import Category
from user.models import User


# noinspection PyUnresolvedReferences
def reset_all():
    # user = User.objects.filter(email="alavi.sa@yaftar.ir")[0]
    # user.admin_validation = True
    # user.save()
    if len(Group.objects.all()) == 0:
        reset_groups()
    if len(User.objects.all()) == 0:
        reset_users()
    if len(MainAccess.objects.all()) == 0:
        reset_main_access()
    if len(Category.objects.all()) == 0:
        reset_categories()


# noinspection PyUnresolvedReferences
def reset_users():
    print("reset_users", file=sys.stderr)
    user = User.objects.create(email=ADMIN_MAIL, password="reza12qw", name="رضا زینی",
                               group=Group.objects.filter(name="ظفیر")[0])
    user.admin_validation = True
    user.email_validation = True
    user.save()


# noinspection PyUnresolvedReferences
def reset_main_access():
    print("reset_access", file=sys.stderr)
    user = User.objects.filter(email=ADMIN_MAIL)[0]
    # user.main_access.create(name="salam")
    user.save()


