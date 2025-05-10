from rest_framework import serializers
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

# 基础序列化器
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student_id.legal_name', read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff_id.legal_name', read_only=True)
    
    class Meta:
        model = Staff
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseOfferingSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course_code.title', read_only=True)
    
    class Meta:
        model = CourseOffering
        fields = '__all__'

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = '__all__'

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'

class AcademicRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicRank
        fields = '__all__'

class InstructorRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorRole
        fields = '__all__'

class AdminPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPosition
        fields = '__all__'

class AdminRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRole
        fields = '__all__'

class NameHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NameHistory
        fields = '__all__'

class AccommodationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationType
        fields = '__all__'

class DisabilityAccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisabilityAccommodation
        fields = '__all__'

class ProgramAffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramAffiliation
        fields = '__all__'

class StudentProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProgram
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = '__all__'

class ClassAdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassAdvisor
        fields = '__all__'

class CourseRequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRequisite
        fields = '__all__'

class TeachAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachAssignment
        fields = '__all__'

class ClassCoursePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassCoursePlan
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class EnrollmentOverrideSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentOverride
        fields = '__all__'

class AssessmentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentItem
        fields = '__all__'

class AssessmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentSubmission
        fields = '__all__'

class AssessmentFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentFeedback
        fields = '__all__'

class GradeAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeAppeal
        fields = '__all__'

class LeaveReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveReason
        fields = '__all__'

class LeaveOfAbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveOfAbsence
        fields = '__all__'

class ExchangeEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeEnrollment
        fields = '__all__'

class TransferredCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferredCredit
        fields = '__all__'

class CourseWaiverRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseWaiverRequest
        fields = '__all__'

class InstructorLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorLeave
        fields = '__all__'

class AcademicIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicIncident
        fields = '__all__'

class CompetencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Competency
        fields = '__all__'

class StudentCompetencySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCompetency
        fields = '__all__'

class LearningEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningEvent
        fields = '__all__'

class ProjectTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTeam
        fields = '__all__'

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'