from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', login),
    path('logout', logout),
    path('register', register),
    path('accounts', create_account),
    path('accounts/<account_id>/', delete_account),
    path('accounts/balance', get_balance),
    path('accounts/transfer', transfer),
    path('accounts/transactions', get_transactions),
    path('accounts/pending', get_all_pending_user),
    path('accounts/passed/<account_id>/', set_user_passed),
]