from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, customer_card: int or str, password=None, name=None, is_staff=False, is_admin=False, ):
        if not customer_card:
            raise ValueError("User must have a customer card")
        elif not password:
            raise ValueError("User must have a password")

        else:
            user = self.model(
            customer_card=customer_card
            )
            user.set_password(password)
            user.staff = is_staff
            user.admin = is_admin
            user.name = name or f'Customer {customer_card}'
            user.save(using=self._db)
        return user

    def create_staffuser(self, customer_card, password=None):
        user = self.create_user(
        customer_card,
        password=password,
        is_staff=True
        )
        return user

    def create_superuser(self, customer_card, password=None):
        user = self.create_user(
        customer_card,
        password=password,
        is_staff=True,
        is_admin=True
        )
        return user


class User(AbstractBaseUser):
    customer_card = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)




    USERNAME_FIELD = 'customer_card'
    objects = UserManager()

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.admin

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True

    @property
    def unique_id(self):
        return f"{self.customer_card}-{self.name}-111"
# Create your models here.
