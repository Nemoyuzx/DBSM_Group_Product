from decimal import Decimal
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
from .models import Person  # ...existing imports...
import datetime

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
    # 嵌套 PersonSerializer，展示并写入关联的 Person 信息
    person = PersonSerializer(source='person_id')
    # 支持前端扁平提交更新姓名
    student_name = serializers.CharField(source='person_id.legal_name', required=False)
    # 嵌套 AddressSerializer，展示并写入关联的 Address
    address = AddressSerializer(source='person_id.primary_address_id')
    class Meta:
        model = Student
        fields = '__all__'
        extra_kwargs = {
            'person_id': {'read_only': True}
        }
    
    def update(self, instance, validated_data):
        # 弹出前端提交的 student_name 字段
        new_name = validated_data.pop('student_name', None)
        # 更新 Student 自身字段
        instance = super().update(instance, validated_data)
        # 如提供新的 姓名，则更新关联的 Person 模型
        if new_name is not None:
            person = instance.person_id
            person.legal_name = new_name
            person.save()
        return instance

    def create(self, validated_data):
        # 提取嵌套的 Person (包含 address)
        person_data = validated_data.pop('person', {}) or {}
        address_data = validated_data.pop('address', {}) or {}
        # 创建 Address
        address = Address.objects.create(**address_data)
        # 准备 Person 数据
        person_data['primary_address_id'] = address
        # 从 validated_data 获取 student_id
        student_id = validated_data.get('student_id')
        person_data.setdefault('person_id', student_id)
        # 创建 Person
        person = Person.objects.create(**person_data)
        # 设置 Student 默认字段
        validated_data.setdefault('expected_grad_term', '')
        validated_data.setdefault('disability_flag', False)
        # 创建 Student 并关联 Person
        student = Student.objects.create(person_id=person, **validated_data)
        return student

class StaffSerializer(serializers.ModelSerializer):
    # 使用person_id.legal_name，支持读写；设置为非必填
    staff_name = serializers.CharField(source='person_id.legal_name', required=False)
    
    class Meta:
        model = Staff
        fields = '__all__'
        extra_kwargs = {
            'person_id': {'read_only': True}
        }
    
    def update(self, instance, validated_data):
        # 更新Staff自身字段
        new_name = validated_data.pop('staff_name', None)
        instance = super().update(instance, validated_data)
        if new_name is not None:
            person = instance.person_id
            person.legal_name = new_name
            person.save()
        return instance
    
    def create(self, validated_data):
        # 提取 staff_name 并移除重复的 person_id
        new_name = validated_data.pop('staff_name', None)
        validated_data.pop('person_id', None)
        # 从 validated_data 获取 staff_id
        staff_id = validated_data.get('staff_id')
        # 获取或创建 Person
        defaults = {
            'legal_name': new_name or staff_id,
            'preferred_name': new_name or staff_id,
            'sex_at_birth': 'U',
            'birth_date': datetime.date.today(),
            'national_id': staff_id,
            'phone_number': staff_id,
            'email': f"{staff_id}@example.com"
        }
        person, created = Person.objects.get_or_create(person_id=staff_id, defaults=defaults)
        if not created and new_name:
            person.legal_name = new_name
            person.save()
        # 创建Staff并关联Person
        staff = Staff.objects.create(person_id=person, **validated_data)
        return staff

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        extra_kwargs = {
            'dept_id': {'read_only': True}
        }
    def create(self, validated_data):
        # 默认关联第一个 Institution
        from .models import Institution
        inst = Institution.objects.first()
        if inst:
            validated_data['inst_id'] = inst
        # chair_staff_id 可选，默认 None
        validated_data.setdefault('chair_staff_id', None)
        return super().create(validated_data)

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'
        extra_kwargs = {
            'program_id': {'read_only': True}
        }
    def create(self, validated_data):
        # 设置默认的credit_required和gpa_min_required
        validated_data.setdefault('credit_required', 0)
        validated_data.setdefault('gpa_min_required', Decimal('0.00'))
        return super().create(validated_data)

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        
    def validate_credit_value(self, value):
        # 确保使用 Decimal 类型进行验证
        if value < Decimal('0.0'):
            raise serializers.ValidationError("学分值不能为负数")
        return value

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