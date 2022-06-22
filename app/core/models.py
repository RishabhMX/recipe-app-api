"""
Database models

"""


from django.db import models
from django.contrib.auth.models import(
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)

class  UserManager(BaseUserManager):
    """Manager for users"""
    def create_user(self,email,password=None,**extra_fields):
        """Create ,save, and return a new user"""
        user = self.model(email = email,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user



class User(AbstractUser,PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager() # assigning usermanager

    USERNAME_FIELD = 'email'
