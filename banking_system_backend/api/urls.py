from django.urls import path, include
from .views import *

urlpatterns = [
    path('login', login),
    path('logout', logout),
    path('accounts', create_account),
    path('accounts/<int:account_id>/', delete_account),
    path('accounts/balance', get_balance),
    path('accounts/transfer', transfer),
]