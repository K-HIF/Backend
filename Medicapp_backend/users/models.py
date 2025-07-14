from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class MedicappUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class MedicappUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MedicappUserManager()

    def _str_(self):
        return self.email

    class Meta:
        db_table = 'medicapp_user'


class StarCount_2(models.Model):
    count = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return str(self.count)


class DownvoteCounter(models.Model):
    count = models.PositiveIntegerField(default=0)

    def _str_(self):
        return f"Total Downvotes: {self.count}"


class UserDownvote(models.Model):
    user = models.OneToOneField(MedicappUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} downvoted at {self.timestamp}"


class IPDownvote(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.ip_address} downvoted at {self.timestamp}"


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    staff_id = models.CharField(max_length=100, unique=True)
    status = models.BooleanField(default=True)  # True for active, False for inactive
    employed_date = models.DateField()
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='doctors')

    def __str__(self):
        return f"{self.name} ({self.staff_id})"


class Patient(models.Model):
    name = models.CharField(max_length=255)
    patient_id = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=20)
    dob = models.DateField()
    visits = models.PositiveIntegerField(default=0)
    insurance = models.ForeignKey('InsuranceProvider', on_delete=models.SET_NULL, null=True)
    insurance_plan = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.patient_id})"


class Department(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    hod = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, related_name='headed_departments')
    date_formed = models.DateField()

    @property
    def staff_count(self):
        return self.doctors.count()

    def __str__(self):
        return f"{self.name} (HOD: {self.hod})"


class Program(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    status = models.BooleanField(default=True)  # True for active, False for inactive
    start_date = models.DateField()
    end_date = models.DateField()
    coordinator = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, related_name='coordinated_programs')

    def __str__(self):
        return f"{self.name} (Coordinator: {self.coordinator})"


class InsuranceProvider(models.Model):
    PLAN_CHOICES = [
        ('gold', 'Gold'),
        ('standard', 'Standard'),
        ('basic', 'Basic'),
        ('all', 'All'),
    ]
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    plans = models.CharField(max_length=20, choices=PLAN_CHOICES)
    status = models.BooleanField(default=True)  # True for active, False for inactive
    date_of_agreement = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.plans})"


class Claim(models.Model):
    insurance_name = models.CharField(max_length=255)
    email = models.EmailField()
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Claim for {self.patient.name} ({self.patient.patient_id})"


class Pharmacy(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    manager = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PharmacyItem(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    expiry_date = models.DateField()
    batch_number = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.batch_number})"


class Nurse(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    staff_id = models.CharField(max_length=100, unique=True)
    status = models.BooleanField(default=True)  # True for active, False for inactive
    employed_date = models.DateField()
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='nurses')

    def __str__(self):
        return f"{self.name} ({self.staff_id})"