import bcrypt
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=150, unique=True)
    password = models.TextField(_('password'))
    email = models.EmailField(_('email'), max_length=255, unique=True)
    name = models.CharField(_('fullname'), max_length=255)
    own_code = models.CharField(_('refferal_code'), max_length=10)
    referral_code = models.CharField(_('refferal_code'), max_length=10)

    USERNAME_FIELD='username'
    REQUIRED_FIELDS = ['password', 'name', 'email']

    def __str__(self):
        return self.username
    
    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "ref_code": self.referral_code if self.referral_code else None,
        }

    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))