# Final Setup Checklist - Get Token and Login

## Pre-Requirements

- Python 3.8+
- Django 4.0+
- PostgreSQL running (or SQLite)
- Virtual environment activated

---

## STEP 1: Database Setup

\`\`\`bash
# Run migrations
python manage.py migrate
\`\`\`

**Expected output:**
\`\`\`
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, crm_app
Running migrations:
  Applying contenttypes.0001_initial...
  ...
\`\`\`

---

## STEP 2: Create Test Users

**Option A - Management Command (RECOMMENDED):**
\`\`\`bash
python manage.py create_test_users
\`\`\`

**Option B - Direct Script:**
\`\`\`bash
python scripts/setup_users_direct.py
\`\`\`

**Option C - Manual Django Shell:**
\`\`\`bash
python manage.py shell < scripts/create_test_users.py
\`\`\`

**Expected output:**
\`\`\`
✓ Director created: director1 / Director@123
✓ Manager created: manager1 / Manager@123
✓ Admin created: admin1 / Admin@123
✓ Teacher created: teacher1 / Teacher@123
✓ Student created: student1 / Student@123
\`\`\`

---

## STEP 3: Start Server

\`\`\`bash
python manage.py runserver
\`\`\`

**Expected output:**
\`\`\`
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
\`\`\`

---

## STEP 4: Test Login

### Using Swagger UI:

1. Open: http://127.0.0.1:8000/api/docs/
2. Find endpoint: "POST /api/login/"
3. Click "Try it out"
4. Enter request body:
   \`\`\`json
   {
     "username": "director1",
     "password": "Director@123"
   }
   \`\`\`
5. Click "Execute"

**Expected response:**
\`\`\`json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": 1,
  "role": "Director",
  "center_id": null
}
\`\`\`

### Using cURL:

\`\`\`bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"director1","password":"Director@123"}'
\`\`\`

### Using Postman:

- **Method:** POST
- **URL:** http://127.0.0.1:8000/api/login/
- **Body:** 
  \`\`\`json
  {
    "username": "director1",
    "password": "Director@123"
  }
  \`\`\`

---

## STEP 5: Use Token in Requests

Copy the token from response and use it:

\`\`\`bash
curl -X GET http://127.0.0.1:8000/api/centers/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
\`\`\`

In Swagger: Click green "Authorize" button, paste token with "Bearer " prefix

---

## All Test Users Ready

| Role | Username | Password | Login |
|------|----------|----------|-------|
| Director | director1 | Director@123 | ✓ |
| Manager | manager1 | Manager@123 | ✓ |
| Admin | admin1 | Admin@123 | ✓ |
| Teacher | teacher1 | Teacher@123 | ✓ |
| Student | student1 | Student@123 | ✓ |

---

## Next Steps

- All 50+ API endpoints are ready in Swagger UI
- Use token for all authenticated requests
- Frontend can redirect to dashboard based on `role` field
- See TOKEN_AND_FRONTEND_INTEGRATION.md for frontend examples

---

## Troubleshooting

See `LOGIN_TROUBLESHOOTING.md` for common issues and solutions

---

## File References

- Management Command: `crm_app/management/commands/create_test_users.py`
- Direct Script: `scripts/setup_users_direct.py`
- Instructions: `CREATE_USERS_INSTRUCTIONS.md`
- Frontend Integration: `TOKEN_AND_FRONTEND_INTEGRATION.md`
- Troubleshooting: `LOGIN_TROUBLESHOOTING.md`
