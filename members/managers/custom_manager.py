from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from members.settings import LOCAL_URL
from members.token import account_activation_token


class CustomUserManager(BaseUserManager):
    def create(self, email, password, **extra_fields):
        valid = True
        try:
            validate_email(email)
        except ValidationError:
            valid = False

        if valid:
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()
            return user
        return None

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create(email, password, **extra_fields)


def generate_activation_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    activation_link = LOCAL_URL + f'{uid}/{token}'
    print(activation_link)
    return activation_link
