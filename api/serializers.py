from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Doctor, Patient, HealthRecord, DoctorAnnotation, DoctorNotification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Doctor
        fields = ('id', 'user', 'specialization', 'license_number')
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Patient
        fields = ('id', 'user', 'date_of_birth', 'assigned_doctors')
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        assigned_doctors = validated_data.pop('assigned_doctors', [])
        user = UserSerializer().create(user_data)
        patient = Patient.objects.create(user=user, **validated_data)
        patient.assigned_doctors.set(assigned_doctors)
        return patient

class HealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        fields = ('id', 'patient', 'title', 'description', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class DoctorAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAnnotation
        fields = ('id', 'health_record', 'doctor', 'comment', 'created_at')
        read_only_fields = ('created_at',)

class DoctorNotificationSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = DoctorNotification
        fields = ('id', 'patient', 'patient_name', 'is_new_patient', 'created_at', 'is_read')
        read_only_fields = ('created_at',)
    
    def get_patient_name(self, obj):
        return f"{obj.patient.user.first_name} {obj.patient.user.last_name}" 