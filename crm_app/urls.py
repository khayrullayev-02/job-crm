# # from django.urls import path, include
# # from rest_framework.routers import DefaultRouter
# #
# # # from .models import UserViewSet
# # from .views import (
# #     EducationalCenterViewSet, DirectorViewSet,  #LoginViewSet,
# #     BranchViewSet, SubjectViewSet, GroupViewSet, StudentViewSet, TeacherViewSet,
# #     LessonViewSet, AttendanceViewSet, PaymentViewSet, AssignmentViewSet,
# #     AssignmentSubmissionViewSet, ExamViewSet, ExamResultViewSet, RoomViewSet,
# #     PayrollViewSet, NotificationViewSet, ContractViewSet, LeadViewSet, LoginAPIView
# # )
# #
# # router = DefaultRouter()
# #
# # # SuperAdmin Endpoints
# # router.register(r'centers', EducationalCenterViewSet, basename='center')
# # router.register(r'directors', DirectorViewSet, basename='director')
# #
# # # Authentication
# # router.register(r'auth', LoginAPIView, basename='auth')
# #
# # # Director/Manager Endpoints
# # router.register(r'branches', BranchViewSet, basename='branch')
# # router.register(r'subjects', SubjectViewSet, basename='subject')
# # router.register(r'groups', GroupViewSet, basename='group')
# #
# # # User Management
# # router.register(r'students', StudentViewSet, basename='student')
# # router.register(r'teachers', TeacherViewSet, basename='teacher')
# #
# # # Academic
# # router.register(r'lessons', LessonViewSet, basename='lesson')
# # router.register(r'attendance', AttendanceViewSet, basename='attendance')
# # router.register(r'assignments', AssignmentViewSet, basename='assignment')
# # router.register(r'submissions', AssignmentSubmissionViewSet, basename='submission')
# # router.register(r'exams', ExamViewSet, basename='exam')
# # router.register(r'exam-results', ExamResultViewSet, basename='exam-result')
# #
# # # Financial
# # router.register(r'payments', PaymentViewSet, basename='payment')
# # router.register(r'payroll', PayrollViewSet, basename='payroll')
# #
# # # Operations
# # router.register(r'rooms', RoomViewSet, basename='room')
# # router.register(r'contracts', ContractViewSet, basename='contract')
# # router.register(r'leads', LeadViewSet, basename='lead')
# #
# # # User
# # router.register(r'notifications', NotificationViewSet, basename='notification')
# # # router.register(r'users', UserViewSet, basename='user')
# # from rest_framework import routers
# # from crm_app.views import UserViewSet
# #
# # router = routers.DefaultRouter()
# # router.register(r'users', UserViewSet, basename='user')
# #
# # urlpatterns = [
# #     path('', include(router.urls)),
# #     path('login/', LoginAPIView.as_view(), name='login'),
# # ]
# # # {'post': 'login'}
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import (
#     EducationalCenterViewSet, DirectorViewSet,  # LoginViewSet,
#     BranchViewSet, SubjectViewSet, GroupViewSet, StudentViewSet, TeacherViewSet,
#     LessonViewSet, AttendanceViewSet, PaymentViewSet, AssignmentViewSet,
#     AssignmentSubmissionViewSet, ExamViewSet, ExamResultViewSet, RoomViewSet,
#     PayrollViewSet, NotificationViewSet, ContractViewSet, LeadViewSet,
#     LoginAPIView, UserViewSet  # UserViewSet ni import qiling
# )

# router = DefaultRouter()

# # SuperAdmin Endpoints
# router.register(r'centers', EducationalCenterViewSet, basename='center')
# router.register(r'directors', DirectorViewSet, basename='director')

# # User Management
# router.register(r'users', UserViewSet, basename='user')  # Bu yerda
# router.register(r'students', StudentViewSet, basename='student')
# router.register(r'teachers', TeacherViewSet, basename='teacher')

# # Director/Manager Endpoints
# router.register(r'branches', BranchViewSet, basename='branch')
# router.register(r'subjects', SubjectViewSet, basename='subject')
# router.register(r'groups', GroupViewSet, basename='group')

# # Academic
# router.register(r'lessons', LessonViewSet, basename='lesson')
# router.register(r'attendance', AttendanceViewSet, basename='attendance')
# router.register(r'assignments', AssignmentViewSet, basename='assignment')
# router.register(r'submissions', AssignmentSubmissionViewSet, basename='submission')
# router.register(r'exams', ExamViewSet, basename='exam')
# router.register(r'exam-results', ExamResultViewSet, basename='exam-result')

# # Financial
# router.register(r'payments', PaymentViewSet, basename='payment')
# router.register(r'payroll', PayrollViewSet, basename='payroll')

# # Operations
# router.register(r'rooms', RoomViewSet, basename='room')
# router.register(r'contracts', ContractViewSet, basename='contract')
# router.register(r'leads', LeadViewSet, basename='lead')

# # User
# router.register(r'notifications', NotificationViewSet, basename='notification')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('login/', LoginAPIView.as_view(), name='login'),
# ]








from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EducationalCenterViewSet, DirectorViewSet,
    BranchViewSet, SubjectViewSet, GroupViewSet, StudentViewSet, TeacherViewSet,
    LessonViewSet, AttendanceViewSet, PaymentViewSet, AssignmentViewSet,
    AssignmentSubmissionViewSet, ExamViewSet, ExamResultViewSet, RoomViewSet,
    PayrollViewSet, NotificationViewSet, ContractViewSet, LeadViewSet,
    LoginAPIView, UserViewSet
)

# DefaultRouter yordamida barcha ViewSetlarni ro'yxatdan o'tkazamiz
router = DefaultRouter()

# ----------------------------
# SuperAdmin Endpoints
# ----------------------------
router.register(r'centers', EducationalCenterViewSet, basename='center')
router.register(r'directors', DirectorViewSet, basename='director')

# ----------------------------
# User Management
# ----------------------------
router.register(r'users', UserViewSet, basename='user')  # CRUD + block/unblock
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')

# ----------------------------
# Director/Manager Endpoints
# ----------------------------
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'groups', GroupViewSet, basename='group')

# ----------------------------
# Academic Endpoints
# ----------------------------
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'submissions', AssignmentSubmissionViewSet, basename='submission')
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'exam-results', ExamResultViewSet, basename='exam-result')

# ----------------------------
# Financial Endpoints
# ----------------------------
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'payroll', PayrollViewSet, basename='payroll')

# ----------------------------
# Operations
# ----------------------------
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'contracts', ContractViewSet, basename='contract')
router.register(r'leads', LeadViewSet, basename='lead')

# ----------------------------
# Notifications
# ----------------------------
router.register(r'notifications', NotificationViewSet, basename='notification')

# ----------------------------
# JWT Login API
# ----------------------------
urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='login'),  # username/password orqali token olish
]
