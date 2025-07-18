from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Linking to Department
    
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
    staff_id = models.CharField(max_length=100, unique=True)

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

    def __str__(self):  # Corrected method name to __str__
        return f"{self.user.full_name} downvoted at {self.timestamp}"

class IPDownvote(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # Corrected method name to __str__
        return f"{self.ip_address} downvoted at {self.timestamp}"
    

#class Doctor(models.Model):
#    name = models.CharField(max_length=255)
#    email = models.EmailField(unique=True)
#    staff_id = models.CharField(max_length=100, unique=True)
#    status = models.BooleanField(default=True)  # True for active, False for inactive
#    employed_date = models.DateField()
#    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='doctors')
#
#    def __str__(self):
#        return f"{self.name} ({self.staff_id})"
#
#
#class Patient(models.Model):
#    name = models.CharField(max_length=255)
#    patient_id = models.CharField(max_length=100, unique=True)
#    phone = models.CharField(max_length=20)
#    dob = models.DateField()
#    visits = models.PositiveIntegerField(default=0)
#    insurance = models.ForeignKey('InsuranceProvider', on_delete=models.SET_NULL, null=True)
#    insurance_plan = models.CharField(max_length=20)
#
#    def __str__(self):
#        return f"{self.name} ({self.patient_id})"
#
#
#class Department(models.Model):
#    name = models.CharField(max_length=255, unique=True)  # Ensure department names are unique
#    email = models.EmailField(unique=True)
#    hod = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, related_name='headed_departments')
#    date_formed = models.DateField()
#
#    @property
#    def staff_count(self):
#        return (
#            self.doctors.count() +
#            self.nurses.count() +
#            self.lab_technicians.count() +
#            self.pharmacists.count() +
#            self.receptionists.count() +
#            self.finance_staff.count()
#        )
#
#    def __str__(self):
#        return f"{self.name} (HOD: {self.hod})"
#
#class Program(models.Model):
#    STATUS_CHOICES = [
#        ('Active', 'Active'),
#        ('Inactive', 'Inactive'),
#    ]
#
#    name = models.CharField(max_length=255)
#    email = models.EmailField(unique=True)
#    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
#    startYear = models.DateField()
#    endYear = models.DateField()
#
#    def __str__(self):
#        return self.name
#
#class InsuranceProvider(models.Model):
#    PLAN_CHOICES = [
#        ('Basic', 'Basic'),
#        ('Standard', 'Standard'),
#        ('Premium', 'Premium'),
#    ]
#    STATUS_CHOICES = [
#        ('Active', 'Active'),
#        ('Inactive', 'Inactive'),
#    ]
#
#    name = models.CharField(max_length=255)
#    email = models.EmailField(unique=True)
#    plan = ArrayField(models.CharField(max_length=50, choices=PLAN_CHOICES), default=list)
#    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
#    since = models.DateField()
#    logo = models.URLField(default='https://via.placeholder.com/40?text=🏥')
#
#    def __str__(self):
#        return self.name
#    
#
#class Claim(models.Model):
#    insurance_name = models.CharField(max_length=255)
#    email = models.EmailField()
#    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
#    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#
#    def __str__(self):
#        return f"Claim for {self.patient.name} ({self.patient.patient_id})"
#
#
#class Pharmacy(models.Model):
#    name = models.CharField(max_length=255)
#    address = models.CharField(max_length=255)
#    phone = models.CharField(max_length=20)
#    manager = models.CharField(max_length=255)
#
#    def __str__(self):
#        return self.name
#
#
#class PharmacyItem(models.Model):
#    pharmacy = models.ForeignKey(Pharmacy, related_name='items', on_delete=models.CASCADE)
#    name = models.CharField(max_length=255)
#    quantity = models.PositiveIntegerField(default=0)
#    price = models.DecimalField(max_digits=8, decimal_places=2)
#    expiry_date = models.DateField()
#    batch_number = models.CharField(max_length=100)
#
#    def __str__(self):
#        return f"{self.name} ({self.batch_number})"
#
#
#class Nurse(models.Model):
#    name = models.CharField(max_length=255)
#    email = models.EmailField(unique=True)
#    staff_id = models.CharField(max_length=100, unique=True)
#    status = models.BooleanField(default=True)  
#    employed_date = models.DateField()
#    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='nurses')
#
#    def __str__(self):
#        return f"{self.name} ({self.staff_id})"
#
#
#class LabTechnician(models.Model):
#    name = models.CharField(max_length=255)
#    email = models.EmailField(unique=True)
#    staff_id = models.CharField(max_length=100, unique=True)
#    status = models.BooleanField(default=True)
#    employed_date = models.DateField()
#    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='lab_technicians')
#
#    def __str__(self):
#        return f"{self.name} ({self.staff_id})"
#
#
#class Pharmacist(models.Model):
#    name = models.CharField(max_length=255)
#    email = models.EmailField(unique=True)
#    staff_id = models.CharField(max_length=100, unique=True)
#    status = models.BooleanField(default=True)
#    employed_date = models.DateField()
#    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='pharmacists')
#
#    def __str__(self):
#        return f"{self.name} ({self.staff_id})"
#
#
#class Receptionist(models.Model):
#    name = models.CharField(max_length=255)
#    email = models.EmailField(unique=True)
#    staff_id = models.CharField(max_length=100, unique=True)
#    status = models.BooleanField(default=True)
#    employed_date = models.DateField()
#    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='receptionists')
#
#    def __str__(self):
#        return f"{self.name} ({self.staff_id})"
#
#
#class FinanceStaff(models.Model):
#    name = models.CharField(max_length=255)
#    email = models.EmailField(unique=True)
#    staff_id = models.CharField(max_length=100, unique=True)
#    status = models.BooleanField(default=True)
#    employed_date = models.DateField()
#    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='finance_staff')
#
#    def __str__(self):
#        return f"{self.name} ({self.staff_id})"
#
#
#class Facility(models.Model):
#    name = models.CharField(max_length=255)
#    count = models.PositiveIntegerField(default=0)
#    occupied = models.PositiveIntegerField(default=0)
#
#    def __str__(self):
#        return f"{self.name}"