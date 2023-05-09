import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from api.models import User, Token


class login(View):
    @csrf_exempt
    def post(self, request):
        print(request.body)
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Invalid login credentials', 'status': 'error'})
        if user.check_password(password):
            token = Token.objects.get_or_create(user=user)
            return JsonResponse({'message': 'Login successful', 'status': 'success', 'accountId': user.id,
                                 'sessionId': str(token[0]), 'userType': user.userType})
        else:
            return JsonResponse({'message': 'Invalid login credentials', 'status': 'error'})


class logout(View):
    @csrf_exempt
    def post(self, request):
        # 获取token
        auth_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        try:
            token = Token.objects.get(key=auth_token)
            token.delete()
            return JsonResponse({'message': 'Logout successful', 'status': 'success'})
        except Token.DoesNotExist:
            return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})


class createAccount(View):
    @csrf_exempt
    def post(self, request):
        # 获取token
        auth_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        try:
            token = Token.objects.get(key=auth_token)
            current_user = token.user
        except Token.DoesNotExist:
            return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
        if current_user.is_clerk():
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            userType = data['userType']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create(username=username, password=password, userType=userType)
                return JsonResponse({'message': 'Account created successfully',
                                     'status': 'success', 'accountId': user.id})
            return JsonResponse({'message': 'Username already exists', 'status': 'error'})
        else:
            return JsonResponse({'message': 'Current User is not clerk or admin', 'status': 'error'})


@csrf_exempt
def delete_account(request, account_id):
    if request.method == 'DELETE':
        # 获取token
        auth_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        try:
            token = Token.objects.get(key=auth_token)
            current_user = token.user
        except Token.DoesNotExist:
            return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
        if current_user.is_clerk():
            try:
                user = User.objects.get(pk=account_id)
                user.delete()
                return JsonResponse({'message': 'Delete Successfully', 'status': 'success'})
            except User.DoesNotExist:
                return JsonResponse({'message': 'Account does not exist', 'status': 'error'})

        else:
            return JsonResponse({'message': 'Current User is not clerk or admin', 'status': 'error'})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


@csrf_exempt
def get_balance(request):
    if request.method == 'GET':
        # 获取token
        auth_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        try:
            token = Token.objects.get(key=auth_token)
            user = token.user
            return JsonResponse({'message': 'Get balance successfully', 'status': 'success', 'balance': user.balance})
        except Token.DoesNotExist:
            return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


@csrf_exempt
def transfer(request):
    data = json.loads(request.body)
    destAccountId = data['destAccountId']
    amount = data['amount']
    # 禁止非负
    if amount <= 0:
        return JsonResponse({'message': 'Invalid amount', 'status': 'error'})
    # 获取token
    auth_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    try:
        token = Token.objects.get(key=auth_token)
        current_user = token.user
    except Token.DoesNotExist:
        return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
    try:
        dest_user = User.objects.get(pk=destAccountId)
    except User.DoesNotExist:
        return JsonResponse({'message': 'Destination account does not exist', 'status': 'error'})
    if current_user.balance < amount:
        return JsonResponse({'message': 'Insufficient balance', 'status': 'error'})
    current_user.balance -= amount
    dest_user.balance += amount
    current_user.save()
    dest_user.save()
    return JsonResponse({'message': 'Transaction successful', 'status': 'success'})
