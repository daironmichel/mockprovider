from django.contrib import admin

from .models import Client, Token


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'client_secret', 'default_redirect_uri', 'user')
    list_display_links = ('client_id',)


class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'oauth_token', 'oauth_token_secret', 'user')
    list_display_links = ('client_id',)


admin.site.register(Client, ClientAdmin)
admin.site.register(Token, TokenAdmin)
