"""
Script to create test users for each role in the system.
Run this in Django shell: python manage.py shell < scripts/create_test_users.py
"""

from django.contrib.auth.models import User
from crm_app.models import UserProfile, EducationalCenter

# Clear existing test data (optional - comment out if you want to keep data)
print("Creating test users for all roles...\n")

# 1. Create SUPERADMIN User (only in Django admin)
superadmin_user, created = User.objects.get_or_create(
    username='superadmin',
    defaults={
        'email': 'superadmin@crm.com',
        'first_name': 'Super',
        'last_name': 'Admin',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    superadmin_user.set_password('SuperAdmin@123')
    superadmin_user.save()
    print("✓ Superadmin created: superadmin / SuperAdmin@123")
else:
    print("✓ Superadmin already exists")

# 2. Create DIRECTOR User
director_user, created = User.objects.get_or_create(
    username='director1',
    defaults={
        'email': 'director1@crm.com',
        'first_name': 'Azizbek',
        'last_name': 'Abdullaev',
    }
)
if created:
    director_user.set_password('Director@123')
    director_user.save()
    profile, _ = UserProfile.objects.get_or_create(
        user=director_user,
        defaults={
            'role': 'Director',
            'phone': '+998901234567',
            'passport_number': 'AB1234567',
            'birthday': '1985-05-15',
        }
    )
    print("✓ Director created: director1 / Director@123")
else:
    print("✓ Director already exists")

# 3. Create MANAGER User
manager_user, created = User.objects.get_or_create(
    username='manager1',
    defaults={
        'email': 'manager1@crm.com',
        'first_name': 'Farruh',
        'last_name': 'Nasrov',
    }
)
if created:
    manager_user.set_password('Manager@123')
    manager_user.save()
    profile, _ = UserProfile.objects.get_or_create(
        user=manager_user,
        defaults={
            'role': 'Manager',
            'phone': '+998902345678',
            'passport_number': 'AB2345678',
            'birthday': '1990-07-20',
        }
    )
    print("✓ Manager created: manager1 / Manager@123")
else:
    print("✓ Manager already exists")

# 4. Create ADMIN User
admin_user, created = User.objects.get_or_create(
    username='admin1',
    defaults={
        'email': 'admin1@crm.com',
        'first_name': 'Shuhrat',
        'last_name': 'Karimov',
    }
)
if created:
    admin_user.set_password('Admin@123')
    admin_user.save()
    profile, _ = UserProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'role': 'Admin',
            'phone': '+998903456789',
            'passport_number': 'AB3456789',
            'birthday': '1992-03-10',
        }
    )
    print("✓ Admin created: admin1 / Admin@123")
else:
    print("✓ Admin already exists")

# 5. Create TEACHER User
teacher_user, created = User.objects.get_or_create(
    username='teacher1',
    defaults={
        'email': 'teacher1@crm.com',
        'first_name': 'Nodira',
        'last_name': 'Shodmonova',
    }
)
if created:
    teacher_user.set_password('Teacher@123')
    teacher_user.save()
    profile, _ = UserProfile.objects.get_or_create(
        user=teacher_user,
        defaults={
            'role': 'Teacher',
            'phone': '+998904567890',
            'passport_number': 'AB4567890',
            'birthday': '1988-09-25',
        }
    )
    print("✓ Teacher created: teacher1 / Teacher@123")
else:
    print("✓ Teacher already exists")

# 6. Create STUDENT User
student_user, created = User.objects.get_or_create(
    username='student1',
    defaults={
        'email': 'student1@crm.com',
        'first_name': 'Ali',
        'last_name': 'Rasulov',
    }
)
if created:
    student_user.set_password('Student@123')
    student_user.save()
    profile, _ = UserProfile.objects.get_or_create(
        user=student_user,
        defaults={
            'role': 'Student',
            'phone': '+998905678901',
            'passport_number': 'AB5678901',
            'birthday': '2005-11-12',
        }
    )
    print("✓ Student created: student1 / Student@123")
else:
    print("✓ Student already exists")

print("\n" + "="*50)
print("ALL TEST USERS CREATED SUCCESSFULLY!")
print("="*50)
print("\nLogin credentials:")
print("├─ Director  : director1 / Director@123")
print("├─ Manager   : manager1 / Manager@123")
print("├─ Admin     : admin1 / Admin@123")
print("├─ Teacher   : teacher1 / Teacher@123")
print("└─ Student   : student1 / Student@123")
print("\nTest login at: POST http://127.0.0.1:8000/api/login/")
print("="*50)
