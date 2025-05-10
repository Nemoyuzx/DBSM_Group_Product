from django.http import JsonResponse
from django.apps import apps
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

def api_person_search(request):
    """简单的API接口用于搜索人员"""
    query = request.GET.get('q', '')
    if not query or len(query) < 2:
        return JsonResponse({'results': []})
        
    people = Person.objects.filter(legal_name__icontains=query)[:10]
    results = [{'id': p.person_id, 'name': p.legal_name} for p in people]
    return JsonResponse({'results': results})

def api_table_counts(request):
    """获取各个数据表的记录数量"""
    # 定义要统计的模型列表
    models_to_count = {
        'Person': Person,
        'Student': Student,
        'Staff': Staff,
        'Course': Course,
        'Department': Department,
        'Program': Program,
        'CourseOffering': CourseOffering,
        'Address': Address,
        'Institution': Institution,
        'Term': Term,
        'AcademicRank': AcademicRank,
        'InstructorRole': InstructorRole,
        'AdminPosition': AdminPosition,
        'AdminRole': AdminRole,
        'NameHistory': NameHistory,
        'AccommodationType': AccommodationType,
        'DisabilityAccommodation': DisabilityAccommodation,
        'ProgramAffiliation': ProgramAffiliation,
        'StudentProgram': StudentProgram,
        'Class': Class,
        'StudentClass': StudentClass,
        'ClassAdvisor': ClassAdvisor,
        'CourseRequisite': CourseRequisite,
        'TeachAssignment': TeachAssignment,
        'ClassCoursePlan': ClassCoursePlan,
        'Enrollment': Enrollment,
        'EnrollmentOverride': EnrollmentOverride,
        'AssessmentItem': AssessmentItem,
        'AssessmentSubmission': AssessmentSubmission,
        'AssessmentFeedback': AssessmentFeedback,
        'GradeAppeal': GradeAppeal,
        'LeaveReason': LeaveReason,
        'LeaveOfAbsence': LeaveOfAbsence,
        'ExchangeEnrollment': ExchangeEnrollment,
        'TransferredCredit': TransferredCredit,
        'CourseWaiverRequest': CourseWaiverRequest,
        'InstructorLeave': InstructorLeave,
        'AcademicIncident': AcademicIncident,
        'Competency': Competency,
        'StudentCompetency': StudentCompetency,
        'LearningEvent': LearningEvent,
        'ProjectTeam': ProjectTeam,
        'TeamMember': TeamMember,
    }
    
    # 统计每个模型的记录数量
    counts = {}
    for model_name, model in models_to_count.items():
        counts[model_name] = model.objects.count()
    
    # 按照类别分组
    categories = {
        '人员与地址': ['Person', 'Student', 'Staff', 'Address', 'NameHistory', 'RewardPunish'],
        '学术组织': ['Department', 'Program', 'Institution', 'Term', 'AcademicRank', 'InstructorRole', 'AdminPosition', 'AdminRole'],
        '课程体系': ['Course', 'CourseOffering', 'CourseRequisite', 'TeachAssignment'],
        '班级管理': ['Class', 'StudentClass', 'ClassAdvisor', 'ClassCoursePlan'],
        '注册与成绩': ['Enrollment', 'EnrollmentOverride', 'AssessmentItem', 'AssessmentSubmission', 'AssessmentFeedback', 'GradeAppeal'],
        '学籍与合规': ['LeaveReason', 'LeaveOfAbsence', 'ExchangeEnrollment', 'TransferredCredit', 'CourseWaiverRequest', 'InstructorLeave', 'AcademicIncident'],
        '创新与能力': ['Competency', 'StudentCompetency', 'LearningEvent', 'ProjectTeam', 'TeamMember'],
    }
    
    # 构建分类结果
    categorized_counts = {}
    for category, models in categories.items():
        categorized_counts[category] = {model: counts.get(model, 0) for model in models if model in counts}
    
    return JsonResponse({
        'counts': counts,
        'categorized_counts': categorized_counts
    })
