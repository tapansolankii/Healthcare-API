# API Testing Guide with cURL and Postman Examples

## Base URL
```
https://health-api-production-8414.up.railway.app
```

## 1. Authentication

### Get JWT Tokens
```bash
# cURL
curl -X POST https://health-api-production-8414.up.railway.app/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'

# Postman
POST {{base_url}}/api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Expected Response (200 OK)**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Refresh Token
```bash
# cURL
curl -X POST https://health-api-production-8414.up.railway.app/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "your_refresh_token"
  }'

# Postman
POST {{base_url}}/api/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

## 2. Doctor Endpoints

### List All Doctors
```bash
# cURL
curl -X GET https://health-api-production-8414.up.railway.app/api/doctors/ \
  -H "Authorization: Bearer your_access_token"

# Postman
GET {{base_url}}/api/doctors/
Authorization: Bearer {{access_token}}
```

**Expected Response (200 OK)**
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

### Create New Doctor
```bash
# cURL
curl -X POST https://health-api-production-8414.up.railway.app/api/doctors/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "user": {
        "username": "dr.johnson",
        "email": "dr.johnson@hospital.com",
        "password": "secure_password123"
    },
    "specialization": "Neurology",
    "license_number": "DOC789012"
  }'

# Postman
POST {{base_url}}/api/doctors/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "user": {
        "username": "dr.johnson",
        "email": "dr.johnson@hospital.com",
        "password": "secure_password123"
    },
    "specialization": "Neurology",
    "license_number": "DOC789012"
}
```

### Get Doctor's Patients
```bash
# cURL
curl -X GET https://health-api-production-8414.up.railway.app/api/doctors/1/patients/ \
  -H "Authorization: Bearer your_access_token"

# Postman
GET {{base_url}}/api/doctors/1/patients/
Authorization: Bearer {{access_token}}
```

## 3. Patient Endpoints

### List All Patients
```bash
# cURL
curl -X GET https://health-api-production-8414.up.railway.app/api/patients/ \
  -H "Authorization: Bearer your_access_token"

# Postman
GET {{base_url}}/api/patients/
Authorization: Bearer {{access_token}}
```

### Create New Patient
```bash
# cURL
curl -X POST https://health-api-production-8414.up.railway.app/api/patients/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "user": {
        "username": "john.doe",
        "email": "john.doe@email.com",
        "password": "patient_password123"
    },
    "date_of_birth": "1990-01-01",
    "gender": "M",
    "blood_group": "O+",
    "assigned_doctors": [1]
  }'

# Postman
POST {{base_url}}/api/patients/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "user": {
        "username": "john.doe",
        "email": "john.doe@email.com",
        "password": "patient_password123"
    },
    "date_of_birth": "1990-01-01",
    "gender": "M",
    "blood_group": "O+",
    "assigned_doctors": [1]
}
```

## 4. Health Records

### Create Health Record
```bash
# cURL
curl -X POST https://health-api-production-8414.up.railway.app/api/health-records/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "patient": 1,
    "diagnosis": "Hypertension Stage 1",
    "prescription": "Amlodipine 5mg daily",
    "notes": "Regular checkup required",
    "record_date": "2024-03-20"
  }'

# Postman
POST {{base_url}}/api/health-records/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "patient": 1,
    "diagnosis": "Hypertension Stage 1",
    "prescription": "Amlodipine 5mg daily",
    "notes": "Regular checkup required",
    "record_date": "2024-03-20"
}
```

### Get Patient's Health Records
```bash
# cURL
curl -X GET https://health-api-production-8414.up.railway.app/api/patients/1/records/ \
  -H "Authorization: Bearer your_access_token"

# Postman
GET {{base_url}}/api/patients/1/records/
Authorization: Bearer {{access_token}}
```

## 5. Doctor Annotations

### Add Annotation to Health Record
```bash
# cURL
curl -X POST https://health-api-production-8414.up.railway.app/api/doctors/1/annotate_record/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "record_id": 1,
    "comment": "Patient showing improvement in blood pressure"
  }'

# Postman
POST {{base_url}}/api/doctors/1/annotate_record/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "record_id": 1,
    "comment": "Patient showing improvement in blood pressure"
}
```

## Postman Environment Setup

1. Create a new environment in Postman
2. Add these variables:
   ```
   base_url: https://health-api-production-8414.up.railway.app
   access_token: (leave empty, will be set after login)
   refresh_token: (leave empty, will be set after login)
   ```

3. Create a login request that automatically sets the tokens:
   ```javascript
   // In the Tests tab of your login request
   var jsonData = pm.response.json();
   pm.environment.set("access_token", jsonData.access);
   pm.environment.set("refresh_token", jsonData.refresh);
   ```

## Common Error Responses

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

### 400 Bad Request
```json
{
    "error": "Invalid input data",
    "details": {
        "field_name": ["Error message"]
    }
}
```

## Testing Tips

1. **Token Management**
   - Always store tokens in environment variables
   - Use token refresh when access token expires
   - Test with invalid tokens to verify security

2. **Data Validation**
   - Test with invalid data formats
   - Test required fields
   - Test unique constraints (e.g., license numbers)

3. **Permissions**
   - Test with different user roles
   - Verify access restrictions
   - Test cross-user data access

4. **Rate Limiting**
   - Monitor response headers for rate limit info
   - Test with multiple rapid requests
   - Handle 429 Too Many Requests responses 