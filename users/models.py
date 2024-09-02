from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    username = None  # As username is not in use
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # Set username field as email
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        # Convert Email to lowercase to avoid Case Senstivity
        self.email = self.email.lower()
        if not self.pk:
            # Hash & set the password & mark is_active True
            self.set_password(self.password)
            self.is_active = True
        super(User, self).save(*args, **kwargs)


class BaseModel(models.Model):
    '''Abstract Model with base Fields'''
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, models.PROTECT,
                                   related_name='%(class)s_created_by')
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, models.PROTECT, null=True,
                                    related_name='%(class)s_modified_by')
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
