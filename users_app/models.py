import bcrypt
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.translation import gettext_lazy as _

from .utils import generate_referral_code


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, name, **extra_fields):
        if not username:
            raise ValueError('The given username must be set.')
        if not email:
            raise ValueError('The given email must be set.')
        if not password:
            raise ValueError('Password must be set.')
        if not name:
            raise ValueError('Name must be set.')
        
        email = self.normalize_email(email=email)
        user = self.model(username=username, email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, name, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        self.create_user(username=username, email=email, password=password, name=name, **extra_fields)
        
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=150, unique=True)
    password = models.TextField(_('password'))
    email = models.EmailField(_('email'), max_length=255, unique=True)
    name = models.CharField(_('fullname'), max_length=255)
    own_code = models.CharField(_('refferal_code'), max_length=10)
    referral_code = models.CharField(_('refferal_code'), max_length=10)

    USERNAME_FIELD='username'
    REQUIRED_FIELDS = ['password', 'name', 'email']

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "my_referral_code": self.own_code if self.own_code else None,
        }

    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))
    
    def generate_personal_ref_code(self):
        self.own_code = generate_referral_code(self.username)