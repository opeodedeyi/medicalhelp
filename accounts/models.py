from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, medical_practitioner, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")
        if not medical_practitioner:
            raise ValueError("User must specify if he or she is a medical practioner")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            medical_practitioner = medical_practitioner,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, medical_practitioner, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username,
            medical_practitioner = medical_practitioner,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    IS_MEDICAL_PRACTIONER = (
        ('NO', 'NO'),
        ('YES', 'YES'),
    )

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    medical_practitioner = models.CharField(max_length=3, choices=IS_MEDICAL_PRACTIONER, blank=False, null=False, default="NO")
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'medical_practitioner']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Sickness(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class MedicalInformation(models.Model):
    DURATION = (
        ('0-1 week', '0-1 week'),
        ('2 weeks', '2 weeks'),
        ('3 weeks', '3 weeks'),
        ('4 weeks', '4 weeks'),
        ('5+ weeks', '5+ weeks'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='information')
    sickness = models.ForeignKey(Sickness, on_delete=models.CASCADE, related_name='diagnosis')
    duration = models.CharField(max_length=10, choices=DURATION, blank=False, null=False)
    location = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
