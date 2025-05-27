# Health Record API

A Django REST Framework API for managing health records between patients and doctors.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- POST /api/token/ - Get JWT token
- POST /api/token/refresh/ - Refresh JWT token

### Patient Endpoints
- POST /api/patients/register/ - Register new patient
- GET /api/patients/records/ - View own health records
- POST /api/patients/records/ - Create new health record
- PUT /api/patients/records/{id}/ - Update health record

### Doctor Endpoints
- POST /api/doctors/register/ - Register new doctor
- GET /api/doctors/patients/ - View assigned patients
- GET /api/doctors/patients/{id}/records/ - View patient records
- POST /api/doctors/patients/{id}/records/{record_id}/annotate/ - Add annotation to record 