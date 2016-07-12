from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, email, password = None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    date_activated = models.DateTimeField(null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    is_company_admin = models.BooleanField(default=False)
    default_company = models.ForeignKey('alverna.Company', null=True, blank=True,
                                        related_name="users",
                                        help_text="Company first selected for a new user when they login for the first time")
    available_companies = models.ManyToManyField('alverna.Company', blank=True)

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    module_access = models.TextField(null=True, blank=True, help_text="Leave blank to only allow dashboard access.")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        return self.email

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True





class Invitation(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="invitations")
    valid = models.BooleanField(default=False)
    key = models.TextField(null=True)
    date_confirmed = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_created']


class PasswordReset(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="password_resets")
    valid = models.BooleanField(default=False)
    key = models.TextField(null=True)
    date_confirmed = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_created']