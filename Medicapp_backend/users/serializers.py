from rest_framework import serializers
from .models import MedicappUser , Department#, Doctor, Patient, Program, InsuranceProvider, Claim, Pharmacy, PharmacyItem, Nurse, LabTechnician, Pharmacist, Receptionist, FinanceStaff, Facility
from django.contrib.auth import authenticate
from .models import Department, MedicappUser, Doctor, Nurse, Pharmacy, Lab, Checkout, Reception

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'email', 'date_formed', 'hod', 'staff_count']

class MedicappUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicappUser
        fields = ['id', 'email', 'full_name', 'department', 'is_active', 'is_verified', 'is_staff']

class DoctorSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email')
    user_full_name = serializers.CharField(source='user.full_name')
    department = serializers.CharField(source='user.department.name', read_only=True)
    class Meta:
        model = Doctor
        fields = ['user_full_name', 'user_email', 'staff_id', 'department','date_employed', 'status', 'verification']

class NurseSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email')
    user_full_name = serializers.CharField(source='user.full_name')
    department = serializers.CharField(source='user.department.name', read_only=True)
    class Meta:
        model = Nurse
        fields = ['user_full_name', 'user_email','department', 'staff_id', 'date_employed', 'status', 'verification']

class LabSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email')
    user_full_name = serializers.CharField(source='user.full_name')
    department = serializers.CharField(source='user.department.name', read_only=True)
    class Meta:
        model = Lab
        fields = ['user_full_name', 'user_email', 'staff_id', 'department','date_employed', 'status', 'verification']

class PharmacySerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email')
    user_full_name = serializers.CharField(source='user.full_name')
    department = serializers.CharField(source='user.department.name', read_only=True)
    class Meta:
        model = Pharmacy
        fields = ['user_full_name', 'user_email', 'staff_id', 'department','date_employed', 'status', 'verification']

class CheckoutSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email')
    user_full_name = serializers.CharField(source='user.full_name')
    department = serializers.CharField(source='user.department.name', read_only=True)
    class Meta:
        model = Checkout
        fields = ['user_full_name', 'user_email', 'department','staff_id', 'date_employed', 'status', 'verification']

class ReceptionSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email')
    user_full_name = serializers.CharField(source='user.full_name')
    department = serializers.CharField(source='user.department.name', read_only=True)
    class Meta:
        model = Reception
        fields = ['user_full_name', 'user_email', 'department','staff_id', 'date_employed', 'status', 'verification']



class RegisterSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source='full_name')
    password = serializers.CharField(write_only=True, required=False)
    department = serializers.CharField()

    class Meta:
        model = MedicappUser
        fields = ['email', 'fullName', 'department', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        department_name = validated_data.pop('department', None)

        # Find or create the Department instance
        department, created = Department.objects.get_or_create(name=department_name)

        validated_data['department'] = department  # Set the department instance
        print(f"Creating user in department: {department_name}")


        # Determine role based on department
        role_type = None
        if department_name.lower() == 'doctor':
            role_type = 'doctor'
        elif department_name.lower() == 'nurse':
            role_type = 'nurse'
        elif department_name.lower() == 'lab':
            role_type = 'lab'
        elif department_name.lower() == 'reception':
            role_type = 'reception'
        elif department_name.lower() == 'finance':
            role_type = 'finance'
        elif department_name.lower() == 'pharmacy':
            role_type = 'pharmacy'
        elif department_name.lower() == 'admin':
            role_type = 'admin'
        else:
            raise serializers.ValidationError({"department": "Unknown department"})

        # Create the user instance
        user = MedicappUser(**validated_data)

        # Handle password and user activation
        if role_type == 'admin':
            print('Creating admin user')
            if not password:
                raise serializers.ValidationError({"password": "Password is required for admin registration."})
            user.set_password(password)
            user.is_active = True
            user.is_verified = True
        else:
            user.set_unusable_password()
            user.is_active = False
            user.is_verified = False

        user.save()

        # Create the corresponding role entry
        if role_type == 'doctor':
            Doctor.objects.create(user=user)
            print(f"Created Doctor for user: {user.email}")
        elif role_type == 'nurse':
            Nurse.objects.create(user=user)
            print(f"Created Nurse for user: {user.email}")  
        elif role_type == 'lab':
            Lab.objects.create(user=user)
            print(f"Created Lab Technician for user: {user.email}")
        elif role_type == 'reception':
            Reception.objects.create(user=user)
            print(f"Created Receptionist for user: {user.email}")
        elif role_type == 'finance':
            Checkout.objects.create(user=user)
            print(f"Created Finance Staff for user: {user.email}")
        elif role_type == 'pharmacy':
            Pharmacy.objects.create(user=user)
            print(f"Created Pharmacy Staff for user: {user.email}")

        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("Account is inactive.")
        if not user.is_verified:
            raise serializers.ValidationError("Account is not verified.")
        data['user'] = user
        return data
    
class DepartmentSerializer(serializers.ModelSerializer):
    staff_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'email', 'date_formed', 'hod', 'staff_count']

#class DepartmentNestedSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Department
#        fields = ['id', 'name']
#
#
#class DoctorSerializer(serializers.ModelSerializer):
#    department = DepartmentNestedSerializer(read_only=True)
#    department_id = serializers.PrimaryKeyRelatedField(
#        queryset=Department.objects.all(), source='department', write_only=True, required=False
#    )
#
#    class Meta:
#        model = Doctor
#        fields = ['id', 'name', 'email', 'staff_id', 'status', 'employed_date', 'department', 'department_id']
#
#
#class PatientSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Patient
#        fields = ['id', 'name', 'patient_id', 'phone', 'dob', 'visits', 'insurance', 'insurance_plan']
#
#
#class DepartmentSerializer(serializers.ModelSerializer):
#    hod_name = serializers.SerializerMethodField()
#    doctor_count = serializers.SerializerMethodField()
#    nurse_count = serializers.SerializerMethodField()
#    lab_technician_count = serializers.SerializerMethodField()
#    pharmacist_count = serializers.SerializerMethodField()
#    receptionist_count = serializers.SerializerMethodField()
#    finance_count = serializers.SerializerMethodField()
#    staff_count = serializers.SerializerMethodField()
#
#    class Meta:
#        model = Department
#        fields = [
#            'id', 'name', 'email', 'date_formed', 'hod', 'hod_name',
#            'doctor_count', 'nurse_count', 'lab_technician_count',
#            'pharmacist_count', 'receptionist_count', 'finance_count', 'staff_count'
#        ]
#
#    def get_hod_name(self, obj):
#        return obj.hod.name if obj.hod else None
#
#    def get_doctor_count(self, obj):
#        return obj.doctors.count()
#
#    def get_nurse_count(self, obj):
#        return obj.nurses.count()
#
#    def get_lab_technician_count(self, obj):
#        return obj.lab_technicians.count()
#
#    def get_pharmacist_count(self, obj):
#        return obj.pharmacists.count()
#
#    def get_receptionist_count(self, obj):
#        return obj.receptionists.count()
#
#    def get_finance_count(self, obj):
#        return obj.finance_staff.count()
#
#    def get_staff_count(self, obj):
#        return (
#            self.get_doctor_count(obj) +
#            self.get_nurse_count(obj) +
#            self.get_lab_technician_count(obj) +
#            self.get_pharmacist_count(obj) +
#            self.get_receptionist_count(obj) +
#            self.get_finance_count(obj)
#        )
#
#
#class ProgramSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Program
#        fields = '__all__'
#
#
#class InsuranceProviderSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = InsuranceProvider
#        fields = '__all__'
#
#
#class ClaimSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Claim
#        fields = ['id', 'insurance_name', 'email', 'patient_id', 'patient_name', 'total_amount']
#
#
#class PharmacyItemSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = PharmacyItem
#        fields = ['id', 'name', 'quantity', 'price', 'expiry_date', 'batch_number']
#
#
#class PharmacySerializer(serializers.ModelSerializer):
#    items = PharmacyItemSerializer(many=True, read_only=True)
#    class Meta:
#        model = Pharmacy
#        fields = ['id', 'name', 'address', 'phone', 'manager', 'items']
#
#
#class NurseSerializer(serializers.ModelSerializer):
#    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
#
#    class Meta:
#        model = Nurse
#        fields = ['id', 'name', 'email', 'staff_id', 'status', 'employed_date', 'department']
#
#    def to_representation(self, instance):
#        rep = super().to_representation(instance)
#        rep['department'] = DepartmentNestedSerializer(instance.department).data if instance.department else None
#        return rep
#
#
#class LabTechnicianSerializer(serializers.ModelSerializer):
#    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
#
#    class Meta:
#        model = LabTechnician
#        fields = ['id', 'name', 'email', 'staff_id', 'status', 'employed_date', 'department']
#
#    def to_representation(self, instance):
#        rep = super().to_representation(instance)
#        rep['department'] = DepartmentNestedSerializer(instance.department).data if instance.department else None
#        return rep
#
#
#class PharmacistSerializer(serializers.ModelSerializer):
#    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
#
#    class Meta:
#        model = Pharmacist
#        fields = ['id', 'name', 'email', 'staff_id', 'status', 'employed_date', 'department']
#
#    def to_representation(self, instance):
#        rep = super().to_representation(instance)
#        rep['department'] = DepartmentNestedSerializer(instance.department).data if instance.department else None
#        return rep
#
#
#class ReceptionistSerializer(serializers.ModelSerializer):
#    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
#
#    class Meta:
#        model = Receptionist
#        fields = ['id', 'name', 'email', 'staff_id', 'status', 'employed_date', 'department']
#
#    def to_representation(self, instance):
#        rep = super().to_representation(instance)
#        rep['department'] = DepartmentNestedSerializer(instance.department).data if instance.department else None
#        return rep
#
#
#class FinanceStaffSerializer(serializers.ModelSerializer):
#    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
#
#    class Meta:
#        model = FinanceStaff
#        fields = ['id', 'name', 'email', 'staff_id', 'status', 'employed_date', 'department']
#
#    def to_representation(self, instance):
#        rep = super().to_representation(instance)
#        rep['department'] = DepartmentNestedSerializer(instance.department).data if instance.department else None
#        return rep
#
#
#class FacilitySerializer(serializers.ModelSerializer):
#    deficit = serializers.SerializerMethodField()
#
#    class Meta:
#        model = Facility
#        fields = ['id', 'name', 'count', 'occupied', 'deficit']
#
#    def get_deficit(self, obj):
#        return obj.count - obj.occupied