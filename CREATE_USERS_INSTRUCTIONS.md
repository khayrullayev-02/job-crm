# How to Create Test Users and Get Token

## Method 1: Using Django Management Command (EASIEST)

\`\`\`bash
# Make sure you're in the virtual environment (venv)
# Run this command:
python manage.py create_test_users
\`\`\`

Output should be:
\`\`\`
✓ Director created: director1 / Director@123
✓ Manager created: manager1 / Manager@123
✓ Admin created: admin1 / Admin@123
✓ Teacher created: teacher1 / Teacher@123
✓ Student created: student1 / Student@123
\`\`\`

## Method 2: Using Python Script

\`\`\`bash
# Run the direct script:
python scripts/setup_users_direct.py
\`\`\`

## Method 3: Manual Django Shell

\`\`\`bash
# Open Django shell
python manage.py shell

# Then paste this:
\`\`\`

\`\`\`python
from django.contrib.auth.models import User
from crm_app.models import UserProfile

# Create Director
director_user = User.objects.create_user(
    username='director1',
    password='Director@123',
    email='director1@crm.com',
    first_name='Azizbek',
    last_name='Abdullaev'
)
UserProfile.objects.create(
    user=director_user,
    role='Director',
    phone='+998901234567',
    passport_number='AB1234567',
    birthday='1985-05-15'
)
print("Director created!")

# Create Teacher
teacher_user = User.objects.create_user(
    username='teacher1',
    password='Teacher@123',
    email='teacher1@crm.com',
    first_name='Nodira',
    last_name='Shodmonova'
)
UserProfile.objects.create(
    user=teacher_user,
    role='Teacher',
    phone='+998904567890',
    passport_number='AB4567890',
    birthday='1988-09-25'
)
print("Teacher created!")

# Create Student
student_user = User.objects.create_user(
    username='student1',
    password='Student@123',
    email='student1@crm.com',
    first_name='Ali',
    last_name='Rasulov'
)
UserProfile.objects.create(
    user=student_user,
    role='Student',
    phone='+998905678901',
    passport_number='AB5678901',
    birthday='2005-11-12'
)
print("Student created!")
\`\`\`

Then exit with `exit()`

---

## Step 2: Login and Get Token

Once users are created, you can login using any method:

### Using cURL:

\`\`\`bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "director1",
    "password": "Director@123"
  }'
\`\`\`

Response:
\`\`\`json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": 1,
  "role": "Director",
  "center_id": null
}
\`\`\`

### Using Swagger UI:

1. Go to http://127.0.0.1:8000/api/docs/
2. Find "POST /api/login/" endpoint
3. Click "Try it out"
4. Enter:
   \`\`\`json
   {
     "username": "director1",
     "password": "Director@123"
   }
   \`\`\`
5. Click "Execute"
6. Copy the token from response

### Using Postman:

1. Method: POST
2. URL: http://127.0.0.1:8000/api/login/
3. Headers: `Content-Type: application/json`
4. Body (raw):
   \`\`\`json
   {
     "username": "director1",
     "password": "Director@123"
   }
   \`\`\`
5. Send

---

## Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Director | director1 | Director@123 |
| Manager | manager1 | Manager@123 |
| Admin | admin1 | Admin@123 |
| Teacher | teacher1 | Teacher@123 |
| Student | student1 | Student@123 |

---

## Step 3: Use Token in API Requests

Once you have the token, use it in Authorization header:

\`\`\`bash
curl -X GET http://127.0.0.1:8000/api/centers/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
\`\`\`

In Swagger:
1. Click green "Authorize" button at top
2. Paste: `Bearer eyJ0eXAiOiJKV1QiLCJhbGc...`
3. Click "Authorize"
4. Now all endpoints will use this token

---

## Verify Users Were Created

In Django shell:
\`\`\`python
from django.contrib.auth.models import User

# Check all users
User.objects.all().values('id', 'username', 'email')

# Or specific user
User.objects.get(username='director1')
\`\`\`

Should show:
\`\`\`
<User: director1>
<User: manager1>
<User: admin1>
<User: teacher1>
<User: student1>
