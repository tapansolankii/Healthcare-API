from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    assigned_doctors = models.ManyToManyField(Doctor, related_name='patients')
    
    def __str__(self):
        return self.user.get_full_name()

class HealthRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='health_records')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.patient}"

class DoctorAnnotation(models.Model):
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, related_name='annotations')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Annotation by Dr. {self.doctor} on {self.health_record}"

class DoctorNotification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='notifications')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    is_new_patient = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for Dr. {self.doctor} about {self.patient}"
