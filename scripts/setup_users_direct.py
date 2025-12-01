"""
Direct script to create test users.
Run: python scripts/setup_users_direct.py
Or in Django shell: python manage.py shell < scripts/setup_users_direct.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')

try:
    django.setup()
except:
    pass

from django.contrib.auth.models import User
from crm_app.models import UserProfile

print("\n" + "="*60)
print("CREATING TEST USERS...")
print("="*60 + "\n")

users_data = [
    {
        'username': 'director1',
        'password': 'Director@123',
        'email': 'director1@crm.com',
        'first_name': 'Azizbek',
        'last_name': 'Abdullaev',
        'role': 'Director',
        'phone': '+998901234567',
        'passport_number': 'AB1234567',
        'birthday': '1985-05-15',
    },
    {
        'username': 'manager1',
        'password': 'Manager@123',
        'email': 'manager1@crm.com',
        'first_name': 'Farruh',
        'last_name': 'Nasrov',
        'role': 'Manager',
        'phone': '+998902345678',
        'passport_number': 'AB2345678',
        'birthday': '1990-07-20',
    },
    {
        'username': 'admin1',
        'password': 'Admin@123',
        'email': 'admin1@crm.com',
        'first_name': 'Shuhrat',
        'last_name': 'Karimov',
        'role': 'Admin',
        'phone': '+998903456789',
        'passport_number': 'AB3456789',
        'birthday': '1992-03-10',
    },
    {
        'username': 'teacher1',
        'password': 'Teacher@123',
        'email': 'teacher1@crm.com',
        'first_name': 'Nodira',
        'last_name': 'Shodmonova',
        'role': 'Teacher',
        'phone': '+998904567890',
        'passport_number': 'AB4567890',
        'birthday': '1988-09-25',
    },
    {
        'username': 'student1',
        'password': 'Student@123',
        'email': 'student1@crm.com',
        'first_name': 'Ali',
        'last_name': 'Rasulov',
        'role': 'Student',
        'phone': '+998905678901',
        'passport_number': 'AB5678901',
        'birthday': '2005-11-12',
    },
]

for user_data in users_data:
    password = user_data.pop('password')
    role = user_data.pop('role')
    phone = user_data.pop('phone')
    passport_number = user_data.pop('passport_number')
    birthday = user_data.pop('birthday')

    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults=user_data
    )

    if created:
        user.set_password(password)
        user.save()

        UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'role': role,
                'phone': phone,
                'passport_number': passport_number,
                'birthday': birthday,
            }
        )
        print(f"✓ {role:10} created: {user_data['username']:15} / {password}")
    else:
        print(f"- {role:10} exists:  {user_data['username']:15}")

print("\n" + "="*60)
print("TEST USERS READY FOR LOGIN!")
print("="*60)
print("\nCopy and paste this in Swagger or Postman:")
print("\nPOST http://127.0.0.1:8000/api/login/")
print("\nBody (JSON):")
print("{")
print('  "username": "director1",')
print('  "password": "Director@123"')
print("}")
print("\n" + "="*60 + "\n")
