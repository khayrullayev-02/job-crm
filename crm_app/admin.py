from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    EducationalCenter, UserProfile, Branch, Subject, Group, Student,
    Teacher, Lesson, Attendance, Payment, Assignment, AssignmentSubmission,
    Exam, ExamResult, Room, Payroll, Notification, Contract, Lead
)

# ----------------------------
# Educational Center
# ----------------------------
@admin.register(EducationalCenter)
class EducationalCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'phone')


# ----------------------------
# User Profile
# ----------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'educational_center', 'is_blocked', 'created_at')
    list_filter = ('role', 'is_blocked', 'educational_center')
    search_fields = ('user__username', 'user__email', 'passport_number')
    autocomplete_fields = ('educational_center',)


# ----------------------------
# Branch
# ----------------------------
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'educational_center', 'status', 'manager')
    list_filter = ('status', 'educational_center')
    search_fields = ('name',)
    autocomplete_fields = ('educational_center', 'manager')


# ----------------------------
# Subject
# ----------------------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'educational_center')
    search_fields = ('name',)
    autocomplete_fields = ('educational_center',)


# ----------------------------
# Group
# ----------------------------
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'teacher', 'status')
    list_filter = ('status', 'subject')
    search_fields = ('name',)
    autocomplete_fields = ('subject', 'teacher')


# ----------------------------
# Student
# ----------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'group', 'branch', 'status', 'enrollment_date')
    list_filter = ('status', 'branch', 'group')
    search_fields = ('first_name', 'last_name', 'phone')
    autocomplete_fields = ('group', 'branch')

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Full Name"


# ----------------------------
# Teacher
# ----------------------------
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'branch', 'specialization', 'status')
    list_filter = ('branch', 'status')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    autocomplete_fields = ('branch',)


# ----------------------------
# Lesson
# ----------------------------
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('group', 'teacher', 'date', 'is_cancelled')
    list_filter = ('is_cancelled', 'date')
    search_fields = ('group__name', 'teacher__user__username')
    autocomplete_fields = ('group', 'teacher')


# ----------------------------
# Attendance
# ----------------------------
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'status', 'marked_at')
    list_filter = ('status', 'lesson')
    autocomplete_fields = ('student', 'lesson')


# ----------------------------
# Payment
# ----------------------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'payment_date', 'payment_type')
    list_filter = ('payment_type', 'payment_date')
    search_fields = ('student__user__username',)
    autocomplete_fields = ('student',)


# ----------------------------
# Assignment
# ----------------------------
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'teacher', 'due_date')
    search_fields = ('title',)
    autocomplete_fields = ('group', 'teacher')


# ----------------------------
# Assignment Submission
# ----------------------------
@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'grade')
    autocomplete_fields = ('assignment', 'student')


# ----------------------------
# Exam
# ----------------------------
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'exam_date')
    search_fields = ('title',)
    autocomplete_fields = ('group',)


# ----------------------------
# Exam Result
# ----------------------------
@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'score', 'grade')
    autocomplete_fields = ('exam', 'student')


# ----------------------------
# Room
# ----------------------------
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'branch', 'capacity', 'is_available')
    list_filter = ('branch', 'is_available')
    search_fields = ('name',)
    autocomplete_fields = ('branch',)


# ----------------------------
# Payroll
# ----------------------------
@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'month', 'total_salary', 'is_paid')
    list_filter = ('month', 'is_paid')
    autocomplete_fields = ('teacher',)


# ----------------------------
# Notification
# ----------------------------
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')
    search_fields = ('user__username', 'user__email')
    autocomplete_fields = ('user',)


# ----------------------------
# Contract
# ----------------------------
@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('student', 'contract_number', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('contract_number',)
    autocomplete_fields = ('student',)


# ----------------------------
# Lead
# ----------------------------
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status', 'source')
    list_filter = ('status', 'source')
    search_fields = ('name', 'phone')


# ----------------------------
# Custom User Admin
# ----------------------------
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = ('role', 'educational_center', 'phone', 'passport_number', 'birthday', 'image', 'is_blocked')
    readonly_fields = ('created_at', 'updated_at')


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'get_center', 'is_staff', 'is_active')
    list_select_related = ('profile',)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'profile__passport_number')

    # Show first_name, last_name, email in admin detail
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Show first_name, last_name, email in "Add user" page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )

    def get_role(self, obj):
        return obj.profile.role if hasattr(obj, 'profile') else ''
    get_role.short_description = 'Role'

    def get_center(self, obj):
        return obj.profile.educational_center if hasattr(obj, 'profile') else ''
    get_center.short_description = 'Educational Center'


# Unregister default User and register custom
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
