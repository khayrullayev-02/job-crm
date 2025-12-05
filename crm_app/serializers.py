from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    EducationalCenter, UserProfile, Branch, Subject, Group, Student, 
    Teacher, Lesson, Attendance, Payment, Assignment, AssignmentSubmission,
    Exam, ExamResult, Room, Payroll, Notification, Contract, Lead
)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'role',
            'educational_center',
            'phone',
            'passport_number',
            'birthday',
            'image',
            'is_blocked',
            'created_at',
            'updated_at'
        ]

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')   # profile ni alohida ajratamiz
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # endi profile yaratamiz
        UserProfile.objects.create(user=user, **profile_data)

        return user

# class UserSerializer(serializers.ModelSerializer):
#     profile = UserProfileSerializer()
#     """Basic user serializer"""
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password','profile')
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)  # passwordni hash qiladi
#         user.save()
#         return user

#
# class UserProfileSerializer(serializers.ModelSerializer):
#     """User profile serializer with user details"""
#     user = UserSerializer(read_only=True)
#     user_id = serializers.IntegerField(write_only=True, required=False)
#
#     class Meta:
#         model = UserProfile
#         fields = ('id', 'user', 'user_id', 'role', 'educational_center', 'phone',
#                  'passport_number', 'birthday', 'image', 'is_blocked', 'created_at')
#         read_only_fields = ('created_at',)


class DirectorListSerializer(serializers.ModelSerializer):
    """Serializer for listing available directors for center assignment"""
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('id', 'user_full_name', 'user_username', 'phone', 'role')
        read_only_fields = ('id', 'user_full_name', 'user_username', 'phone', 'role')


class EducationalCenterSerializer(serializers.ModelSerializer):
    """Educational center serializer"""
    director_name = serializers.CharField(source='director.get_full_name', read_only=True)
    director_username = serializers.CharField(source='director.username', read_only=True)
    users_count = serializers.SerializerMethodField()
    available_directors = serializers.SerializerMethodField()
    
    class Meta:
        model = EducationalCenter
        fields = ('id', 'name', 'address', 'phone', 'email', 'logo', 'description',
                 'license_number', 'opened_at', 'status', 'website', 'director',
                 'director_name', 'director_username', 'users_count', 'available_directors',
                 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'available_directors')
        extra_kwargs = {
            'director': {'required': False, 'allow_null': True}
        }
    
    def get_users_count(self, obj):
        return obj.users.count()
    
    def get_available_directors(self, obj):
        """Get list of available directors (those without an educational center)"""
        directors = UserProfile.objects.filter(
            role='Director', 
            educational_center__isnull=True
        )
        return DirectorListSerializer(directors, many=True).data


class BranchSerializer(serializers.ModelSerializer):
    """Branch serializer"""
    manager_name = serializers.CharField(source='manager.user.get_full_name', read_only=True)
    center_name = serializers.CharField(source='educational_center.name', read_only=True)
    
    class Meta:
        model = Branch
        fields = ('id', 'educational_center', 'center_name', 'name', 'address', 'phone',
                 'manager', 'manager_name', 'status', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class SubjectSerializer(serializers.ModelSerializer):
    """Subject/Course serializer"""
    center_name = serializers.CharField(source='educational_center.name', read_only=True)
    
    class Meta:
        model = Subject
        fields = ('id', 'educational_center', 'center_name', 'name', 'description', 'created_at')
        read_only_fields = ('created_at',)


class GroupSerializer(serializers.ModelSerializer):
    """Group serializer"""
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    students_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ('id', 'educational_center', 'branch', 'branch_name', 'name', 'subject',
                 'subject_name', 'teacher', 'teacher_name', 'capacity', 'status',
                 'start_date', 'end_date', 'students_count', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
    
    def get_students_count(self, obj):
        return obj.students.count()


class StudentSerializer(serializers.ModelSerializer):
    """Student serializer"""
    user_info = UserSerializer(source='user', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = Student
        fields = ('id', 'user', 'user_info', 'group', 'group_name', 'branch', 'branch_name',
                 'status', 'enrollment_date', 'phone', 'date_of_birth', 'parent_name', 
                 'parent_phone', 'parent_email', 'address', 'passport_number', 'image',
                 'created_at', 'updated_at')
        read_only_fields = ('enrollment_date', 'created_at', 'updated_at')


class TeacherSerializer(serializers.ModelSerializer):
    """Teacher serializer"""
    user_info = UserSerializer(source='user', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    teaching_groups_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Teacher
        fields = ('id', 'user', 'user_info', 'branch', 'branch_name', 'status',
                 'phone', 'date_of_birth', 'specialization', 'qualification', 
                 'performance_rating', 'hire_date', 'hourly_rate', 'address',
                 'passport_number', 'image', 'teaching_groups_count', 'created_at', 'updated_at')
        read_only_fields = ('hire_date', 'created_at', 'updated_at')
    
    def get_teaching_groups_count(self, obj):
        return obj.teaching_groups.count()


class LessonSerializer(serializers.ModelSerializer):
    """Lesson serializer"""
    group_name = serializers.CharField(source='group.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    
    class Meta:
        model = Lesson
        fields = ('id', 'group', 'group_name', 'teacher', 'teacher_name', 'room', 'room_name',
                 'date', 'start_time', 'end_time', 'duration', 'online_link', 'is_cancelled',
                 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class AttendanceSerializer(serializers.ModelSerializer):
    """Attendance serializer"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    lesson_info = serializers.CharField(source='lesson', read_only=True)
    teacher_name = serializers.CharField(source='marked_by.user.get_full_name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ('id', 'lesson', 'lesson_info', 'student', 'student_name', 'status',
                 'marked_by', 'teacher_name', 'notes', 'marked_at')
        read_only_fields = ('marked_at',)


class PaymentSerializer(serializers.ModelSerializer):
    """Payment serializer"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    processed_by = serializers.CharField(source='paid_by.user.get_full_name', read_only=True)
    
    class Meta:
        model = Payment
        fields = ('id', 'student', 'student_name', 'group', 'group_name', 'amount',
                 'payment_type', 'payment_date', 'due_date', 'receipt_number', 'document',
                 'paid_by', 'processed_by', 'notes', 'created_at')
        read_only_fields = ('payment_date', 'created_at')


class AssignmentSerializer(serializers.ModelSerializer):
    """Assignment serializer"""
    group_name = serializers.CharField(source='group.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    submissions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = ('id', 'group', 'group_name', 'teacher', 'teacher_name', 'title',
                 'description', 'file', 'due_date', 'status', 'submissions_count',
                 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
    
    def get_submissions_count(self, obj):
        return obj.submissions.count()


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    """Assignment submission serializer"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    
    class Meta:
        model = AssignmentSubmission
        fields = ('id', 'assignment', 'assignment_title', 'student', 'student_name',
                 'submission_file', 'submitted_at', 'grade', 'feedback', 'graded_at')
        read_only_fields = ('submitted_at',)


class ExamSerializer(serializers.ModelSerializer):
    """Exam serializer"""
    group_name = serializers.CharField(source='group.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    results_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = ('id', 'group', 'group_name', 'teacher', 'teacher_name', 'title',
                 'description', 'exam_date', 'start_time', 'end_time', 'total_points',
                 'passing_score', 'results_count', 'created_at')
        read_only_fields = ('created_at',)
    
    def get_results_count(self, obj):
        return obj.results.count()


class ExamResultSerializer(serializers.ModelSerializer):
    """Exam result serializer"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    
    class Meta:
        model = ExamResult
        fields = ('id', 'exam', 'exam_title', 'student', 'student_name', 'score',
                 'grade', 'answer_file', 'submitted_at')
        read_only_fields = ('submitted_at',)


class RoomSerializer(serializers.ModelSerializer):
    """Room serializer"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = Room
        fields = ('id', 'branch', 'branch_name', 'name', 'capacity', 'equipment',
                 'is_available')


class PayrollSerializer(serializers.ModelSerializer):
    """Payroll serializer"""
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    
    class Meta:
        model = Payroll
        fields = ('id', 'teacher', 'teacher_name', 'month', 'base_salary', 'bonus',
                 'penalty', 'total_salary', 'is_paid', 'paid_date', 'created_at')
        read_only_fields = ('created_at',)


class NotificationSerializer(serializers.ModelSerializer):
    """Notification serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Notification
        fields = ('id', 'user', 'username', 'notification_type', 'title', 'message',
                 'is_read', 'created_at')
        read_only_fields = ('created_at',)


class ContractSerializer(serializers.ModelSerializer):
    """Contract serializer"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    verified_by_name = serializers.CharField(source='verified_by.user.get_full_name', read_only=True)
    
    class Meta:
        model = Contract
        fields = ('id', 'student', 'student_name', 'group', 'group_name',
                 'contract_number', 'contract_file', 'signed_date', 'is_verified',
                 'verified_by', 'verified_by_name', 'created_at')
        read_only_fields = ('created_at',)


class LeadSerializer(serializers.ModelSerializer):
    """Lead serializer"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    course_name = serializers.CharField(source='course_interested.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.user.get_full_name', read_only=True)
    
    class Meta:
        model = Lead
        fields = ('id', 'branch', 'branch_name', 'name', 'email', 'phone',
                 'course_interested', 'course_name', 'status', 'source',
                 'assigned_to', 'assigned_to_name', 'notes', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class LoginSerializer(serializers.Serializer):
    """Login serializer"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
