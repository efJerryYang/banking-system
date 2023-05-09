import secrets

from django.db import models


# User model
class User(models.Model):
    CUSTOMER = 'customer'
    CLERK = 'clerk'
    ADMIN = 'admin'
    USER_TYPE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (CLERK, 'Clerk'),
        (ADMIN, 'Admin'),
    ]
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    userType = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def check_password(self, password):
        return self.password == password

    def is_clerk(self):
        return self.userType == self.CLERK


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        # 生成40个字符的随机字符串作为key
        return secrets.token_hex(20)

    def __str__(self):
        return self.key
