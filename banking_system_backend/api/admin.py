from django.contrib import admin
from api.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'status', 'userType', 'balance')
    list_filter = ('userType',)
    search_fields = ('username',)


class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user_username', 'created', 'expires')
    list_filter = ('user',)
    search_fields = ('user__username',)

    def user_username(self, obj):
        return obj.user.username


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('sender_username', 'receiver_username', 'amount', 'timestamp', 'status')
    list_filter = ('status',)
    search_fields = ('sender__username', 'receiver__username')

    def sender_username(self, obj):
        return obj.sender.username

    def receiver_username(self, obj):
        return obj.receiver.username


admin.site.register(User, UserAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(Transaction, TransactionAdmin)
# Register your models here.
