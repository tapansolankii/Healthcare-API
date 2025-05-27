from django.contrib import admin
from .models import Doctor, Patient, HealthRecord, DoctorAnnotation

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'license_number')
    search_fields = ('user__username', 'user__email', 'specialization')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth')
    search_fields = ('user__username', 'user__email')
    filter_horizontal = ('assigned_doctors',)

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'patient__user__username')
    list_filter = ('created_at', 'updated_at')

@admin.register(DoctorAnnotation)
class DoctorAnnotationAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'health_record', 'created_at')
    search_fields = ('comment', 'doctor__user__username', 'health_record__title')
    list_filter = ('created_at',)
