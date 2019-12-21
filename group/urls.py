from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf import settings

urlpatterns = [
    path('add/', views.GroupAdd.as_view()),
    path('list/', views.GroupList.as_view()),
    path('check/', views.GroupCheck.as_view()),
    path('detail/', views.GroupDetail.as_view()),
    # path('member/', views.GroupMember.as_view()),
    path('transaction/', views.GroupTransaction.as_view()),
    path('change_invite/', views.ChangeInvite.as_view()),
    path('add_member/', views.AddMember.as_view()),

    path('change/chat/', views.GroupChangeID.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
