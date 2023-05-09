from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', login.as_view()),
    path('logout', logout.as_view()),
    path('accounts', createAccount.as_view()),
    path('accounts/<int:account_id>/', delete_account),
    path('accounts/balance', get_balance),
    path('accounts/transfer', transfer),
]