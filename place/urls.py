from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf import settings


urlpatterns = [
    path('add/', views.PlaceAdd.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
    ]


urlpatterns = format_suffix_patterns(urlpatterns)
