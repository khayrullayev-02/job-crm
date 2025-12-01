# Login and Token Issues - Troubleshooting

## Issue 1: "User not found" or 401 error

**Problem**: When you try to login, you get error like:
\`\`\`json
{
  "non_field_errors": ["Invalid username or password"]
}
\`\`\`

**Solution**: 

1. First, verify users exist:
   \`\`\`bash
   python manage.py shell
   \`\`\`

   \`\`\`python
   from django.contrib.auth.models import User
   User.objects.all().values('username')
   \`\`\`

   Should show:
   \`\`\`
   [{'username': 'director1'}, {'username': 'teacher1'}, ...]
   \`\`\`

2. If users don't exist, create them using Method 1 (Management Command):
   \`\`\`bash
   python manage.py create_test_users
   \`\`\`

---

## Issue 2: "Failed to connect to backend"

**Problem**: Frontend can't reach backend at http://127.0.0.1:8000

**Solution**:

1. Make sure server is running:
   \`\`\`bash
   python manage.py runserver
   \`\`\`

2. Check if server is on port 8000:
   \`\`\`
   Output should show:
   Starting development server at http://127.0.0.1:8000/
   \`\`\`

3. Test with cURL:
   \`\`\`bash
   curl http://127.0.0.1:8000/api/docs/
   \`\`\`

   If you see Swagger UI HTML, server is running.

---

## Issue 3: CORS Error

**Problem**: Browser shows CORS error when frontend calls backend

**Solution**: Add to `crm_project/settings.py`:

\`\`\`python
INSTALLED_APPS = [
    # ... other apps
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ADD THIS FIRST
    'django.middleware.common.CommonMiddleware',
    # ... rest of middleware
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
\`\`\`

Install corsheaders:
\`\`\`bash
pip install django-cors-headers
\`\`\`

---

## Issue 4: Token not being returned

**Problem**: Login works but token is null or empty in response

**Check**: Verify LoginSerializer in serializers.py has `return_token` method

\`\`\`python
def validate(self, data):
    user = authenticate(username=data['username'], password=data['password'])
    if not user:
        raise serializers.ValidationError("Invalid credentials")
    return user
\`\`\`

---

## Quick Debug Checklist

1. Migrations done?
   \`\`\`bash
   python manage.py migrate
   \`\`\`

2. Users created?
   \`\`\`bash
   python manage.py create_test_users
   \`\`\`

3. Server running?
   \`\`\`bash
   python manage.py runserver
   \`\`\`

4. Can access Swagger?
   \`\`\`
   http://127.0.0.1:8000/api/docs/
   \`\`\`

5. Try login with cURL:
   \`\`\`bash
   curl -X POST http://127.0.0.1:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"username":"director1","password":"Director@123"}'
   \`\`\`

---

## Still not working?

If none of the above works:

1. Check Django logs for errors
2. Run `python manage.py check` to verify setup
3. Make sure PostgreSQL is running (if using PostgreSQL)
4. Check environment variables in `.env` file
