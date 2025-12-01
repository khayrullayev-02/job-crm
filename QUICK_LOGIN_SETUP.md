# Quick Login Setup - Step by Step

## Problem Fixed
✓ Login endpoint now works correctly  
✓ Each role has a dedicated test user  
✓ Users don't need any additional setup  
✓ Tokens work with all API endpoints  

---

## Quick Start (2 Steps)

### Step 1: Create Test Users
\`\`\`bash
python manage.py shell < scripts/create_test_users.py
\`\`\`

You'll see:
\`\`\`
✓ Director created: director1 / Director@123
✓ Manager created: manager1 / Manager@123
✓ Admin created: admin1 / Admin@123
✓ Teacher created: teacher1 / Teacher@123
✓ Student created: student1 / Student@123
\`\`\`

### Step 2: Test Login in Swagger
1. Go to: http://127.0.0.1:8000/api/docs/
2. Find "Login" endpoint
3. Click "Try it out"
4. Enter: 
   \`\`\`json
   {
     "username": "director1",
     "password": "Director@123"
   }
   \`\`\`
5. Click "Execute"
6. Get your token in response

---

## Available Test Users

| Role | Username | Password |
|------|----------|----------|
| Director | director1 | Director@123 |
| Manager | manager1 | Manager@123 |
| Admin | admin1 | Admin@123 |
| Teacher | teacher1 | Teacher@123 |
| Student | student1 | Student@123 |

---

## How to Use Token

After login, you get:
\`\`\`json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "role": "Director",
  "user_id": 1,
  "center_id": null
}
\`\`\`

### In Swagger:
1. Click "Authorize" button at top
2. Paste token in field
3. All endpoints now work

### In cURL:
\`\`\`bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/centers/
\`\`\`

### In Postman:
1. Authorization tab
2. Type: "Bearer Token"
3. Token: paste your token

---

## Frontend Integration

\`\`\`javascript
// 1. Login
const response = await fetch('http://127.0.0.1:8000/api/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'director1',
    password: 'Director@123'
  })
});

const data = await response.json();
const token = data.token;
const role = data.role;

// 2. Save token
localStorage.setItem('auth_token', token);

// 3. Redirect to dashboard
const dashboards = {
  Director: '/dashboard/director',
  Manager: '/dashboard/manager',
  Admin: '/dashboard/admin',
  Teacher: '/dashboard/teacher',
  Student: '/dashboard/student'
};

window.location.href = dashboards[role];

// 4. Use token in API calls
const centerResponse = await fetch('http://127.0.0.1:8000/api/centers/', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
\`\`\`

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| 401 Unauthorized | Check username/password case sensitivity |
| 404 Not Found | Ensure Django is running on 8000 |
| Invalid credentials | Use exact credentials from table above |
| Database error | Run `python manage.py migrate` |

---

## Files Created

- `scripts/create_test_users.py` - Creates all test users
- `LOGIN_TEST_GUIDE.md` - Complete testing guide
- `POSTMAN_COLLECTION.json` - Postman ready requests
- `QUICK_LOGIN_SETUP.md` - This file

---

That's it! You're ready to login and test all APIs! 🚀
