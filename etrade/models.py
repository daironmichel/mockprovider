from django.db import models
from django.contrib.auth.models import User
from authlib.oauth1 import ClientMixin
from authlib.oauth1 import TokenCredentialMixin


class Client(models.Model, ClientMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=48, unique=True, db_index=True)
    client_secret = models.CharField(max_length=48, blank=True)
    default_redirect_uri = models.TextField(blank=False, default='')

    def get_default_redirect_uri(self):
        return self.default_redirect_uri

    def get_client_secret(self):
        return self.client_secret

    def get_rsa_public_key(self):
        return None


class Token(models.Model, TokenCredentialMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=48, db_index=True)
    oauth_token = models.CharField(max_length=84, unique=True, db_index=True)
    oauth_token_secret = models.CharField(max_length=84)

    def get_oauth_token(self):
        return self.oauth_token

    def get_oauth_token_secret(self):
        return self.oauth_token_secret
