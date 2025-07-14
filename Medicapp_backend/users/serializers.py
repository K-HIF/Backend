# users/serializers.py
from rest_framework import serializers
from .models import MedicappUser, Doctor, Patient, Department, Program, InsuranceProvider, Claim, Pharmacy, PharmacyItem, Nurse


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MedicappUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = MedicappUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'email', 'staff_id', 'status', 'employed_date', 'department']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'patient_id', 'phone', 'dob', 'visits', 'insurance', 'insurance_plan']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'email', 'hod', 'staff_count', 'date_formed']


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['id', 'name', 'email', 'status', 'start_date', 'end_date', 'coordinator']


class InsuranceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceProvider
        fields = ['id', 'name', 'email', 'plans', 'status', 'date_of_agreement']


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ['id', 'insurance_name', 'email', 'patient_id', 'patient_name', 'total_amount']


class PharmacyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyItem
        fields = ['id', 'name', 'quantity', 'price', 'expiry_date', 'batch_number']


class PharmacySerializer(serializers.ModelSerializer):
    items = PharmacyItemSerializer(many=True, read_only=True)
    class Meta:
        model = Pharmacy
        fields = ['id', 'name', 'address', 'phone', 'manager', 'items']


class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = ['id', 'name', 'email', 'staff_id', 'status', 'employed_date', 'department']