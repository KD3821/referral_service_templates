from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db.models import CharField, BooleanField, DateTimeField, DecimalField
from django.contrib.auth.hashers import make_password, identify_hasher

import random
import string


def referralcode_generator(size=6, chars=string.ascii_uppercase + string.digits):
    referralcode = ''.join(random.choice(chars) for _ in range(size))

    while User.objects.filter(referralcode=referralcode).exists():
        referralcode = ''.join(random.choice(chars) for _ in range(size))

    return referralcode


def passcode_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone, passcode=None, password=None,
                    is_active=True, is_staff=False, is_admin=False):
        if not phone:
            raise ValueError('Укажите номер телефона')
        if not passcode:
            raise ValueError('Укажите 4-х значный код')

        user = self.model(phone=phone, invitecode=None, passcode=passcode)
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, passcode=None, password=None):
        if passcode is None:
            raise ValueError('Задайте 4-х значный пароль!')
        user = self.create_user(phone, passcode=passcode, password=password, is_staff=True, is_admin=True)
        return user

    def create_staffuser(self, phone, passcode=None):
        if passcode is None:
            raise ValueError('Задайте 4-х значный пароль!')
        user = self.create_user(phone, passcode=passcode, is_staff=True, is_admin=False)
        return user


class User(AbstractBaseUser):
    phone = DecimalField(max_digits=11, decimal_places=0, unique=True)
    referralcode = CharField(max_length=100, unique=True)
    invitecode = CharField(max_length=100, null=True, blank=True)
    passcode = CharField(max_length=200, null=True, blank=True)
    staff = BooleanField(default=False)
    admin = BooleanField(default=False)
    active = BooleanField(default=True)
    is_invited = BooleanField(default=False)
    is_verified = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['passcode']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.phone)

    def assign_referralcode(self):
        referralcode = referralcode_generator()
        return referralcode

    def get_username(self):
        return str(self.phone)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def save(self, *args, **kwargs):
        try:
            _alg = identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        if not self.referralcode:
            self.referralcode = self.assign_referralcode()
        super().save(*args, **kwargs)


class TemporaryUser(models.Model):
    phone = DecimalField(max_digits=11, decimal_places=0, unique=True)
    passcode = CharField(max_length=200, verbose_name="Пока не пользователь")

    class Meta:
        verbose_name = 'ПокаНеПользователь'
        verbose_name_plural = 'ПокаНеПользователи'

