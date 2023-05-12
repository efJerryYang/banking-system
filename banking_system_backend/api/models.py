import secrets

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone


# User model
class User(models.Model):
    CUSTOMER = 'customer'
    CLERK = 'clerk'
    USER_TYPE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (CLERK, 'Clerk'),
    ]
    STATUS_CHOICES = [
        ('passed', 'Passed'),
        ('pending', 'Pending'),
    ]
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    userType = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=CUSTOMER)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def check_password(self, password):
        return self.password == password

    def is_clerk(self):
        return self.userType == self.CLERK


class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transfers')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transfers')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.sender.username} transferred {self.amount} to {self.receiver.username}'

    class Meta:
        ordering = ['-timestamp']

    def to_dict(self):
        return {
            'id': self.id,
            'src_user': self.sender.username,
            'dst_user': self.receiver.username,
            'amount': str(self.amount),
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=40, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(default=None)

    def is_expired(self):
        return self.expires <= timezone.now()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = secrets.token_hex(20)
        return super().save(*args, **kwargs)

    def update_expiration(self):
        self.expires = timezone.now() + timezone.timedelta(hours=1)
        self.save()

@receiver(pre_save, sender=Token)
def generate_token_key(sender, instance, **kwargs):
    # 设置Token对象的过期时间为创建时间加上1小时
    instance.expires = timezone.now() + timezone.timedelta(hours=1)


@receiver(post_save, sender=Token)
def delete_expired_tokens(sender, **kwargs):
    # 删除过期的Token对象
    Token.objects.filter(expires__lt=timezone.now()).delete()
