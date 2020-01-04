from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf import settings

urlpatterns = [
    path('add/', views.GroupAdd.as_view()),
    path('list/', views.GroupList.as_view()),
    path('check/', views.GroupCheck.as_view()),
    path('change_chat_id/', views.GroupChangeChatID.as_view()),
    path('join/', views.GroupJoin.as_view()),
    path('left/', views.GroupLeft.as_view()),
    path('members/', views.GroupMembers.as_view()),
    path('transactions/', views.GroupTransactions.as_view()),
    path('transaction/', views.GroupAddTransaction.as_view()),
    path('del_transaction/', views.GroupDeleteTransaction.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
