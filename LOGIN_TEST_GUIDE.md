# Login and Authentication Test Guide

## Step 1: Create Test Users

Run this command to create test users for each role:

\`\`\`bash
python manage.py shell < scripts/create_test_users.py
\`\`\`

**Output should look like:**
\`\`\`
Creating test users for all roles...

✓ Director created: director1 / Director@123
✓ Manager created: manager1 / Manager@123
✓ Admin created: admin1 / Admin@123
✓ Teacher created: teacher1 / Teacher@123
✓ Student created: student1 / Student@123

==================================================
ALL TEST USERS CREATED SUCCESSFULLY!
==================================================

Login credentials:
├─ Director  : director1 / Director@123
├─ Manager   : manager1 / Manager@123
├─ Admin     : admin1 / Admin@123
├─ Teacher   : teacher1 / Teacher@123
└─ Student   : student1 / Student@123
\`\`\`

---

## Step 2: Test Login with Each Role

### Login Endpoint
\`\`\`
POST http://127.0.0.1:8000/api/login/
\`\`\`

### Request Headers
\`\`\`
Content-Type: application/json
\`\`\`

---

## Test Cases

### 1. Director Login

**Request:**
\`\`\`bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "director1",
    "password": "Director@123"
  }'
\`\`\`

**Expected Response:**
\`\`\`json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": 1,
  "username": "director1",
  "role": "Director",
  "center_id": null
}
\`\`\`

**Status Code:** `200 OK`

---

### 2. Manager Login

**Request:**
\`\`\`bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "manager1",
    "password": "Manager@123"
  }'
\`\`\`

**Expected Response:**
\`\`\`json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": 2,
  "username": "manager1",
  "role": "Manager",
  "center_id": null
}
\`\`\`

**Status Code:** `200 OK`

---

### 3. Admin Login

**Request:**
\`\`\`bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin1",
    "password": "Admin@123"
  }'
\`\`\`

**Expected Response:**
\`\`\`json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": 3,
  "username": "admin1",
  "role": "Admin",
  "center_id": null
}
\`\`\`

**Status Code:** `200 OK`

---

### 4. Teacher Login

**Request:**
\`\`\`bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "teacher1",
    "password": "Teacher@123"
  }'
\`\`\`

**Expected Response:**
\`\`\`json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": 4,
  "username": "teacher1",
  "role": "Teacher",
  "center_id": null
}
\`\`\`

**Status Code:** `200 OK`

---

### 5. Student Login

**Request:**
\`\`\`bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "Student@123"
  }'
\`\`\`

**Expected Response:**
\`\`\`json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": 5,
  "username": "student1",
  "role": "Student",
  "center_id": null
}
\`\`\`

**Status Code:** `200 OK`

---

## Step 3: Use Token to Access Protected Endpoints

Once you have the token, use it to access protected endpoints by adding the Authorization header:

\`\`\`bash
curl -X GET http://127.0.0.1:8000/api/centers/ \
  -H "Authorization: Bearer <YOUR_TOKEN_HERE>"
\`\`\`

**Example with real token:**
\`\`\`bash
curl -X GET http://127.0.0.1:8000/api/centers/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
\`\`\`

---

## Error Handling

### Wrong Password

**Request:**
\`\`\`bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "director1",
    "password": "WrongPassword"
  }'
\`\`\`

**Response:**
\`\`\`json
{
  "error": "Invalid credentials"
}
\`\`\`

**Status Code:** `401 Unauthorized`

---

### Non-existent User

**Request:**
\`\`\`bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nonexistent",
    "password": "Password123"
  }'
\`\`\`

**Response:**
\`\`\`json
{
  "error": "Invalid credentials"
}
\`\`\`

**Status Code:** `401 Unauthorized`

---

### Missing Required Fields

**Request:**
\`\`\`bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "director1"
  }'
\`\`\`

**Response:**
\`\`\`json
{
  "password": ["This field is required."]
}
\`\`\`

**Status Code:** `400 Bad Request`

---

## Frontend Implementation Example

### Redirect to Dashboard Based on Role

After successful login, redirect user to their role-specific dashboard:

\`\`\`javascript
const loginResponse = {
  "token": "...",
  "role": "Director",
  "user_id": 1,
  "center_id": 1
};

// Save token to localStorage
localStorage.setItem('auth_token', loginResponse.token);

// Redirect based on role
const roleRedirects = {
  'Director': '/dashboard/director',
  'Manager': '/dashboard/manager',
  'Admin': '/dashboard/admin',
  'Teacher': '/dashboard/teacher',
  'Student': '/dashboard/student'
};

window.location.href = roleRedirects[loginResponse.role];
\`\`\`

---

## Troubleshooting

### Issue: "Invalid credentials" for correct password

**Solutions:**
1. Verify the password is exactly as created (check case sensitivity)
2. Re-create the user: `python manage.py shell < scripts/create_test_users.py`
3. Check database is properly migrated: `python manage.py migrate`

### Issue: 401 Unauthorized when using token

**Solutions:**
1. Ensure token is included in Authorization header: `Authorization: Bearer <token>`
2. Token might be expired - get a new one by logging in again
3. Check token format - should start with `eyJ`

### Issue: Cannot find API endpoint

**Solutions:**
1. Ensure Django server is running: `python manage.py runserver`
2. Check URL is correct: `http://127.0.0.1:8000/api/login/`
3. Check Django URLs are properly configured

---

## Complete Workflow Example

\`\`\`bash
#!/bin/bash

# 1. Create test users
echo "Creating test users..."
python manage.py shell < scripts/create_test_users.py

# 2. Login as director
echo -e "\nLogging in as director..."
LOGIN_RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "director1", "password": "Director@123"}')

echo "Login Response:"
echo $LOGIN_RESPONSE | jq '.'

# 3. Extract token
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.token')
echo -e "\nExtracted Token:"
echo $TOKEN

# 4. Test protected endpoint
echo -e "\nFetching centers with token..."
curl -s -X GET http://127.0.0.1:8000/api/centers/ \
  -H "Authorization: Bearer $TOKEN" | jq '.'
\`\`\`

Save this as `test_workflow.sh`, make it executable, and run:
\`\`\`bash
chmod +x test_workflow.sh
./test_workflow.sh
\`\`\`

---

## Summary

✓ Create test users with `create_test_users.py`  
✓ Login using POST `/api/login/` with username and password  
✓ Receive JWT token in response  
✓ Use token in Authorization header for protected endpoints  
✓ Token includes user role for frontend routing  

All test users are now ready for use!
