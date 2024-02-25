from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class AllUser(BaseUserManager):
    def create_user(self, phone, email, password=None, first_name=None, last_name=None, **kwargs):
        if not email:
            raise ValueError('کاربر باید پست الکترونیکی داشته باشد')
        
        if not phone:
            raise ValueError('کاربر باید شماره تلفن داشته باشد')
        
        if not first_name:
            raise ValueError('کاربر باید شماره نام داشته باشد')
        
        if not last_name:
            raise ValueError('کاربر باید شماره نام خانوادگی داشته باشد')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            **kwargs,
        )
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, phone, email, password, first_name, last_name):
        user = self.create_user(
            email=email,
            phone=phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_active  = False
        user.is_superuser = False        
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password, first_name, last_name):
        user = self.create_user(
            email=email,
            phone=phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_staff = True
        user.is_active  = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='فقط نمادهای الفبایی و اعداد پذیرفته میشوند')
    numbers      = RegexValidator(r'^[0-9a]*$', message='تنها اعداد پذیرفته میشوند')
    phone        = models.CharField(max_length=11, unique=True, validators=[numbers], verbose_name='شماره تماس', help_text='این فیلد برای احراز هویت استفاده میشود، در انتخاب آن دقت کنید')
    email        = models.EmailField(verbose_name='پست الکترونیکی', unique=True, max_length=244, help_text='این فیلد الزامی میباشد')
    first_name   = models.CharField(max_length=30, null=True, blank=True, verbose_name='نام', help_text='این فیلد الزامی میباشد')
    last_name    = models.CharField(max_length=50, null=True, blank=True, verbose_name='نام خانوادگی', help_text='این فیلد الزامی میباشد')
    pic          = models.ImageField(upload_to='user/', default='pic1.png')
    
    # TODO : for User's to be able to login
    is_active    = models.BooleanField(default=False, null=False, verbose_name='وضعیت فعالیت')
    
    # TODO : for OTP, if someone use OTP more than certain time, it becomes false for certain time 
    is_locked    = models.BooleanField(default=False, null=False, verbose_name='')
    
    is_staff     = models.BooleanField(default=False, null=False, verbose_name='دسترسی ادمین')
    is_superuser = models.BooleanField(default=False, null=False, verbose_name='مدیر')
    
    # role         = models.PositiveSmallIntegerField(choices=User_Role.ROLE, default=2, verbose_name='نقش')

    objects = AllUser()

    USERNAME_FIELD  = 'phone'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    @property
    def fullName(self):
        return str(self.first_name) + " " + str(self.last_name)

    def __str__(self):
        return f"{self.phone}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_otp")
    otp  = models.CharField(max_length=6, unique=True)
    created_at = models.TimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.user}"


class Profile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    phone      = models.CharField(max_length=11)
    email      = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name  = models.CharField(max_length=30)
    pic        = models.ImageField(upload_to='profile/')
    role       = models.PositiveSmallIntegerField()
    
    @property
    def fullName(self):
        return str(self.first_name) + " " + str(self.last_name)
    
    def __str__(self) -> str:
        return f"{self.user}"
