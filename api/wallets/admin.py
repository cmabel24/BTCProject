from django.contrib import admin

from .models import Key, Wallet,Transaction

admin.site.register(Key)
admin.site.register(Wallet)
admin.site.register(Transaction)
