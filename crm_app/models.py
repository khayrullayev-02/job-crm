from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta

# from rest_framework import viewsets, permissions

# from crm_app.serializers import UserSerializer


# from crm_app.serializers import UserSerializer


class EducationalCenter(models.Model):
    """Main educational center model"""
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    logo = models.ImageField(upload_to='centers/', null=True, blank=True)
    description = models.TextField(blank=True)
    license_number = models.CharField(max_length=100, unique=True, blank=True)
    opened_at = models.DateField(default=datetime.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    website = models.URLField(blank=True)
    director = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='directed_centers', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Educational Centers'
    
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Extended user profile for different roles"""
    ROLE_CHOICES = [
        ('SuperAdmin', 'SuperAdmin'),
        ('Director', 'Director'),
        ('Manager', 'Manager'),
        ('Admin', 'Admin'),
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    educational_center = models.ForeignKey(EducationalCenter, on_delete=models.CASCADE, 
                                          related_name='users', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    passport_number = models.CharField(
    max_length=50,
    unique=True,
    null=True,
    blank=True
    )
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"


class Branch(models.Model):
    """Branches of educational center"""
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]
    
    educational_center = models.ForeignKey(EducationalCenter, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    manager = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='managed_branches', limit_choices_to={'role': 'Manager'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.educational_center.name} - {self.name}"
    
    class Meta:
        ordering = ['-created_at']


class Subject(models.Model):
    """Subjects/Courses offered"""
    educational_center = models.ForeignKey(EducationalCenter, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ('educational_center', 'name')


class Group(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Closed', 'Closed'),
    ]

    educational_center = models.ForeignKey(
        EducationalCenter,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='groups'
    )
    room = models.ForeignKey(           # 🔥 YANGI QISM
        'Room',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='groups'
    )
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        related_name='groups'
    )
    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teaching_groups'
    )
    capacity = models.IntegerField(default=30)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.room.name if self.room else 'No room'}"

    class Meta:
        unique_together = ('branch', 'name')
        ordering = ['-created_at']



# class Student(models.Model):
#     """Student model"""
#     STATUS_CHOICES = [
#         ('Active', 'Active'),
#         ('Inactive', 'Inactive'),
#         ('Blocked', 'Blocked'),
#     ]
    
    
#     group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='students')
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
#     enrollment_date = models.DateField(auto_now_add=True)
#     phone = models.CharField(max_length=20, blank=True)
#     date_of_birth = models.DateField(null=True, blank=True)
#     parent_name = models.CharField(max_length=255, blank=True)
#     parent_phone = models.CharField(max_length=20, blank=True)
#     parent_email = models.EmailField(blank=True)
#     address = models.TextField(blank=True)
#     passport_number = models.CharField(max_length=20, blank=True, unique=True)
#     image = models.ImageField(upload_to='students/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.user.get_full_name()} - {self.group}"
    
#     class Meta:
#         ordering = ['-created_at']




class Student(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Blocked', 'Blocked'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)  # Markazga kelgan sanasi
    address = models.TextField(blank=True)
    
    parent_name = models.CharField(max_length=255, blank=True)
    parent_phone = models.CharField(max_length=20, blank=True)
    parent_email = models.EmailField(blank=True)
    
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    # group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='students')
    
    passport_number = models.CharField(
    max_length=50,
    unique=True,
    null=True,
    blank=True
    )
    image = models.ImageField(upload_to='students/', null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.group.name if self.group else 'No Group'}"
    
    class Meta:
        ordering = ['-created_at']





class Teacher(models.Model):
    """Teacher model with performance metrics"""
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Blocked', 'Blocked'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='teachers')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    specialization = models.CharField(max_length=255, blank=True)
    qualification = models.TextField(blank=True)
    performance_rating = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    hire_date = models.DateField(auto_now_add=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.TextField(blank=True)
    passport_number = models.CharField(
    max_length=50,
    unique=True,
    null=True,
    blank=True
    )
    image = models.ImageField(upload_to='teachers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"
    
    class Meta:
        ordering = ['-created_at']


    def get_queryset(self):
        """Superuser bo'lmagan foydalanuvchilarni ko'rsatish"""
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(is_superuser=False)

class Lesson(models.Model):
    """Lessons/Classes"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lessons')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='lessons')
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in minutes", default=45)
    online_link = models.URLField(blank=True)
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.group.name} - {self.date} {self.start_time}"
    
    class Meta:
        ordering = ['-date', '-start_time']


class Attendance(models.Model):
    """Student attendance tracking"""
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    ]
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='marked_attendances')
    notes = models.TextField(blank=True)
    marked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.lesson.date} - {self.status}"
    
    class Meta:
        unique_together = ('lesson', 'student')
        ordering = ['-marked_at']


class Payment(models.Model):
    """Payment records"""
    PAYMENT_TYPE_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Bank Transfer', 'Bank Transfer'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    payment_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    receipt_number = models.CharField(max_length=100, unique=True)
    document = models.FileField(upload_to='receipts/', null=True, blank=True)
    paid_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='processed_payments',
                               limit_choices_to={'role__in': ['Admin', 'Manager']})
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.amount} - {self.payment_date}"
    
    class Meta:
        ordering = ['-payment_date']


class Assignment(models.Model):
    """Homework/Assignments"""
    STATUS_CHOICES = [
        ('Assigned', 'Assigned'),
        ('Submitted', 'Submitted'),
        ('Graded', 'Graded'),
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Assigned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.group.name}"
    
    class Meta:
        ordering = ['-created_at']


class AssignmentSubmission(models.Model):
    """Student assignment submissions"""
    GRADE_CHOICES = [
        ('A', 'Excellent'),
        ('B', 'Good'),
        ('C', 'Average'),
        ('D', 'Below Average'),
        ('F', 'Fail'),
    ]
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submission_file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    feedback = models.TextField(blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.assignment.title}"
    
    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']


class Exam(models.Model):
    """Exam/Test module"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='exams')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_points = models.IntegerField(default=100)
    passing_score = models.IntegerField(default=60)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.exam_date}"
    
    class Meta:
        ordering = ['-exam_date']


class ExamResult(models.Model):
    """Exam results for students"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_results')
    score = models.IntegerField(validators=[MinValueValidator(0)])
    grade = models.CharField(max_length=2, blank=True)
    answer_file = models.FileField(upload_to='exam_answers/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam.title} - {self.score}"
    
    class Meta:
        unique_together = ('exam', 'student')
        ordering = ['-submitted_at']


class Room(models.Model):
    """Classroom/Room management"""
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    equipment = models.CharField(max_length=255, blank=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.branch.name} - {self.name} (Capacity: {self.capacity})"
    
    class Meta:
        unique_together = ('branch', 'name')


class Payroll(models.Model):
    """Teacher payroll management"""
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='payroll')
    month = models.CharField(max_length=7)  # YYYY-MM format
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    penalty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.teacher.user.get_full_name()} - {self.month}"
    
    class Meta:
        unique_together = ('teacher', 'month')
        ordering = ['-month']


class Notification(models.Model):
    """System notifications"""
    NOTIFICATION_TYPES = [
        ('Payment Reminder', 'Payment Reminder'),
        ('Attendance Alert', 'Attendance Alert'),
        ('Exam Notification', 'Exam Notification'),
        ('System Alert', 'System Alert'),
        ('Group Notification', 'Group Notification'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.title}"
    
    class Meta:
        ordering = ['-created_at']


class Contract(models.Model):
    """Student contracts"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='contracts')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='contracts')
    contract_number = models.CharField(max_length=100, unique=True)
    contract_file = models.FileField(upload_to='contracts/')
    signed_date = models.DateField()
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='verified_contracts')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Contract - {self.student.user.get_full_name()}"
    
    class Meta:
        ordering = ['-signed_date']


class Lead(models.Model):
    """Marketing leads"""
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Qualified', 'Qualified'),
        ('Converted', 'Converted'),
        ('Rejected', 'Rejected'),
    ]
    
    SOURCE_CHOICES = [
        ('Social Media', 'Social Media'),
        ('Website', 'Website'),
        ('Referral', 'Referral'),
        ('Direct Call', 'Direct Call'),
        ('Advertisement', 'Advertisement'),
    ]
    
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='leads')
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    course_interested = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='assigned_leads', limit_choices_to={'role': 'Manager'})
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']
