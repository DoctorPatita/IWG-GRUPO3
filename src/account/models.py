from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import pre_save


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Los usuarios deben tener un correo electronico")
        if not username:
            raise ValueError("Los usuarios deben tener un nombre de usuario")
             
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                = models.CharField(verbose_name="Nombre de usuario", max_length=30, unique=True)
    date_joined             = models.DateTimeField(verbose_name='Fecha de registro', auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='Ultimo inicio de sesión', auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    profile_pic             = models.ImageField(default="default_pic.jpg", null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects= MyAccountManager()


    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_Label):
        return True
    
@receiver(pre_save, sender=Usuario)
def delete_old_pfp(sender, instance, *args, **kwargs):
    if instance.pk:
        existing_image = Usuario.objects.get(pk=instance.pk)
        if instance.profile_pic and existing_image.profile_pic != instance.profile_pic:
            existing_image.profile_pic.delete(False)