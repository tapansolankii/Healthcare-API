# Database Models Documentation

## Overview
The Healthcare API uses Django's ORM with the following models to manage healthcare data. All models include timestamps for auditing and tracking.

## User Model (Django Auth)
```python
from django.contrib.auth.models import User

# Fields:
- username: CharField (unique)
- email: EmailField
- password: CharField (hashed)
- is_active: BooleanField
- is_staff: BooleanField
- date_joined: DateTimeField
```

## Doctor Model
```python
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    patients = models.ManyToManyField('Patient', related_name='doctors')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
```

### Relationships
- One-to-One with User
- Many-to-Many with Patient
- One-to-Many with DoctorAnnotation
- One-to-Many with DoctorNotification

### Fields
- `user`: OneToOneField to User model
- `specialization`: Doctor's medical specialty
- `license_number`: Unique medical license number
- `patients`: ManyToManyField to Patient model
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

## Patient Model
```python
class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    assigned_doctors = models.ManyToManyField(Doctor, related_name='assigned_patients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
```

### Relationships
- One-to-One with User
- Many-to-Many with Doctor
- One-to-Many with HealthRecord

### Fields
- `user`: OneToOneField to User model
- `date_of_birth`: Patient's birth date
- `gender`: Patient's gender (M/F/O)
- `blood_group`: Patient's blood type
- `assigned_doctors`: ManyToManyField to Doctor model
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

## HealthRecord Model
```python
class HealthRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='health_records')
    diagnosis = models.TextField()
    prescription = models.TextField()
    notes = models.TextField(blank=True)
    record_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-record_date', '-created_at']
```

### Relationships
- Many-to-One with Patient
- One-to-Many with DoctorAnnotation

### Fields
- `patient`: ForeignKey to Patient model
- `diagnosis`: Medical diagnosis
- `prescription`: Prescribed medication/treatment
- `notes`: Additional medical notes
- `record_date`: Date of the medical record
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

## DoctorAnnotation Model
```python
class DoctorAnnotation(models.Model):
    health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE, related_name='annotations')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='annotations')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
```

### Relationships
- Many-to-One with HealthRecord
- Many-to-One with Doctor

### Fields
- `health_record`: ForeignKey to HealthRecord model
- `doctor`: ForeignKey to Doctor model
- `comment`: Doctor's annotation/comment
- `created_at`: Timestamp of creation

## DoctorNotification Model
```python
class DoctorNotification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='notifications')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_notifications')
    is_new_patient = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
```

### Relationships
- Many-to-One with Doctor
- Many-to-One with Patient

### Fields
- `doctor`: ForeignKey to Doctor model
- `patient`: ForeignKey to Patient model
- `is_new_patient`: Flag for new patient notifications
- `is_read`: Flag for read status
- `created_at`: Timestamp of creation

## Database Indexes
```python
# Doctor Model
indexes = [
    models.Index(fields=['license_number']),
    models.Index(fields=['specialization'])
]

# Patient Model
indexes = [
    models.Index(fields=['date_of_birth']),
    models.Index(fields=['blood_group'])
]

# HealthRecord Model
indexes = [
    models.Index(fields=['record_date']),
    models.Index(fields=['patient', 'record_date'])
]

# DoctorAnnotation Model
indexes = [
    models.Index(fields=['health_record', 'created_at'])
]

# DoctorNotification Model
indexes = [
    models.Index(fields=['doctor', 'is_read']),
    models.Index(fields=['created_at'])
]
```

## Model Methods

### Doctor Model
```python
def get_patient_count(self):
    return self.patients.count()

def get_unread_notifications(self):
    return self.notifications.filter(is_read=False)

def get_recent_annotations(self, limit=5):
    return self.annotations.all()[:limit]
```

### Patient Model
```python
def get_age(self):
    return (date.today() - self.date_of_birth).days // 365

def get_doctor_count(self):
    return self.assigned_doctors.count()

def get_recent_records(self, limit=5):
    return self.health_records.all()[:limit]
```

### HealthRecord Model
```python
def get_annotations_count(self):
    return self.annotations.count()

def get_latest_annotation(self):
    return self.annotations.first()
```

## Data Validation
- License numbers must be unique
- Email addresses must be valid
- Dates must be in the past
- Blood groups must be valid choices
- Gender must be valid choice

## Security Considerations
1. Sensitive data is never exposed in API responses
2. Passwords are hashed using Django's auth system
3. All models have proper access controls
4. Audit trails through created_at/updated_at fields 