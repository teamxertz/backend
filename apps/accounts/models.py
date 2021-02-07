from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager

class User(AbstractBaseUser,PermissionsMixin):
    #Choices
    class Types(models.TextChoices):
        PATIENT = "PATIENT","Patient"
        DOCTOR = "DOCTOR","Doctor"
        HOSPITAL = "HOSPITAL","Hospital"
        SUPERADMIN = "SUPERADMIN", "Super Admin"
    

    objects = UserManager(types=Types)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True)

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    type = models.CharField(_("Type"), max_length=50, choices=Types.choices, default=Types.PATIENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_superuser(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

# Data Models
class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    line1 = models.TextField()
    line2 = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    
class PatientData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(_("Name"),max_length=100)
    phone = models.CharField(_("Phone"), max_length=10, unique=True)
    age = models.PositiveIntegerField()

    class Gender(models.TextChoices):
        NONE = "NONE", "None" #Gender not set
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"

    gender = models.CharField(_("Gender"),max_length=6, default=Gender.NONE, choices=Gender.choices)

class DoctorData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class HospitalData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


#Proxy Models Managers
class PatientManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args,**kwargs).filter(type=User.Types.PATIENT)

class DoctorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args,**kwargs).filter(type=User.Types.DOCTOR)

class HospitalManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args,**kwargs).filter(type=User.Types.HOSPITAL)

# Custom Proxy Models
class Patient(User):
    #base_type = User.Types.PATIENT
    objects = PatientManager()
    class Meta:
        proxy=True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.PATIENT
            super().save(*args, **kwargs)

    @property
    def data():
        return self.patientdata

class Doctor(User):
    #base_type = User.Types.DOCTOR
    objects = DoctorManager()
    class Meta:
        proxy=True

    @property
    def data():
        return self.doctordata

class Hospital(User):
    #base_type = User.Types.HOSPITAL
    objects = HospitalManager()
    class Meta:
        proxy=True
    
    @property
    def data():
        return self.hospitaldata



