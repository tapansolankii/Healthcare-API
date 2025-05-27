```mermaid
graph TD
    subgraph "Authentication Flow"
        A[Client] -->|1. Login Request| B[/api/token/]
        B -->|2. JWT Tokens| A
        A -->|3. Access Token| C[Protected Endpoints]
    end

    subgraph "Doctor API Flow"
        C -->|4. GET /api/doctors/| D[Doctor List]
        C -->|5. POST /api/doctors/| E[Create Doctor]
        C -->|6. GET /api/doctors/{id}/patients/| F[Doctor's Patients]
        C -->|7. GET /api/doctors/{id}/notifications/| G[Doctor's Notifications]
        C -->|8. POST /api/doctors/{id}/annotate_record/| H[Add Annotation]
    end

    subgraph "Patient API Flow"
        C -->|9. GET /api/patients/| I[Patient List]
        C -->|10. POST /api/patients/| J[Create Patient]
        C -->|11. GET /api/patients/{id}/records/| K[Patient Records]
    end

    subgraph "Health Records Flow"
        C -->|12. GET /api/health-records/| L[Health Records List]
        C -->|13. POST /api/health-records/| M[Create Health Record]
    end

    subgraph "Test Cases Structure"
        N[Authentication Tests]
        N -->|Test Case 1| O[Login Success]
        N -->|Test Case 2| P[Login Failure]
        N -->|Test Case 3| Q[Token Refresh]

        R[Doctor API Tests]
        R -->|Test Case 4| S[Create Doctor]
        R -->|Test Case 5| T[List Doctors]
        R -->|Test Case 6| U[Get Doctor's Patients]
        R -->|Test Case 7| V[Add Annotation]

        W[Patient API Tests]
        W -->|Test Case 8| X[Create Patient]
        W -->|Test Case 9| Y[List Patients]
        W -->|Test Case 10| Z[Get Patient Records]

        AA[Health Records Tests]
        AA -->|Test Case 11| AB[Create Record]
        AA -->|Test Case 12| AC[List Records]
        AA -->|Test Case 13| AD[Update Record]
    end

    subgraph "Error Handling Tests"
        AE[400 Bad Request] -->|Invalid Data| AF[Validation Error]
        AG[401 Unauthorized] -->|No Token| AH[Auth Error]
        AI[403 Forbidden] -->|Invalid Permissions| AJ[Permission Error]
        AK[404 Not Found] -->|Invalid Resource| AL[Resource Error]
    end
```

# Test Cases Structure and API Flow

## Authentication Flow
1. Client sends login request to `/api/token/`
2. Server validates credentials and returns JWT tokens
3. Client uses access token for subsequent requests

## Doctor API Flow
1. List Doctors (`GET /api/doctors/`)
   - Returns all doctors with their details
   - Requires authentication
   - Test cases: permissions, pagination, filtering

2. Create Doctor (`POST /api/doctors/`)
   - Creates new doctor with user account
   - Test cases: validation, duplicate license, required fields

3. Doctor's Patients (`GET /api/doctors/{id}/patients/`)
   - Returns list of assigned patients
   - Test cases: empty list, invalid doctor ID

4. Doctor's Notifications (`GET /api/doctors/{id}/notifications/`)
   - Returns unread notifications
   - Test cases: notification types, read status

5. Add Annotation (`POST /api/doctors/{id}/annotate_record/`)
   - Adds comment to health record
   - Test cases: record existence, permission

## Patient API Flow
1. List Patients (`GET /api/patients/`)
   - Returns all patients
   - Test cases: filtering, search, pagination

2. Create Patient (`POST /api/patients/`)
   - Creates new patient with user account
   - Test cases: validation, required fields

3. Patient Records (`GET /api/patients/{id}/records/`)
   - Returns patient's health records
   - Test cases: date range, sorting

## Health Records Flow
1. List Records (`GET /api/health-records/`)
   - Returns all health records
   - Test cases: filtering, date range

2. Create Record (`POST /api/health-records/`)
   - Creates new health record
   - Test cases: validation, doctor assignment

## Error Handling Tests
1. 400 Bad Request
   - Invalid input data
   - Missing required fields
   - Invalid data types

2. 401 Unauthorized
   - Missing token
   - Invalid token
   - Expired token

3. 403 Forbidden
   - Invalid permissions
   - Unauthorized access

4. 404 Not Found
   - Invalid resource ID
   - Non-existent records

## Test Case Implementation Example
```python
# Example test case for creating a doctor
def test_create_doctor(self):
    # Test data
    data = {
        "user": {
            "username": "dr.smith",
            "email": "dr.smith@hospital.com",
            "password": "secure_password"
        },
        "specialization": "Cardiology",
        "license_number": "DOC123456"
    }
    
    # Make request
    response = self.client.post(
        '/api/doctors/',
        data=json.dumps(data),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
    )
    
    # Assertions
    self.assertEqual(response.status_code, 201)
    self.assertEqual(Doctor.objects.count(), 1)
    self.assertEqual(Doctor.objects.get().license_number, "DOC123456")
``` 