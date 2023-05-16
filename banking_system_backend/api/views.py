import json
from django.http import JsonResponse
from django.db import transaction
from api.models import *
from django.db.models import Q
import uuid

def register(request):
    # 检查请求方法是否正确
    if request.method == 'POST':
        # 获取用户名与密码
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        # 检查用户是否存在
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'User already exists', 'status': 'error'})
        else:
            # 创建用户
            user = User.objects.create(username=username, password=password)
            user.save()
            return JsonResponse({'message': 'Register successful', 'status': 'success'})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


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
            return JsonResponse({'message': 'User does not exist', 'status': 'error'})
        # 检查用户状态
        if user.status == 'pending':
            return JsonResponse({'message': 'User pending,please contact the clerk', 'status': 'error'})
        # 检查密码是否正确
        if user.check_password(password):
            # 使用get_or_create方法获取or创建token
            token, create = Token.objects.get_or_create(user=user)
            # 如果token并非刚被创建，则删除旧token，再创建新token
            if not create:
                token.delete()
                token = Token.objects.create(user=user)
            return JsonResponse({'message': 'Login successful', 'status': 'success', 'accountId': user.id,
                                 'sessionId': token.key, 'userType': user.userType})
        else:
            return JsonResponse({'message': 'Invalid password', 'status': 'error'})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


def logout(request):
    if request.method == 'GET':
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
            # 如果token不存在，那可能已经过期删除了，可以算是登出成功
            return JsonResponse({'message': 'Logout successful', 'status': 'success'})
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
        # 检查当前session是否过期，如果过期则删除并返回错误，否则更新session
        if token.is_expired():
            token.delete()
            return JsonResponse({'message': 'Session expired', 'status': 'error'})
        else:
            token.update_expiration()
        # 检查当前用户是否为clerk
        if current_user.is_clerk():
            # 获取新用户的信息
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            userType = data['userType']
            # 检查用户是否已经存在
            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'Username already exists', 'status': 'error'})
            user = User.objects.create(username=username, password=password, userType=userType, status='passed')
            return JsonResponse({'message': 'Account created successfully',
                                 'status': 'success', 'accountId': user.id})
        else:
            return JsonResponse({'message': 'Current User is not clerk', 'status': 'error'})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


def delete_account(request, account_id):
    # 检查请求方法是否正确
    if request.method == 'DELETE':
        if account_id.isdigit() is False:
            return JsonResponse({'message': 'Invalid account id', 'status': 'error'})
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
        # 检查当前session是否过期，如果过期则删除并返回错误，否则更新session
        if token.is_expired():
            token.delete()
            return JsonResponse({'message': 'Session expired', 'status': 'error'})
        else:
            token.update_expiration()
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
        except Token.DoesNotExist:
            return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
        # 检查当前session是否过期，如果过期则删除并返回错误，否则更新session
        if token.is_expired():
            token.delete()
            return JsonResponse({'message': 'Session expired', 'status': 'error'})
        else:
            token.update_expiration()
        user = token.user
        return JsonResponse({'message': 'Get balance successfully', 'status': 'success', 'balance': user.balance})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


@transaction.atomic
def transfer(request):
    # 获取转账信息
    data = json.loads(request.body)
    destAccountId = data['destAccountId']
    amount = data['amount']
    if destAccountId.isdigit() is False:
        return JsonResponse({'message': 'Invalid destAccountId', 'status': 'error'})
    # 非负
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
    # 检查当前session是否过期，如果过期则删除并返回错误，否则更新session
    if token.is_expired():
        token.delete()
        return JsonResponse({'message': 'Session expired', 'status': 'error'})
    else:
        token.update_expiration()
    # 查看目标账户是否存在
    try:
        if destAccountId == current_user.id:
            return JsonResponse({'message': 'Cannot transfer to yourself', 'status': 'error'})
        dest_user = User.objects.get(pk=destAccountId)
    except User.DoesNotExist:
        return JsonResponse({'message': 'Dest account does not exist', 'status': 'error'})
    # 检查余额是否足够
    if current_user.balance < amount:
        Transaction.objects.create(sender=current_user, receiver=dest_user, amount=amount, status='failed')
        return JsonResponse({'message': 'Insufficient balance', 'status': 'error'})
    current_user.balance -= amount
    dest_user.balance += amount
    current_user.save()
    dest_user.save()
    Transaction.objects.create(sender=current_user, receiver=dest_user, amount=amount, status='success')
    return JsonResponse({'message': 'Transaction successful', 'status': 'success'})


def get_transactions(request):
    # 检查请求方法是否正确
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
        except Token.DoesNotExist:
            return JsonResponse({'message': 'Invalid AUTHORIZATION', 'status': 'error'})
        # 检查当前session是否过期，如果过期则删除并返回错误，否则更新session
        if token.is_expired():
            token.delete()
            return JsonResponse({'message': 'Session expired', 'status': 'error'})
        else:
            token.update_expiration()
        # 获取当前用户的所有交易记录
        if user.is_clerk():
            transactions = Transaction.objects.all()
        else:
            transactions = Transaction.objects.filter(Q(sender=user) | Q(receiver=user))
        # 将交易记录转化为json格式
        transaction_list = []
        for transaction in transactions:
            transaction_list.append({'sender': transaction.sender.username,
                                     'receiver': transaction.receiver.username,
                                     'amount': transaction.amount,
                                     'id': uuid.uuid4().hex,
                                     'status': transaction.status})
        return JsonResponse({'message': 'Get transactions successfully', 'status': 'success',
                             'transactions': transaction_list})
    else:
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})


def get_all_pending_user(request):
    if request.method != 'GET':
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})
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
    # 检查当前session是否过期，如果过期则删除并返回错误，否则更新session
    if token.is_expired():
        token.delete()
        return JsonResponse({'message': 'Session expired', 'status': 'error'})
    else:
        token.update_expiration()
    # 检查当前用户是否为clerk
    if current_user.is_clerk() is False:
        return JsonResponse({'message': 'Permission denied', 'status': 'error'})
    # 获取所有待审核用户
    users = User.objects.filter(status='pending')
    # 将用户转化为json格式
    user_list = []
    for user in users:
        user_list.append({'id': user.id, 'username': user.username, 'userType': user.userType})
    return JsonResponse({'message': 'Get all pending user successfully', 'status': 'success', 'users': user_list})


def set_user_passed(request, account_id):
    if request.method != 'GET':
        return JsonResponse({'message': 'Invalid request method', 'status': 'error'})
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
    # 检查当前session是否过期，如果过期则删除并返回错误，否则更新session
    if token.is_expired():
        token.delete()
        return JsonResponse({'message': 'Session expired', 'status': 'error'})
    else:
        token.update_expiration()
    # 检查当前用户是否为clerk
    if current_user.is_clerk() is False:
        return JsonResponse({'message': 'Permission denied', 'status': 'error'})
    # 检查目标用户是否存在
    try:
        dest_user = User.objects.get(pk=account_id)
    except User.DoesNotExist:
        return JsonResponse({'message': 'Dest account does not exist', 'status': 'error'})
    # 检查目标用户是否为pending
    if dest_user.status != 'pending':
        return JsonResponse({'message': 'Dest account is not pending', 'status': 'error'})
    # 设置目标用户为passed
    dest_user.status = 'passed'
    dest_user.save()
    return JsonResponse({'message': 'Set user passed successfully', 'status': 'success'})