# Healthcare API Documentation

## Project Overview
A Django REST Framework-based Healthcare API that manages doctor-patient relationships, health records, and medical annotations. The API provides secure endpoints for managing healthcare data with JWT authentication.

## Tech Stack
- **Backend Framework**: Django 5.0.2
- **API Framework**: Django REST Framework 3.14.0
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: 
  - Development: SQLite3
  - Production: PostgreSQL (Railway)
- **Deployment**: Railway

## Dependencies
```
Django==5.0.2
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
gunicorn==21.2.0
whitenoise==6.6.0
python-dotenv==1.0.1
dj-database-url==2.1.0
```

## Project Structure
```
health_records/
├── api/                    # Main application directory
│   ├── models.py          # Database models
│   ├── serializers.py     # Data serializers
│   ├── views.py           # API views
│   └── urls.py            # API endpoints
├── health_records/        # Project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI configuration
├── manage.py              # Django management script
├── requirements.txt       # Project dependencies
├── Procfile              # Railway deployment configuration
└── railway.toml          # Railway configuration
```

## Models
1. **Doctor**
   - User (OneToOne with Django User)
   - Specialization
   - License Number
   - Patients (ManyToMany with Patient)

2. **Patient**
   - User (OneToOne with Django User)
   - Date of Birth
   - Gender
   - Blood Group
   - Assigned Doctors (ManyToMany with Doctor)

3. **HealthRecord**
   - Patient (ForeignKey to Patient)
   - Diagnosis
   - Prescription
   - Notes
   - Record Date
   - Created At
   - Updated At

4. **DoctorAnnotation**
   - Health Record (ForeignKey to HealthRecord)
   - Doctor (ForeignKey to Doctor)
   - Comment
   - Created At

5. **DoctorNotification**
   - Doctor (ForeignKey to Doctor)
   - Patient (ForeignKey to Patient)
   - Is New Patient
   - Is Read
   - Created At

## API Endpoints

### Authentication
- `POST /api/token/` - Get JWT tokens
- `POST /api/token/refresh/` - Refresh JWT token

### Doctors
- `GET /api/doctors/` - List all doctors
- `POST /api/doctors/` - Create new doctor
- `GET /api/doctors/{id}/` - Get doctor details
- `GET /api/doctors/{id}/patients/` - Get doctor's patients
- `GET /api/doctors/{id}/notifications/` - Get doctor's notifications
- `POST /api/doctors/{id}/mark_notification_read/` - Mark notification as read
- `POST /api/doctors/{id}/annotate_record/` - Add annotation to health record

### Patients
- `GET /api/patients/` - List all patients
- `POST /api/patients/` - Create new patient
- `GET /api/patients/{id}/` - Get patient details
- `GET /api/patients/{id}/records/` - Get patient's health records

### Health Records
- `GET /api/health-records/` - List all health records
- `POST /api/health-records/` - Create new health record
- `GET /api/health-records/{id}/` - Get health record details

### Health Check
- `GET /api/health/` - API health check endpoint

## Security Features
- JWT Authentication
- CORS Configuration
- SSL/HTTPS in Production
- Secure Password Validation
- CSRF Protection
- XSS Protection
- HSTS Enabled

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Run development server:
   ```bash
   python manage.py runserver
   ```

## Production Deployment (Railway)
1. Database: PostgreSQL on Railway



## Future Improvements in mind
1. Add email notifications for doctor (can integrate Gauth for bulk or update email project in my porfolio)

