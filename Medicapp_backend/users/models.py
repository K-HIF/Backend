from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.postgres.fields import ArrayField



class Program(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    startYear = models.DateField()
    endYear = models.DateField()

    def __str__(self):
        return self.name

class InsuranceProvider(models.Model):
    PLAN_CHOICES = [
        ('Basic', 'Basic'),
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    plan = ArrayField(models.CharField(max_length=50, choices=PLAN_CHOICES), default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    since = models.DateField()
    

    def __str__(self):
        return self.name
    
class Facility(models.Model):
    name = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0)
    occupied = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

class Department(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    date_formed = models.DateField(default=timezone.now)
    hod = models.CharField(max_length=255)  # Head of Department

    def __str__(self):
        return self.name

    @property
    def staff_count(self):
        # Count users in this department, excluding 'admin'
        return MedicappUser.objects.filter(department=self).exclude(department__name='admin').count()

class Patient(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    dob = models.DateField(default=timezone.now)
    age = models.CharField(max_length=255)  
    id_number = models.IntegerField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True,blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    insurance= models.BooleanField(default=False)
    insurance_provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True, null=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    visits = models.PositiveIntegerField(default=0)
    passport_number = models.CharField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name


class MedicappUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, department=None, role_type=None):
        print(f"Creating user with role type: {role_type}") 
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, department=department)
        user.set_password(password)
        user.save(using=self._db)

        

        return user

    def create_superuser(self, email, full_name, password=None, department=None):
        user = self.create_user(email, full_name, password, department)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class MedicappUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  
    
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'department']

    objects = MedicappUserManager()  # Use the custom user manager

    def __str__(self):
        return self.email

class RoleBase(models.Model):
    user = models.OneToOneField(MedicappUser, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)  # Active or inactive
    verification = models.BooleanField(default=False)  # Verified or unverified
    date_employed = models.DateTimeField(default=timezone.now)
    staff_id = models.CharField(max_length=100, unique=True, null=True, blank=True)

    class Meta:
        abstract = True

class Doctor(RoleBase):
    pass

class Nurse(RoleBase):
    pass

class Pharmacy(RoleBase):
    pass

class Lab(RoleBase):
    pass

class Checkout(RoleBase):
    pass

class Reception(RoleBase):
    pass


#Downvote and Star Count Models
class StarCount_2(models.Model):
    count = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.count)

class DownvoteCounter(models.Model):
    count = models.PositiveIntegerField(default=0)

    def __str__(self):  
        return f"Total Downvotes: {self.count}"

class UserDownvote(models.Model):
    user = models.OneToOneField(MedicappUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return f"{self.user.full_name} downvoted at {self.timestamp}"

class IPDownvote(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return f"{self.ip_address} downvoted at {self.timestamp}"
    
#upvote
class UpvoteCounter(models.Model):
    count = models.PositiveIntegerField(default=0)

    def __str__(self):  
        return f"Total Downvotes: {self.count}"

class UserUpvote(models.Model):
    user = models.OneToOneField(MedicappUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return f"{self.user.full_name} downvoted at {self.timestamp}"

class IPUpvote(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return f"{self.ip_address} downvoted at {self.timestamp}"
    
