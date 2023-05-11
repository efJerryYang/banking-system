import json
from django.http import JsonResponse
from django.db import transaction
from api.models import User, Token


def login(request):
    # 检查请求方法是否正确
    if request.method == 'POST':
        # 获取用户名与密码
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        # 检查用户是否存在
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'message': '不存在此用户', 'status': 'error'})
        # 检查密码是否正确
        if user.check_password(password):
            token = Token.objects.get_or_create(user=user)
            return JsonResponse({'message': 'Login successful', 'status': 'success', 'accountId': user.id,
                                 'sessionId': str(token[0]), 'userType': user.userType})
        else:
            return JsonResponse({'message': '密码错误', 'status': 'error'})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


def logout(request):
    if request.method == 'POST':
        # 获取token
        temp = request.META.get('HTTP_AUTHORIZATION').split(' ')
        if len(temp) > 1:
            auth_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        else:
            return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
        # 删除token
        try:
            token = Token.objects.get(key=auth_token)
            token.delete()
            return JsonResponse({'message': 'Logout successful', 'status': 'success'})
        except Token.DoesNotExist:
            return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


def create_account(request):
    # 检查请求方法是否正确
    if request.method == 'POST':
        # 获取token
        temp = request.META.get('HTTP_AUTHORIZATION').split(' ')
        if len(temp) > 1:
            auth_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        else:
            return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
        # 寻找token对应的用户
        try:
            token = Token.objects.get(key=auth_token)
            current_user = token.user
        except Token.DoesNotExist:
            return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
        # 检查当前用户是否为clerk
        if current_user.is_clerk():
            # 获取新用户的信息
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            userType = data['userType']
            # 检查用户是否已经存在
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create(username=username, password=password, userType=userType)
                return JsonResponse({'message': 'Account created successfully',
                                     'status': 'success', 'accountId': user.id})
            return JsonResponse({'message': 'Username already exists', 'status': 'error'})
        else:
            return JsonResponse({'message': 'Current User is not clerk', 'status': 'error'})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


def delete_account(request, account_id):
    # 检查请求方法是否正确
    if request.method == 'DELETE':
        # 获取token
        temp = request.META.get('HTTP_AUTHORIZATION').split(' ')
        if len(temp) > 1:
            auth_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        else:
            return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
        # 寻找token对应的用户
        try:
            token = Token.objects.get(key=auth_token)
            current_user = token.user
        except Token.DoesNotExist:
            return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
        # 检查当前用户是否为clerk
        if current_user.is_clerk():
            try:
                user = User.objects.get(pk=account_id)
                user.delete()
                return JsonResponse({'message': 'Delete Successfully', 'status': 'success'})
            except User.DoesNotExist:
                return JsonResponse({'message': 'Account does not exist', 'status': 'error'})

        else:
            return JsonResponse({'message': 'Current User is not clerk', 'status': 'error'})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


def get_balance(request):
    if request.method == 'GET':
        # 获取token
        temp = request.META.get('HTTP_AUTHORIZATION').split(' ')
        if len(temp) > 1:
            auth_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        else:
            return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
        # 寻找token对应的用户
        try:
            token = Token.objects.get(key=auth_token)
            user = token.user
            return JsonResponse({'message': 'Get balance successfully', 'status': 'success', 'balance': user.balance})
        except Token.DoesNotExist:
            return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


@transaction.atomic
def transfer(request):
    # 获取转账信息
    data = json.loads(request.body)
    destAccountId = data['destAccountId']
    amount = data['amount']
    # 禁止非负
    if amount <= 0:
        return JsonResponse({'message': 'Invalid amount', 'status': 'error'})
    # 获取token
    temp = request.META.get('HTTP_AUTHORIZATION').split(' ')
    if len(temp) > 1:
        auth_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
    else:
        return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
    # 寻找token对应的用户
    try:
        token = Token.objects.get(key=auth_token)
        current_user = token.user
    except Token.DoesNotExist:
        return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
    # 检查余额是否足够
    if current_user.balance < amount:
        return JsonResponse({'message': 'Insufficient balance', 'status': 'error'})
    # 查看目标账户是否存在
    try:
        dest_user = User.objects.get(pk=destAccountId)
    except User.DoesNotExist:
        return JsonResponse({'message': 'Destination account does not exist', 'status': 'error'})
    current_user.balance -= amount
    dest_user.balance += amount
    current_user.save()
    dest_user.save()
    return JsonResponse({'message': 'Transaction successful', 'status': 'success'})
