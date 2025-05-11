from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import (
    Person, Student, Staff, Course, Department, Program,
    CourseOffering, Address, Institution, Term, AcademicRank,
    InstructorRole, AdminPosition, AdminRole, NameHistory,
    AccommodationType, DisabilityAccommodation, ProgramAffiliation,
    StudentProgram, Class, StudentClass, ClassAdvisor, CourseRequisite,
    TeachAssignment, ClassCoursePlan, Enrollment, EnrollmentOverride,
    AssessmentItem, AssessmentSubmission, AssessmentFeedback, GradeAppeal,
    LeaveReason, LeaveOfAbsence, ExchangeEnrollment, TransferredCredit,
    CourseWaiverRequest, InstructorLeave, AcademicIncident, Competency,
    StudentCompetency, LearningEvent, ProjectTeam, TeamMember
)
from .serializers import (
    PersonSerializer, StudentSerializer, StaffSerializer, CourseSerializer,
    DepartmentSerializer, ProgramSerializer, CourseOfferingSerializer,
    AddressSerializer, InstitutionSerializer, TermSerializer,
    AcademicRankSerializer, InstructorRoleSerializer, AdminPositionSerializer,
    AdminRoleSerializer, NameHistorySerializer, AccommodationTypeSerializer,
    DisabilityAccommodationSerializer, ProgramAffiliationSerializer,
    StudentProgramSerializer, ClassSerializer, StudentClassSerializer,
    ClassAdvisorSerializer, CourseRequisiteSerializer, TeachAssignmentSerializer,
    ClassCoursePlanSerializer, EnrollmentSerializer, EnrollmentOverrideSerializer,
    AssessmentItemSerializer, AssessmentSubmissionSerializer,
    AssessmentFeedbackSerializer, GradeAppealSerializer, LeaveReasonSerializer,
    LeaveOfAbsenceSerializer, ExchangeEnrollmentSerializer,
    TransferredCreditSerializer, CourseWaiverRequestSerializer,
    InstructorLeaveSerializer, AcademicIncidentSerializer, CompetencySerializer,
    StudentCompetencySerializer, LearningEventSerializer, ProjectTeamSerializer,
    TeamMemberSerializer
)

# 基础视图集类，提供通用的CRUD操作
class BaseModelViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

# 人员与地址层视图集
class AddressViewSet(BaseModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    search_fields = ['line1', 'city', 'province', 'country']
    ordering_fields = ['city', 'province', 'country']

class PersonViewSet(BaseModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    search_fields = ['legal_name', 'preferred_name', 'email', 'national_id']
    ordering_fields = ['legal_name', 'birth_date']
    
    @action(detail=True, methods=['get'])
    def full_info(self, request, pk=None):
        person = self.get_object()
        data = self.get_serializer(person).data
        
        # 尝试获取学生信息
        try:
            student = Student.objects.get(student_id=person.person_id)
            data['student'] = StudentSerializer(student).data
        except Student.DoesNotExist:
            data['student'] = None
            
        # 尝试获取教职工信息
        try:
            staff = Staff.objects.get(staff_id=person.person_id)
            data['staff'] = StaffSerializer(staff).data
        except Staff.DoesNotExist:
            data['staff'] = None
            
        return Response(data)

class StudentViewSet(BaseModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    search_fields = ['student_id__legal_name', 'enrollment_status']
    ordering_fields = ['admission_year', 'enrollment_status']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        # 获取关联的Person信息
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class StaffViewSet(BaseModelViewSet):
    queryset = Staff.objects.all().select_related('staff_id').order_by('staff_id')  # 添加select_related优化查询
    serializer_class = StaffSerializer
    search_fields = ['staff_id__legal_name', 'employment_type', 'staff_status']
    ordering_fields = ['hire_date', 'staff_status']

# 学术组织层视图集
class DepartmentViewSet(BaseModelViewSet):
    queryset = Department.objects.all().order_by('dept_id')  # 添加默认排序
    serializer_class = DepartmentSerializer
    search_fields = ['name', 'office_location']
    ordering_fields = ['name']

class ProgramViewSet(BaseModelViewSet):
    queryset = Program.objects.all().order_by('program_id')  # 添加默认排序
    serializer_class = ProgramSerializer
    search_fields = ['name', 'degree_type']
    ordering_fields = ['name', 'degree_type']

class InstitutionViewSet(BaseModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    search_fields = ['name', 'type']
    ordering_fields = ['name']

class TermViewSet(BaseModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    search_fields = ['term_code', 'description']
    ordering_fields = ['start_date']

class AcademicRankViewSet(BaseModelViewSet):
    queryset = AcademicRank.objects.all()
    serializer_class = AcademicRankSerializer
    search_fields = ['rank_name']
    ordering_fields = ['rank_id']

class InstructorRoleViewSet(BaseModelViewSet):
    queryset = InstructorRole.objects.all()
    serializer_class = InstructorRoleSerializer

class AdminPositionViewSet(BaseModelViewSet):
    queryset = AdminPosition.objects.all()
    serializer_class = AdminPositionSerializer
    search_fields = ['title']
    ordering_fields = ['level']

class AdminRoleViewSet(BaseModelViewSet):
    queryset = AdminRole.objects.all()
    serializer_class = AdminRoleSerializer

class NameHistoryViewSet(BaseModelViewSet):
    queryset = NameHistory.objects.all()
    serializer_class = NameHistorySerializer
    search_fields = ['old_name', 'new_name']
    ordering_fields = ['effective_to']

class AccommodationTypeViewSet(BaseModelViewSet):
    queryset = AccommodationType.objects.all()
    serializer_class = AccommodationTypeSerializer
    search_fields = ['acc_type', 'description']

class DisabilityAccommodationViewSet(BaseModelViewSet):
    queryset = DisabilityAccommodation.objects.all()
    serializer_class = DisabilityAccommodationSerializer
    search_fields = ['note']
    ordering_fields = ['active_from']

# 课程体系层视图集
class CourseViewSet(BaseModelViewSet):
    queryset = Course.objects.all().order_by('course_code')  # 添加默认排序
    serializer_class = CourseSerializer
    search_fields = ['course_code', 'title']
    ordering_fields = ['title', 'credit_value']
    
    @action(detail=True, methods=['get'])
    def offerings(self, request, pk=None):
        course = self.get_object()
        offerings = CourseOffering.objects.filter(course_code=course)
        serializer = CourseOfferingSerializer(offerings, many=True)
        return Response(serializer.data)

class CourseOfferingViewSet(BaseModelViewSet):
    queryset = CourseOffering.objects.all()
    serializer_class = CourseOfferingSerializer
    search_fields = ['section_number', 'campus']
    ordering_fields = ['term_code', 'section_number']

class CourseRequisiteViewSet(BaseModelViewSet):
    queryset = CourseRequisite.objects.all()
    serializer_class = CourseRequisiteSerializer

class TeachAssignmentViewSet(BaseModelViewSet):
    queryset = TeachAssignment.objects.all()
    serializer_class = TeachAssignmentSerializer
    search_fields = ['role']

# 班级相关视图集
class ClassViewSet(BaseModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    search_fields = ['class_name', 'cohort_year']
    ordering_fields = ['cohort_year', 'class_name']

class StudentClassViewSet(BaseModelViewSet):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer

class ClassAdvisorViewSet(BaseModelViewSet):
    queryset = ClassAdvisor.objects.all()
    serializer_class = ClassAdvisorSerializer
    search_fields = ['advisor_role']

class ClassCoursePlanViewSet(BaseModelViewSet):
    queryset = ClassCoursePlan.objects.all()
    serializer_class = ClassCoursePlanSerializer

# 注册与成绩层视图集
class EnrollmentViewSet(BaseModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    search_fields = ['enroll_state']
    ordering_fields = ['enroll_date']

class EnrollmentOverrideViewSet(BaseModelViewSet):
    queryset = EnrollmentOverride.objects.all()
    serializer_class = EnrollmentOverrideSerializer
    search_fields = ['override_type', 'reason']

class AssessmentItemViewSet(BaseModelViewSet):
    queryset = AssessmentItem.objects.all()
    serializer_class = AssessmentItemSerializer
    search_fields = ['item_name']
    ordering_fields = ['due_datetime']

class AssessmentSubmissionViewSet(BaseModelViewSet):
    queryset = AssessmentSubmission.objects.all()
    serializer_class = AssessmentSubmissionSerializer
    ordering_fields = ['submit_time']

class AssessmentFeedbackViewSet(BaseModelViewSet):
    queryset = AssessmentFeedback.objects.all()
    serializer_class = AssessmentFeedbackSerializer
    search_fields = ['feedback_type']

class GradeAppealViewSet(BaseModelViewSet):
    queryset = GradeAppeal.objects.all()
    serializer_class = GradeAppealSerializer
    search_fields = ['decision', 'appeal_reason']
    ordering_fields = ['appeal_date']

# 学籍与合规层视图集
class LeaveReasonViewSet(BaseModelViewSet):
    queryset = LeaveReason.objects.all()
    serializer_class = LeaveReasonSerializer
    search_fields = ['reason_code', 'description']

class LeaveOfAbsenceViewSet(BaseModelViewSet):
    queryset = LeaveOfAbsence.objects.all()
    serializer_class = LeaveOfAbsenceSerializer
    search_fields = ['approval_status', 'description']

class ExchangeEnrollmentViewSet(BaseModelViewSet):
    queryset = ExchangeEnrollment.objects.all()
    serializer_class = ExchangeEnrollmentSerializer
    search_fields = ['status', 'host_program']

class TransferredCreditViewSet(BaseModelViewSet):
    queryset = TransferredCredit.objects.all()
    serializer_class = TransferredCreditSerializer
    search_fields = ['host_course_code']

class CourseWaiverRequestViewSet(BaseModelViewSet):
    queryset = CourseWaiverRequest.objects.all()
    serializer_class = CourseWaiverRequestSerializer
    search_fields = ['reason_type', 'decision']
    ordering_fields = ['request_date']

class InstructorLeaveViewSet(BaseModelViewSet):
    queryset = InstructorLeave.objects.all()
    serializer_class = InstructorLeaveSerializer
    search_fields = ['leave_type']

class AcademicIncidentViewSet(BaseModelViewSet):
    queryset = AcademicIncident.objects.all()
    serializer_class = AcademicIncidentSerializer
    search_fields = ['incident_type', 'status']
    ordering_fields = ['report_date']

# 创新与能力层视图集
class CompetencyViewSet(BaseModelViewSet):
    queryset = Competency.objects.all()
    serializer_class = CompetencySerializer
    search_fields = ['description']

class StudentCompetencyViewSet(BaseModelViewSet):
    queryset = StudentCompetency.objects.all()
    serializer_class = StudentCompetencySerializer
    search_fields = ['competency_level']
    ordering_fields = ['verify_date']

class LearningEventViewSet(BaseModelViewSet):
    queryset = LearningEvent.objects.all()
    serializer_class = LearningEventSerializer
    search_fields = ['event_type']
    ordering_fields = ['timestamp']

class ProjectTeamViewSet(BaseModelViewSet):
    queryset = ProjectTeam.objects.all()
    serializer_class = ProjectTeamSerializer
    search_fields = ['project_title']

class TeamMemberViewSet(BaseModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    search_fields = ['role_in_team']
    ordering_fields = ['join_date']

class ProgramAffiliationViewSet(BaseModelViewSet):
    queryset = ProgramAffiliation.objects.all()
    serializer_class = ProgramAffiliationSerializer
    search_fields = ['affiliation_type']
    ordering_fields = ['program', 'dept']

class StudentProgramViewSet(BaseModelViewSet):
    queryset = StudentProgram.objects.all()
    serializer_class = StudentProgramSerializer
    search_fields = ['is_primary_major']
    ordering_fields = ['start_term', 'end_term']