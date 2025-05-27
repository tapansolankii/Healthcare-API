# API Reference Documentation

## Base URL
```
https://health-api-production-8414.up.railway.app
```

## Authentication

### Get JWT Tokens
```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Response**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Refresh Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

## Doctor Endpoints

### List Doctors
```http
GET /api/doctors/
Authorization: Bearer your_access_token
```

**Response**
```json
[
    {
        "id": 1,
        "user": {
            "username": "dr.smith",
            "email": "dr.smith@hospital.com"
        },
        "specialization": "Cardiology",
        "license_number": "DOC123456",
        "patients": [1, 2, 3]
    }
]
```

### Create Doctor
```http
POST /api/doctors/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "user": {
        "username": "dr.smith",
        "email": "dr.smith@hospital.com",
        "password": "secure_password"
    },
    "specialization": "Cardiology",
    "license_number": "DOC123456"
}
```

### Get Doctor's Patients
```http
GET /api/doctors/{doctor_id}/patients/
Authorization: Bearer your_access_token
```

### Get Doctor's Notifications
```http
GET /api/doctors/{doctor_id}/notifications/
Authorization: Bearer your_access_token
```

### Add Annotation to Health Record
```http
POST /api/doctors/{doctor_id}/annotate_record/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "record_id": 1,
    "comment": "Patient showing improvement"
}
```

## Patient Endpoints

### List Patients
```http
GET /api/patients/
Authorization: Bearer your_access_token
```

### Create Patient
```http
POST /api/patients/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "user": {
        "username": "john.doe",
        "email": "john.doe@email.com",
        "password": "secure_password"
    },
    "date_of_birth": "1990-01-01",
    "gender": "M",
    "blood_group": "O+",
    "assigned_doctors": [1]
}
```

### Get Patient's Health Records
```http
GET /api/patients/{patient_id}/records/
Authorization: Bearer your_access_token
```

## Health Records

### List Health Records
```http
GET /api/health-records/
Authorization: Bearer your_access_token
```

### Create Health Record
```http
POST /api/health-records/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "patient": 1,
    "diagnosis": "Hypertension",
    "prescription": "Amlodipine 5mg daily",
    "notes": "Regular checkup required",
    "record_date": "2024-03-20"
}
```

## Error Responses

### 400 Bad Request
```json
{
    "error": "Invalid input data",
    "details": {
        "field_name": ["Error message"]
    }
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

## Rate Limiting
- 100 requests per minute per IP
- 1000 requests per hour per user

## Best Practices
1. Always include the Authorization header
2. Handle token expiration (401 responses)
3. Use appropriate HTTP methods
4. Validate input data
5. Handle errors gracefully

## Testing the API
1. Use Postman or similar tool
2. Set up environment variables for:
   - `base_url`
   - `access_token`
3. Create a collection with all endpoints
4. Use the health check endpoint to verify API status

## Example Postman Setup
1. Create a new environment
2. Add variables:
   - `base_url`: https://health-api-production-8414.up.railway.app
   - `access_token`: (empty initially)
3. Create a login request that sets the token
4. Use the token in subsequent requests

## Common Use Cases

### Doctor Workflow
1. Login to get JWT token
2. View assigned patients
3. Check patient records
4. Add annotations
5. View notifications

### Patient Workflow
1. Login to get JWT token
2. View own health records
3. View assigned doctors
4. Check notifications

### Admin Workflow
1. Login to admin interface
2. Manage users
3. Assign doctors to patients
4. Monitor system 