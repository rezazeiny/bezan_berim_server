from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf import settings

urlpatterns = [
    path('check/', views.UserCheckByID.as_view()),
    path('signup/', views.UserSignup.as_view()),
    path('phone/change/', views.UserPhoneChange.as_view()),
    path('phone/send/', views.UserPhoneSend.as_view()),
    path('phone/validate/', views.UserPhoneValidate.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        path('list/', views.UserList.as_view()),
        path('list/<int:pk>/', views.UserDetail.as_view())
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
