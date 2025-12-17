from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q, Count, Avg
from django.utils import timezone
from .models import (
    EducationalCenter, UserProfile, Branch, Subject, Group, Student,
    Teacher, Lesson, Attendance, Payment, Assignment, AssignmentSubmission,
    Exam, ExamResult, Room, Payroll, Notification, Contract, Lead
)
from .serializers import (
    UserSerializer, UserProfileSerializer, EducationalCenterSerializer,
    BranchSerializer, SubjectSerializer, GroupSerializer, StudentSerializer,
    TeacherSerializer, LessonSerializer, AttendanceSerializer, PaymentSerializer,
    AssignmentSerializer, AssignmentSubmissionSerializer, ExamSerializer,
    ExamResultSerializer, RoomSerializer, PayrollSerializer, NotificationSerializer,
    ContractSerializer, LeadSerializer, LoginSerializer
)


# SUPERADMIN VIEWS
class EducationalCenterViewSet(viewsets.ModelViewSet):
    """
    SuperAdmin API for managing educational centers.

    Authentication: IsAuthenticated
    Permission: Only SuperAdmin role allowed (comment out for testing with AllowAny)

    ENDPOINTS:
    - GET /api/centers/ - List all centers
    - POST /api/centers/ - Create new center
    - GET /api/centers/{id}/ - Retrieve center
    - PUT /api/centers/{id}/ - Update center
    - PATCH /api/centers/{id}/ - Partial update
    - DELETE /api/centers/{id}/ - Delete center
    - POST /api/centers/{id}/activate/ - Activate center
    - POST /api/centers/{id}/deactivate/ - Deactivate center
    """
    queryset = EducationalCenter.objects.all()
    serializer_class = EducationalCenterSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate center"""
        center = self.get_object()
        center.status = 'Active'
        center.save()
        return Response({'status': 'Center activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate center"""
        center = self.get_object()
        center.status = 'Inactive'
        center.save()
        return Response({'status': 'Center deactivated'})


class DirectorViewSet(viewsets.ModelViewSet):
    """
    SuperAdmin API for creating and managing directors.

    Authentication: IsAuthenticated
    Permission: Only SuperAdmin role allowed

    ENDPOINTS:
    - GET /api/directors/ - List all directors
    - POST /api/directors/ - Create new director
    - GET /api/directors/{id}/ - Retrieve director
    - PUT /api/directors/{id}/ - Update director
    - DELETE /api/directors/{id}/ - Delete director
    """
    queryset = UserProfile.objects.filter(role='Director')
    serializer_class = UserProfileSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """Create director with user account"""
        user_data = self.request.data
        user = User.objects.create_user(
            username=user_data.get('username'),
            password=user_data.get('password'),
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            email=user_data.get('email', '')
        )
        serializer.save(user=user, role='Director')


# class LoginAPIView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = authenticate(
#             username=serializer.validated_data['username'],
#             password=serializer.validated_data['password']
#         )

#         if not user:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#         refresh = RefreshToken.for_user(user)
#         profile = UserProfile.objects.filter(user=user).first()

#         return Response({
#             'access': str(refresh.access_token),
#             'refresh': str(refresh),
#             'user_id': user.id,
#             'username': user.username,
#             'role': getattr(profile, 'role', None),
#             'center_id': getattr(profile.educational_center, 'id', None) if profile else None
#         })




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from .models import UserProfile

class LoginAPIView(APIView):
    """
    Login API for obtaining JWT token.
    POST: { "username": "user", "password": "pass" }
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # JWT token yaratish
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Foydalanuvchi roli
        try:
            profile = user.userprofile  # OneToOneField orqali UserProfile
            role = profile.role
        except:
            role = "NoRole"

        return Response({
            'access': access_token,
            'refresh': str(refresh),
            'username': user.username,
            'role': role
        }, status=status.HTTP_200_OK)






# DIRECTOR VIEWS
class BranchViewSet(viewsets.ModelViewSet):
    """
    Director/Manager API for managing branches.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/branches/ - List all branches
    - POST /api/branches/ - Create new branch
    - GET /api/branches/{id}/ - Retrieve branch
    - PUT /api/branches/{id}/ - Update branch
    - DELETE /api/branches/{id}/ - Delete branch
    - POST /api/branches/{id}/open/ - Open branch
    - POST /api/branches/{id}/close/ - Close branch
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter branches by user's center"""
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'SuperAdmin':
                    return Branch.objects.all()
                return Branch.objects.filter(educational_center=profile.educational_center)
            except UserProfile.DoesNotExist:
                return Branch.objects.all()
        return Branch.objects.all()

    @action(detail=True, methods=['post'])
    def open(self, request, pk=None):
        """Open branch"""
        branch = self.get_object()
        branch.status = 'Open'
        branch.save()
        return Response({'status': 'Branch opened'})

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Close branch"""
        branch = self.get_object()
        branch.status = 'Closed'
        branch.save()
        return Response({'status': 'Branch closed'})


class SubjectViewSet(viewsets.ModelViewSet):
    """
    Director API for managing subjects/courses.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/subjects/ - List all subjects
    - POST /api/subjects/ - Create new subject
    - GET /api/subjects/{id}/ - Retrieve subject
    - PUT /api/subjects/{id}/ - Update subject
    - PATCH /api/subjects/{id}/ - Partial update
    - DELETE /api/subjects/{id}/ - Delete subject
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter subjects by user's center"""
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'SuperAdmin':
                    return Subject.objects.all()
                return Subject.objects.filter(educational_center=profile.educational_center)
            except UserProfile.DoesNotExist:
                return Subject.objects.all()
        return Subject.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
    """
    Director API for managing groups/classes.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/groups/ - List all groups
    - POST /api/groups/ - Create new group
    - GET /api/groups/{id}/ - Retrieve group
    - PUT /api/groups/{id}/ - Update group
    - PATCH /api/groups/{id}/ - Partial update
    - DELETE /api/groups/{id}/ - Delete group
    - GET /api/groups/{id}/statistics/ - Get group statistics
    - GET /api/groups/{id}/attendance-report/ - Get attendance report
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter groups by user's center"""
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'SuperAdmin':
                    return Group.objects.all()
                return Group.objects.filter(educational_center=profile.educational_center)
            except UserProfile.DoesNotExist:
                return Group.objects.all()
        return Group.objects.all()

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get group statistics"""
        group = self.get_object()
        return Response({
            'students_count': group.students.count(),
            'lessons_count': group.lessons.count(),
            'average_attendance': self._calculate_avg_attendance(group),
            'payment_status': self._get_payment_status(group)
        })

    @action(detail=True, methods=['get'])
    def attendance_report(self, request, pk=None):
        """Get attendance report for group"""
        group = self.get_object()
        attendances = Attendance.objects.filter(lesson__group=group)
        return Response({
            'total_lessons': group.lessons.count(),
            'total_attendances': attendances.count(),
            'present_count': attendances.filter(status='Present').count(),
            'absent_count': attendances.filter(status='Absent').count(),
            'late_count': attendances.filter(status='Late').count(),
        })

    def _calculate_avg_attendance(self, group):
        """Calculate average attendance"""
        attendances = Attendance.objects.filter(lesson__group=group)
        if not attendances.exists():
            return 0
        present = attendances.filter(status='Present').count()
        return (present / attendances.count()) * 100 if attendances.count() > 0 else 0

    def _get_payment_status(self, group):
        """Get payment status for group"""
        payments = Payment.objects.filter(group=group)
        total = sum(p.amount for p in payments)
        return {'total_payments': total, 'payment_count': payments.count()}


# class StudentViewSet(viewsets.ModelViewSet):
#     """
#     Director/Manager/Admin API for managing students.

#     Authentication: IsAuthenticated

#     ENDPOINTS:
#     - GET /api/students/ - List all students
#     - POST /api/students/ - Create new student
#     - GET /api/students/{id}/ - Retrieve student
#     - PUT /api/students/{id}/ - Update student
#     - PATCH /api/students/{id}/ - Partial update
#     - DELETE /api/students/{id}/ - Delete student
#     - POST /api/students/{id}/block/ - Block student
#     - POST /api/students/{id}/assign-group/ - Assign student to group
#     - GET /api/students/{id}/attendance-history/ - Get attendance history
#     - GET /api/students/{id}/payment-history/ - Get payment history
#     """
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     # PRODUCTION: Uncomment line below and comment AllowAny line
#     # permission_classes = [permissions.IsAuthenticated]
#     permission_classes = [permissions.AllowAny]

#     def get_queryset(self):
#         """Filter students by user's center/branch"""
#         user = self.request.user
#         if user.is_authenticated:
#             try:
#                 profile = UserProfile.objects.get(user=user)
#                 if profile.role == 'SuperAdmin':
#                     return Student.objects.all()
#                 elif profile.role in ['Director', 'Manager']:
#                     return Student.objects.filter(branch__educational_center=profile.educational_center)
#                 return Student.objects.filter(user=user)
#             except UserProfile.DoesNotExist:
#                 return Student.objects.all()
#         return Student.objects.all()

#     @action(detail=True, methods=['post'])
#     def block(self, request, pk=None):
#         """Block student"""
#         student = self.get_object()
#         student.status = 'Blocked'
#         student.save()
#         return Response({'status': 'Student blocked'})

#     @action(detail=True, methods=['post'])
#     def assign_group(self, request, pk=None):
#         """Assign student to group"""
#         student = self.get_object()
#         group_id = request.data.get('group_id')
#         try:
#             group = Group.objects.get(id=group_id)
#             student.group = group
#             student.save()
#             return Response({'status': 'Student assigned to group'})
#         except Group.DoesNotExist:
#             return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

#     @action(detail=True, methods=['get'])
#     def attendance_history(self, request, pk=None):
#         """Get student attendance history"""
#         student = self.get_object()
#         attendances = Attendance.objects.filter(student=student).values('status').annotate(count=Count('id'))
#         return Response(list(attendances))

#     @action(detail=True, methods=['get'])
#     def payment_history(self, request, pk=None):
#         """Get student payment history"""
#         student = self.get_object()
#         payments = Payment.objects.filter(student=student)
#         serializer = PaymentSerializer(payments, many=True)
#         return Response(serializer.data)





class StudentViewSet(viewsets.ModelViewSet):
    """
    API for managing students.

    ENDPOINTS:
    - GET /api/students/ - List all students
    - POST /api/students/ - Create new student
    - GET /api/students/{id}/ - Retrieve student
    - PUT /api/students/{id}/ - Update student
    - PATCH /api/students/{id}/ - Partial update
    - DELETE /api/students/{id}/ - Delete student
    - POST /api/students/{id}/block/ - Block student
    - POST /api/students/{id}/assign-group/ - Assign student to group
    - GET /api/students/{id}/attendance-history/ - Get attendance history
    - GET /api/students/{id}/payment-history/ - Get payment history
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]  # productionda IsAuthenticated qilinadi

    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        """Block student"""
        student = self.get_object()
        student.status = 'Blocked'
        student.save()
        return Response({'status': 'Student blocked'})

    @action(detail=True, methods=['post'])
    def assign_group(self, request, pk=None):
        """Assign student to group"""
        student = self.get_object()
        group_id = request.data.get('group_id')
        if not group_id:
            return Response({'error': 'group_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            group = Group.objects.get(id=group_id)
            student.group = group
            student.save()
            return Response({'status': f'Student assigned to group {group.name}'})
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def attendance_history(self, request, pk=None):
        """Get student attendance history"""
        student = self.get_object()
        attendances = Attendance.objects.filter(student=student).values('is_present').annotate(count=Count('id'))
        # Formatlash
        history = [{'present': a['is_present'], 'count': a['count']} for a in attendances]
        return Response(history)

    @action(detail=True, methods=['get'])
    def payment_history(self, request, pk=None):
        """Get student payment history"""
        student = self.get_object()
        payments = Payment.objects.filter(student=student)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)





# class TeacherViewSet(viewsets.ModelViewSet):
#     """
#     Director/Manager API for managing teachers.

#     Authentication: IsAuthenticated

#     ENDPOINTS:
#     - GET /api/teachers/ - List all teachers
#     - POST /api/teachers/ - Create new teacher
#     - GET /api/teachers/{id}/ - Retrieve teacher
#     - PUT /api/teachers/{id}/ - Update teacher
#     - PATCH /api/teachers/{id}/ - Partial update
#     - DELETE /api/teachers/{id}/ - Delete teacher
#     - POST /api/teachers/{id}/rate/ - Rate teacher performance
#     - GET /api/teachers/{id}/schedule/ - Get teacher schedule
#     - GET /api/teachers/{id}/performance/ - Get performance metrics
#     """
#     queryset = Teacher.objects.all()
#     serializer_class = TeacherSerializer
#     # PRODUCTION: Uncomment line below and comment AllowAny line
#     # permission_classes = [permissions.IsAuthenticated]
#     permission_classes = [permissions.AllowAny]

#     def get_queryset(self):
#         """Filter teachers by user's center"""
#         user = self.request.user
#         if user.is_authenticated:
#             try:
#                 profile = UserProfile.objects.get(user=user)
#                 if profile.role == 'SuperAdmin':
#                     return Teacher.objects.all()
#                 return Teacher.objects.filter(branch__educational_center=profile.educational_center)
#             except UserProfile.DoesNotExist:
#                 return Teacher.objects.all()
#         return Teacher.objects.all()

#     @action(detail=True, methods=['post'])
#     def rate(self, request, pk=None):
#         """Rate teacher performance"""
#         teacher = self.get_object()
#         rating = request.data.get('rating', 0)
#         if 0 <= float(rating) <= 5:
#             teacher.performance_rating = rating
#             teacher.save()
#             return Response({'status': 'Teacher rated', 'rating': rating})
#         return Response({'error': 'Invalid rating'}, status=status.HTTP_400_BAD_REQUEST)

#     @action(detail=True, methods=['get'])
#     def schedule(self, request, pk=None):
#         """Get teacher schedule"""
#         teacher = self.get_object()
#         lessons = Lesson.objects.filter(teacher=teacher).order_by('date', 'start_time')
#         serializer = LessonSerializer(lessons, many=True)
#         return Response(serializer.data)

#     @action(detail=True, methods=['get'])
#     def performance(self, request, pk=None):
#         """Get teacher performance metrics"""
#         teacher = self.get_object()
#         lessons = teacher.lessons.count()
#         attendances = Attendance.objects.filter(marked_by=teacher)
#         assignments = teacher.assignments.count()
#         exams = teacher.exams.count()

#         return Response({
#             'lessons_count': lessons,
#             'attendances_marked': attendances.count(),
#             'assignments_given': assignments,
#             'exams_conducted': exams,
#             'performance_rating': teacher.performance_rating
#         })





from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Teacher, UserProfile, Lesson, Attendance
from .serializers import TeacherSerializer, LessonSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    """
    Director/Manager API for managing teachers.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.AllowAny]  # PRODUCTION: IsAuthenticated

    def get_queryset(self):
        """Filter teachers by user's center"""
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'SuperAdmin':
                    return Teacher.objects.all()
                return Teacher.objects.filter(branch__educational_center=profile.educational_center)
            except UserProfile.DoesNotExist:
                return Teacher.objects.all()
        return Teacher.objects.all()

    def create(self, request, *args, **kwargs):
        """Create a new teacher and ensure DB save"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        """Rate teacher performance"""
        teacher = self.get_object()
        try:
            rating = float(request.data.get('rating', 0))
        except (ValueError, TypeError):
            return Response({'error': 'Invalid rating'}, status=status.HTTP_400_BAD_REQUEST)

        if 0 <= rating <= 5:
            teacher.performance_rating = rating
            teacher.save()
            return Response({'status': 'Teacher rated', 'rating': rating})
        return Response({'error': 'Rating must be between 0 and 5'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        """Get teacher schedule"""
        teacher = self.get_object()
        lessons = Lesson.objects.filter(teacher=teacher).order_by('date', 'start_time')
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        """Get teacher performance metrics"""
        teacher = self.get_object()
        lessons_count = teacher.lessons.count()
        attendances_count = Attendance.objects.filter(marked_by=teacher).count()
        assignments_count = teacher.assignments.count()
        exams_count = teacher.exams.count()

        return Response({
            'lessons_count': lessons_count,
            'attendances_marked': attendances_count,
            'assignments_given': assignments_count,
            'exams_conducted': exams_count,
            'performance_rating': teacher.performance_rating
        })






class LessonViewSet(viewsets.ModelViewSet):
    """
    Director/Teacher API for managing lessons.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/lessons/ - List all lessons
    - POST /api/lessons/ - Create new lesson
    - GET /api/lessons/{id}/ - Retrieve lesson
    - PUT /api/lessons/{id}/ - Update lesson
    - PATCH /api/lessons/{id}/ - Partial update
    - DELETE /api/lessons/{id}/ - Delete lesson
    - POST /api/lessons/{id}/cancel/ - Cancel lesson
    - POST /api/lessons/{id}/generate-online-link/ - Generate online meeting link
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter lessons by user's role"""
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'SuperAdmin':
                    return Lesson.objects.all()
                elif profile.role in ['Director', 'Manager']:
                    return Lesson.objects.filter(group__branch__educational_center=profile.educational_center)
                elif profile.role == 'Teacher':
                    teacher = Teacher.objects.get(user=user)
                    return Lesson.objects.filter(teacher=teacher)
            except (UserProfile.DoesNotExist, Teacher.DoesNotExist):
                return Lesson.objects.all()
        return Lesson.objects.all()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel lesson"""
        lesson = self.get_object()
        lesson.is_cancelled = True
        lesson.save()
        return Response({'status': 'Lesson cancelled'})

    @action(detail=True, methods=['post'])
    def generate_online_link(self, request, pk=None):
        """Generate online meeting link"""
        lesson = self.get_object()
        import uuid
        online_link = f"https://meet.example.com/{uuid.uuid4().hex[:10]}"
        lesson.online_link = online_link
        lesson.save()
        return Response({'online_link': online_link})


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    Teacher/Admin API for managing attendance.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/attendance/ - List all attendance records
    - POST /api/attendance/ - Mark attendance
    - GET /api/attendance/{id}/ - Retrieve attendance record
    - PUT /api/attendance/{id}/ - Update attendance
    - PATCH /api/attendance/{id}/ - Partial update
    - DELETE /api/attendance/{id}/ - Delete attendance
    - POST /api/attendance/bulk-mark/ - Bulk mark attendance for lesson
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter attendance by user's role"""
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'SuperAdmin':
                    return Attendance.objects.all()
                elif profile.role in ['Director', 'Manager', 'Admin']:
                    return Attendance.objects.filter(lesson__group__branch__educational_center=profile.educational_center)
                elif profile.role == 'Teacher':
                    teacher = Teacher.objects.get(user=user)
                    return Attendance.objects.filter(marked_by=teacher)
                elif profile.role == 'Student':
                    student = Student.objects.get(user=user)
                    return Attendance.objects.filter(student=student)
            except (UserProfile.DoesNotExist, Teacher.DoesNotExist, Student.DoesNotExist):
                return Attendance.objects.all()
        return Attendance.objects.all()

    @action(detail=False, methods=['post'])
    def bulk_mark(self, request):
        """Bulk mark attendance for lesson"""
        lesson_id = request.data.get('lesson_id')
        attendance_data = request.data.get('attendance_data', [])

        try:
            lesson = Lesson.objects.get(id=lesson_id)
            marked_count = 0

            for record in attendance_data:
                student_id = record.get('student_id')
                status_val = record.get('status', 'Absent')

                try:
                    student = Student.objects.get(id=student_id)
                    attendance, created = Attendance.objects.update_or_create(
                        lesson=lesson,
                        student=student,
                        defaults={
                            'status': status_val,
                            'marked_by': request.user
                        }
                    )
                    marked_count += 1
                except Student.DoesNotExist:
                    continue

            return Response({
                'status': 'Attendance marked',
                'marked_count': marked_count
            })
        except Lesson.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    Admin/Director API for managing payments.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/payments/ - List all payments
    - POST /api/payments/ - Create new payment
    - GET /api/payments/{id}/ - Retrieve payment
    - PUT /api/payments/{id}/ - Update payment
    - PATCH /api/payments/{id}/ - Partial update
    - DELETE /api/payments/{id}/ - Delete payment
    - GET /api/payments/student/{student_id}/history/ - Get student payment history
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter payments by user's center"""
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'SuperAdmin':
                    return Payment.objects.all()
                elif profile.role in ['Director', 'Manager', 'Admin']:
                    return Payment.objects.filter(student__branch__educational_center=profile.educational_center)
            except UserProfile.DoesNotExist:
                return Payment.objects.all()
        return Payment.objects.all()


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    Teacher API for managing assignments.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/assignments/ - List all assignments
    - POST /api/assignments/ - Create new assignment
    - GET /api/assignments/{id}/ - Retrieve assignment
    - PUT /api/assignments/{id}/ - Update assignment
    - PATCH /api/assignments/{id}/ - Partial update
    - DELETE /api/assignments/{id}/ - Delete assignment
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter assignments by user's role"""
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'SuperAdmin':
                    return Assignment.objects.all()
                elif profile.role in ['Director', 'Manager']:
                    return Assignment.objects.filter(group__branch__educational_center=profile.educational_center)
                elif profile.role == 'Teacher':
                    teacher = Teacher.objects.get(user=user)
                    return Assignment.objects.filter(teacher=teacher)
            except (UserProfile.DoesNotExist, Teacher.DoesNotExist):
                return Assignment.objects.all()
        return Assignment.objects.all()


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    """
    Student/Teacher API for managing assignment submissions.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/submissions/ - List all submissions
    - POST /api/submissions/ - Submit assignment
    - GET /api/submissions/{id}/ - Retrieve submission
    - PUT /api/submissions/{id}/ - Update submission
    - DELETE /api/submissions/{id}/ - Delete submission
    - POST /api/submissions/{id}/grade/ - Grade submission
    """
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['post'])
    def grade(self, request, pk=None):
        """Grade submission"""
        submission = self.get_object()
        grade = request.data.get('grade')
        comment = request.data.get('comment', '')

        submission.grade = grade
        submission.comment = comment
        submission.graded_at = timezone.now()
        submission.save()

        return Response({'status': 'Submission graded', 'grade': grade})


class ExamViewSet(viewsets.ModelViewSet):
    """
    Teacher API for managing exams.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/exams/ - List all exams
    - POST /api/exams/ - Create new exam
    - GET /api/exams/{id}/ - Retrieve exam
    - PUT /api/exams/{id}/ - Update exam
    - PATCH /api/exams/{id}/ - Partial update
    - DELETE /api/exams/{id}/ - Delete exam
    - POST /api/exams/{id}/publish-results/ - Publish exam results
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter exams by user's role"""
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'SuperAdmin':
                    return Exam.objects.all()
                elif profile.role in ['Director', 'Manager']:
                    return Exam.objects.filter(group__branch__educational_center=profile.educational_center)
                elif profile.role == 'Teacher':
                    teacher = Teacher.objects.get(user=user)
                    return Exam.objects.filter(teacher=teacher)
            except (UserProfile.DoesNotExist, Teacher.DoesNotExist):
                return Exam.objects.all()
        return Exam.objects.all()

    @action(detail=True, methods=['post'])
    def publish_results(self, request, pk=None):
        """Publish exam results"""
        exam = self.get_object()
        exam.results_published = True
        exam.save()
        return Response({'status': 'Results published'})


class ExamResultViewSet(viewsets.ModelViewSet):
    """
    Student/Teacher API for managing exam results.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/exam-results/ - List all exam results
    - POST /api/exam-results/ - Create exam result
    - GET /api/exam-results/{id}/ - Retrieve exam result
    - PUT /api/exam-results/{id}/ - Update exam result
    - PATCH /api/exam-results/{id}/ - Partial update
    - DELETE /api/exam-results/{id}/ - Delete exam result
    """
    queryset = ExamResult.objects.all()
    serializer_class = ExamResultSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter exam results by user's role"""
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'SuperAdmin':
                    return ExamResult.objects.all()
                elif profile.role in ['Director', 'Manager']:
                    return ExamResult.objects.filter(exam__group__branch__educational_center=profile.educational_center)
                elif profile.role == 'Student':
                    student = Student.objects.get(user=user)
                    return ExamResult.objects.filter(student=student)
            except (UserProfile.DoesNotExist, Student.DoesNotExist):
                return ExamResult.objects.all()
        return ExamResult.objects.all()


class RoomViewSet(viewsets.ModelViewSet):
    """
    Director/Manager API for managing rooms/classrooms.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/rooms/ - List all rooms
    - POST /api/rooms/ - Create new room
    - GET /api/rooms/{id}/ - Retrieve room
    - PUT /api/rooms/{id}/ - Update room
    - PATCH /api/rooms/{id}/ - Partial update
    - DELETE /api/rooms/{id}/ - Delete room
    - POST /api/rooms/{id}/occupy/ - Mark room as occupied
    - POST /api/rooms/{id}/free/ - Mark room as free
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter rooms by user's center"""
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'SuperAdmin':
                    return Room.objects.all()
                elif profile.role in ['Director', 'Manager']:
                    return Room.objects.filter(branch__educational_center=profile.educational_center)
            except UserProfile.DoesNotExist:
                return Room.objects.all()
        return Room.objects.all()

    @action(detail=True, methods=['post'])
    def occupy(self, request, pk=None):
        """Mark room as occupied"""
        room = self.get_object()
        room.is_available = False
        room.save()
        return Response({'status': 'Room occupied'})

    @action(detail=True, methods=['post'])
    def free(self, request, pk=None):
        """Mark room as free"""
        room = self.get_object()
        room.is_available = True
        room.save()
        return Response({'status': 'Room freed'})


class PayrollViewSet(viewsets.ModelViewSet):
    """
    Director/Admin API for managing teacher payroll.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/payroll/ - List all payroll records
    - POST /api/payroll/ - Create payroll record
    - GET /api/payroll/{id}/ - Retrieve payroll record
    - PUT /api/payroll/{id}/ - Update payroll record
    - PATCH /api/payroll/{id}/ - Partial update
    - DELETE /api/payroll/{id}/ - Delete payroll record
    - GET /api/payroll/teacher/{teacher_id}/history/ - Get teacher payroll history
    """
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter payroll by user's center"""
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'SuperAdmin':
                    return Payroll.objects.all()
                elif profile.role in ['Director', 'Manager', 'Admin']:
                    return Payroll.objects.filter(teacher__branch__educational_center=profile.educational_center)
            except UserProfile.DoesNotExist:
                return Payroll.objects.all()
        return Payroll.objects.all()


class NotificationViewSet(viewsets.ModelViewSet):
    """
    API for managing notifications.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/notifications/ - List all notifications
    - POST /api/notifications/ - Create notification
    - GET /api/notifications/{id}/ - Retrieve notification
    - DELETE /api/notifications/{id}/ - Delete notification
    - POST /api/notifications/{id}/mark-read/ - Mark as read
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter notifications by user"""
        user = self.request.user
        if user.is_authenticated:
            return Notification.objects.filter(user=user)
        return Notification.objects.none()

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'Notification marked as read'})

# class UserViewSet(viewsets.ModelViewSet):
#     """User management"""
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]





from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer

# =========================
# UserViewSet - CRUD
# =========================
class UserViewSet(viewsets.ModelViewSet):
    """
    User management (CRUD)
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # productionda shu ishlatilsin

    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        """Block user"""
        user = self.get_object()
        profile = getattr(user, 'profile', None)
        if profile:
            profile.is_blocked = True
            profile.save()
            return Response({'status': 'User blocked'})
        return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def unblock(self, request, pk=None):
        """Unblock user"""
        user = self.get_object()
        profile = getattr(user, 'profile', None)
        if profile:
            profile.is_blocked = False
            profile.save()
            return Response({'status': 'User unblocked'})
        return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)


# =========================
# Login API
# =========================
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_api(request):
    """
    Login API for JWT token.
    POST data: {"username": "user", "password": "pass"}
    Returns: access token, refresh token, role
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    # JWT token yaratish
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Foydalanuvchi roli
    try:
        profile = user.profile
        role = profile.role
    except UserProfile.DoesNotExist:
        role = None

    return Response({
        'access': access_token,
        'refresh': str(refresh),
        'username': user.username,
        'role': role
    }, status=status.HTTP_200_OK)







class ContractViewSet(viewsets.ModelViewSet):
    """
    Director/Admin API for managing contracts.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/contracts/ - List all contracts
    - POST /api/contracts/ - Create contract
    - GET /api/contracts/{id}/ - Retrieve contract
    - PUT /api/contracts/{id}/ - Update contract
    - PATCH /api/contracts/{id}/ - Partial update
    - DELETE /api/contracts/{id}/ - Delete contract
    - GET /api/contracts/{id}/download/ - Download contract PDF
    """
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter contracts by user's center"""
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'SuperAdmin':
                    return Contract.objects.all()
                elif profile.role in ['Director', 'Manager', 'Admin']:
                    return Contract.objects.filter(student__branch__educational_center=profile.educational_center)
            except UserProfile.DoesNotExist:
                return Contract.objects.all()
        return Contract.objects.all()


class LeadViewSet(viewsets.ModelViewSet):
    """
    Marketing/Director API for managing leads.

    Authentication: IsAuthenticated

    ENDPOINTS:
    - GET /api/leads/ - List all leads
    - POST /api/leads/ - Create new lead
    - GET /api/leads/{id}/ - Retrieve lead
    - PUT /api/leads/{id}/ - Update lead
    - PATCH /api/leads/{id}/ - Partial update
    - DELETE /api/leads/{id}/ - Delete lead
    - POST /api/leads/{id}/convert-to-student/ - Convert lead to student
    - GET /api/leads/source/{source}/statistics/ - Get statistics by source
    """
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    # PRODUCTION: Uncomment line below and comment AllowAny line
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter leads by user's center"""
        user = self.request.user
        if user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'SuperAdmin':
                    return Lead.objects.all()
                elif profile.role in ['Director', 'Manager']:
                    return Lead.objects.filter(branch__educational_center=profile.educational_center)
            except UserProfile.DoesNotExist:
                return Lead.objects.all()
        return Lead.objects.all()

    @action(detail=True, methods=['post'])
    def convert_to_student(self, request, pk=None):
        """Convert lead to student"""
        lead = self.get_object()
        student = Student.objects.create(
            first_name=lead.first_name,
            last_name=lead.last_name,
            email=lead.email,
            phone=lead.phone,
            branch=lead.branch
        )
        lead.status = 'Converted'
        lead.save()
        return Response({'status': 'Lead converted to student', 'student_id': student.id})

    @action(detail=False, methods=['get'])
    def source_statistics(self, request):
        """Get statistics by lead source"""
        leads_by_source = Lead.objects.values('source').annotate(count=Count('id'))
        return Response(list(leads_by_source))
