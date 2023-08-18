from django.db import models
from django.contrib.auth.models import (
        AbstractBaseUser, PermissionsMixin,  BaseUserManager
    )

# Create your models here.

class CustomUserManager(BaseUserManager):
    """This class represents a custom user manager instead of  the default Django user manager

    Args:
        BaseUserManager (_type_): _description_
    """

    def create_user(self, email, password, **extra_fields):
        
        email = self.normalize_email(email)

        user = self.model(
            email = email,
            **extra_fields
        )

        user.set_password(password)

        user.save()

        return user
    


    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff to be True')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser to be True')
        
        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    """_summary_

    Args:
        AbstractUser (_type_): _description_
    """

    email = models.EmailField(max_length=254, unique=True, blank=False, null=False, error_messages= {
        "max_length": 'This field must not be more than 254 characters',
        "null": "This field must not be empty",
        "blank": "This field must not be empty",
        "unique": "This email already exists"
    })
    fullname = models.CharField(max_length=300, blank=False, null=False)
    mobile = models.CharField(max_length=11, unique=True, blank=False, null=False, error_messages= {
        "max_length": 'This field must not be more than 11 characters',
        "null": "This field must not be empty",
        "blank": "This field must not be empty",
        "unique": "This Phone Number already exists"
    })
    account_number = models.CharField(max_length=10, unique=True, blank=False, null=False, error_messages= {
        "max_length": 'This field must not be more than 10 characters',
        "null": "This field must not be empty",
        "blank": "This field must not be empty",
        "unique": "This Account Number already exists"
    })
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname", "mobile"]

    def __str__(self):
        return f"{self.fullname}"
    
    class Meta:
        ordering = ('-created_at', )
        verbose_name_plural = "User"