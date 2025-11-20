# API Documentation

Complete API documentation for the Chemical Equipment Parameter Visualizer REST API.

## Base URL

```
http://localhost:8000/api
```

For production, replace with your actual domain.

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

## Endpoints

### 1. Health Check

Check if the API is running.

**Endpoint:** `GET /health/`

**Authentication:** Not required

**Response:**
```json
{
  "status": "ok"
}
```

**Status Codes:**
- `200 OK`: API is healthy

---

### 2. User Registration

Register a new user account.

**Endpoint:** `POST /auth/register/`

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password123"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Status Codes:**
- `201 Created`: User successfully registered
- `400 Bad Request`: Invalid data or username already exists

**Validation Rules:**
- Username must be unique
- Password minimum length: 8 characters
- Email must be valid format

---

### 3. User Login

Authenticate and receive JWT tokens.

**Endpoint:** `POST /auth/login/`

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "secure_password123"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Status Codes:**
- `200 OK`: Login successful
- `401 Unauthorized`: Invalid credentials

**Token Information:**
- Access token expires in 5 hours
- Refresh token expires in 24 hours

---

### 4. Upload CSV

Upload and process a CSV file with chemical equipment data.

**Endpoint:** `POST /upload/`

**Authentication:** Required

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with `file` field containing the CSV file

**CSV Format Requirements:**

Required columns:
- Equipment Name (string)
- Type (string)
- Flowrate (numeric)
- Pressure (numeric)
- Temperature (numeric)

Example CSV:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-001,Reactor,150.5,25.3,180.2
Pump-001,Pump,200.0,50.0,75.5
```

**Response:**
```json
{
  "id": 1,
  "message": "File uploaded successfully",
  "summary": {
    "total_equipment": 20,
    "average_flowrate": 148.52,
    "average_pressure": 32.45,
    "average_temperature": 112.30,
    "type_distribution": {
      "Reactor": 5,
      "Pump": 8,
      "Heat Exchanger": 7
    },
    "min_flowrate": 100.0,
    "max_flowrate": 210.5,
    "min_pressure": 5.0,
    "max_pressure": 105.0,
    "min_temperature": 25.0,
    "max_temperature": 205.0
  }
}
```

**Status Codes:**
- `201 Created`: File uploaded and processed successfully
- `400 Bad Request`: Invalid file, missing columns, or validation error
- `401 Unauthorized`: Missing or invalid token

**Constraints:**
- Maximum file size: 5 MB
- Only CSV files allowed
- File must contain required columns

**Business Logic:**
- System automatically maintains only last 5 uploads per user
- Older datasets are automatically deleted with their files

---

### 5. Get Dataset Summary

Retrieve detailed summary and data for a specific dataset.

**Endpoint:** `GET /summary/<dataset_id>/`

**Authentication:** Required

**Path Parameters:**
- `dataset_id` (integer): The ID of the dataset

**Response:**
```json
{
  "id": 1,
  "uploaded_at": "2024-11-16T10:30:00Z",
  "summary": {
    "total_equipment": 20,
    "average_flowrate": 148.52,
    "average_pressure": 32.45,
    "average_temperature": 112.30,
    "type_distribution": {
      "Reactor": 5,
      "Pump": 8,
      "Heat Exchanger": 7
    },
    "min_flowrate": 100.0,
    "max_flowrate": 210.5,
    "min_pressure": 5.0,
    "max_pressure": 105.0,
    "min_temperature": 25.0,
    "max_temperature": 205.0
  },
  "data": [
    {
      "Equipment Name": "Reactor-001",
      "Type": "Reactor",
      "Flowrate": 150.5,
      "Pressure": 25.3,
      "Temperature": 180.2
    },
    {
      "Equipment Name": "Pump-001",
      "Type": "Pump",
      "Flowrate": 200.0,
      "Pressure": 50.0,
      "Temperature": 75.5
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Dataset found and returned
- `404 Not Found`: Dataset doesn't exist or doesn't belong to user
- `401 Unauthorized`: Missing or invalid token

---

### 6. Get Upload History

Get the last 5 uploaded datasets for the authenticated user.

**Endpoint:** `GET /history/`

**Authentication:** Required

**Response:**
```json
[
  {
    "id": 5,
    "file_path": "/path/to/user_20241116_103000.csv",
    "uploaded_at": "2024-11-16T10:30:00Z",
    "summary_json": {
      "total_equipment": 20,
      "average_flowrate": 148.52,
      "average_pressure": 32.45,
      "average_temperature": 112.30,
      "type_distribution": {
        "Reactor": 5,
        "Pump": 8
      }
    }
  },
  {
    "id": 4,
    "file_path": "/path/to/user_20241116_093000.csv",
    "uploaded_at": "2024-11-16T09:30:00Z",
    "summary_json": {
      "total_equipment": 15,
      "average_flowrate": 135.20,
      "average_pressure": 28.30,
      "average_temperature": 105.50,
      "type_distribution": {
        "Reactor": 3,
        "Pump": 6,
        "Tank": 6
      }
    }
  }
]
```

**Status Codes:**
- `200 OK`: History retrieved successfully
- `401 Unauthorized`: Missing or invalid token

**Notes:**
- Returns empty array if no datasets exist
- Maximum 5 datasets per user
- Ordered by upload date (newest first)

---

### 7. Generate PDF Report

Generate and download a PDF report for a specific dataset.

**Endpoint:** `GET /report/<dataset_id>/`

**Authentication:** Required

**Path Parameters:**
- `dataset_id` (integer): The ID of the dataset

**Response:**
- Content-Type: `application/pdf`
- Binary PDF file download

**Report Contents:**
1. Report header with timestamp
2. Dataset information
3. Summary statistics table
4. Equipment type distribution table
5. Range values (min/max) for all parameters

**Status Codes:**
- `200 OK`: PDF generated and returned
- `404 Not Found`: Dataset doesn't exist or doesn't belong to user
- `401 Unauthorized`: Missing or invalid token

**Example using curl:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:8000/api/report/1/ \
     --output report.pdf
```

---

## Error Responses

All endpoints may return the following error format:

```json
{
  "error": "Description of the error"
}
```

### Common Error Codes

- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid authentication token
- `403 Forbidden`: Authenticated but not authorized for this resource
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error (check logs)

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider implementing rate limiting based on:
- IP address
- User account
- Token

---

## CORS

Development configuration allows all origins. For production:

```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

---

## Testing Examples

### Using curl

**Register:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@test.com","password":"testpass123"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

**Upload CSV:**
```bash
curl -X POST http://localhost:8000/api/upload/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@sample_data/sample_equipment.csv"
```

**Get History:**
```bash
curl http://localhost:8000/api/history/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Using Python requests

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api"

# Register
response = requests.post(
    f"{BASE_URL}/auth/register/",
    json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "testpass123"
    }
)
print(response.json())

# Login
response = requests.post(
    f"{BASE_URL}/auth/login/",
    json={
        "username": "testuser",
        "password": "testpass123"
    }
)
token = response.json()["access"]

# Upload CSV
with open("sample_data/sample_equipment.csv", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/upload/",
        files={"file": f},
        headers={"Authorization": f"Bearer {token}"}
    )
print(response.json())

# Get History
response = requests.get(
    f"{BASE_URL}/history/",
    headers={"Authorization": f"Bearer {token}"}
)
print(response.json())
```

---

## WebSocket Support

Currently not implemented. Future versions may include WebSocket support for:
- Real-time upload progress
- Live data updates
- Collaborative features

---

## Versioning

Current version: v1 (implicit)

Future API versions will be prefixed:
- `/api/v1/...`
- `/api/v2/...`

---

## Support

For API issues:
1. Check response error messages
2. Verify authentication token
3. Validate request format
4. Check server logs for detailed errors

---

Last Updated: November 16, 2024

