# users/serializers.py
from rest_framework import serializers
from .models import MedicappUser, Doctor, Patient, Department, Program, InsuranceProvider, Claim, Pharmacy, PharmacyItem, Nurse, LabTechnician, Pharmacist, Receptionist, FinanceStaff


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
    hod_name = serializers.SerializerMethodField()
    doctor_count = serializers.SerializerMethodField()
    nurse_count = serializers.SerializerMethodField()
    lab_technician_count = serializers.SerializerMethodField()
    pharmacist_count = serializers.SerializerMethodField()
    receptionist_count = serializers.SerializerMethodField()
    finance_count = serializers.SerializerMethodField()
    staff_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            'id', 'name', 'email', 'date_formed', 'hod', 'hod_name',
            'doctor_count', 'nurse_count', 'lab_technician_count',
            'pharmacist_count', 'receptionist_count', 'finance_count', 'staff_count'
        ]

    def get_hod_name(self, obj):
        return obj.hod.name if obj.hod else None

    def get_doctor_count(self, obj):
        return obj.doctors.count()

    def get_nurse_count(self, obj):
        return obj.nurses.count()

    def get_lab_technician_count(self, obj):
        return obj.lab_technicians.count()

    def get_pharmacist_count(self, obj):
        return obj.pharmacists.count()

    def get_receptionist_count(self, obj):
        return obj.receptionists.count()

    def get_finance_count(self, obj):
        return obj.finance_staff.count()

    def get_staff_count(self, obj):
        return (
            self.get_doctor_count(obj) +
            self.get_nurse_count(obj) +
            self.get_lab_technician_count(obj) +
            self.get_pharmacist_count(obj) +
            self.get_receptionist_count(obj) +
            self.get_finance_count(obj)
        )


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