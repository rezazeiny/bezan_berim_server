from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf import settings


urlpatterns = [
    path('check/', views.UserCheckByID.as_view()),
    path('signup/', views.UserSignup.as_view()),
    # path('check/', views.CheckUserAPI.as_view()),
    #
    # path('validate/email/send/', views.SendEmailValidate.as_view()),
    # path('validate/email/check/', views.CheckEmailValidate.as_view()),
    #
    # path('validate/forgot/email/', views.ForgotPassEmailValidate.as_view()),
    # path('validate/forgot/check/', views.ForgotPassCodeCheck.as_view()),
    # path('validate/forgot/change/', views.ForgotPassChangePass.as_view()),
    #
    # path('profile/image/upload/', views.ProfileUploadImage.as_view()),
    # path('profile/name/change/', views.ChangeNameProfile.as_view()),
    # path('profile/phone/send/', views.SendPhoneValidate.as_view()),
    # path('profile/phone/check/', views.CheckPhoneValidate.as_view()),
    # path('profile/password/change/', views.ChangePasswordProfile.as_view()),

    # path('show/profile/', views.ShowProfileUsername.as_view()),
    # path('change/profile/', views.ChangeProfilePage.as_view()),
    # path('change/image/', views.ChangeImage.as_view()),
    # path('change/password/', views.ChangePassword.as_view()),
    # path('change/email/', views.ChangeEmail.as_view()),
    # path('change/phone/', views.ChangePhone.as_view()),

    # path('validate/send/phone/', views.SendSMS.as_view()),
    # path('validate/check/phone/', views.CheckValidatePhone.as_view()),

]

if settings.DEBUG:
    urlpatterns += [
        # path('list/', views.UserList.as_view()),
        # path('detail/<int:pk>/', views.UserDetail.as_view())
    ]


urlpatterns = format_suffix_patterns(urlpatterns)
