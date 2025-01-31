from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models  import BaseUserManager

class UserProfileManager(BaseUserManager):
    """manage user profile"""

    def create_user(self, email, name, password=None):
        """create a user and save it in db"""
        if not email:
            raise ValueError('user must have an email')

        email = self.normalize_email(email)
        user = self.model(name=name, email=email)

        user.set_password(password) #to hash the passeword
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """create and save a super user"""
        user = self.create_user(email, name, password)
        #we use self here to ensure wer are using create_user methode of this class
        #and every change in the future on create_user will be applied on create_superuser

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user




class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for our user"""
    email = models.EmailField(max_length=255, unique= True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager() #this is a mnanager for our user in the database


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """retrieve full name"""
        return self.name

    def __str__(self):
        """retrive string representation of our user"""
        return self.email
