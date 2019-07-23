from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

account_activation_token = PasswordResetTokenGenerator()
