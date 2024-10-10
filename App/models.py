from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


class CommonTimePicker(models.Model):
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField("Updated At", auto_now_add=True)
    class Meta:
        abstract = True


class MyUserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an Email Address')
        user = self.model(
            email=self.normalize_email(email),
            is_active=False,)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        if user.is_superuser:
            user.first_name = "Admin"
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    

class MyUser(AbstractBaseUser,CommonTimePicker):
    full_name = models.CharField("Full Name", max_length=255, blank=True, null=True)
    user_name = models.CharField("User Name", max_length=255, blank=True, null=True,unique=True)
    phone_number = models.CharField("Phone Number",max_length=10,default=0)
    email = models.EmailField("Email", unique=True,max_length=255, blank=True, null=True)
    
    
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField("Super User", default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
 

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
     
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
    
        
    class Meta:
        verbose_name_plural = 'My User'
        ordering = ('-created_at',)   



class NotifyModal(CommonTimePicker):
    domain_name = models.CharField("Domain Name",max_length=200, blank=True, null=True)
    server_ip = models.CharField("Server Ip", max_length=200, blank=True, null=True)
    associated_account = models.CharField("Associated Account", max_length=200, blank=True, null=True)
    customer_id = models.CharField("Customer ID", max_length=200, blank=True, null=True)
    domain_account = models.CharField("Domain - Account", max_length=200, blank=True, null=True)
    ssl_status = models.CharField("SSL Status", max_length=200, blank=True, null=True)
    hosted_account = models.CharField("Hosted Account", max_length=200, blank=True, null=True)
    remark = models.CharField("Remark", max_length=200, blank=True, null=True)
    expires = models.CharField("Expires", max_length=200, blank=True, null=True)

    def __str__(self):
        return self.domain_name


class EmployeeModal(CommonTimePicker):
    emp_name = models.CharField("Employee Name", max_length=100,null=True, blank=True)
    email_address = models.CharField("Email Address", max_length=100,null=True, blank=True)
    expires = models.CharField("Expires", max_length=200, blank=True, null=True)
    password = models.CharField("Password",max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.emp_name
