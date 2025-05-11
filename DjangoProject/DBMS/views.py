from django.http import JsonResponse
from django.apps import apps
import datetime
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

def api_table_data(request, table_name):
    """根据表名获取表数据"""
    try:
        # 添加调试信息
        print(f"正在尝试获取表 {table_name} 的数据")
        
        # 尝试不区分大小写获取模型
        try:
            model = apps.get_model('DBMS', table_name)
        except LookupError:
            # 如果找不到，尝试首字母大写，其余小写的形式
            try:
                model = apps.get_model('DBMS', table_name.capitalize())
            except LookupError:
                # 列出所有可用的模型，帮助调试
                available_models = list(apps.app_configs['DBMS'].models.keys())
                print(f"可用模型: {available_models}")
                
                # 查找名称相似的模型（不区分大小写比较）
                similar_models = [m for m in available_models if m.lower() == table_name.lower()]
                if similar_models:
                    print(f"找到相似模型: {similar_models}")
                    model = apps.get_model('DBMS', similar_models[0])
                else:
                    return JsonResponse({
                        'error': f'表 {table_name} 不存在', 
                        'available_models': available_models
                    }, status=404)
        
        # 获取数据
        data = model.objects.all()[:100]  # 限制返回数量
        
        # 准备返回数据
        rows = []
        for item in data:
            # 将模型实例转换为字典
            row = {}
            for field in item._meta.fields:
                field_name = field.name
                field_value = getattr(item, field_name)
                # 处理外键和日期类型
                if field.is_relation:
                    field_value = str(field_value)
                elif isinstance(field_value, (datetime.date, datetime.datetime)):
                    field_value = field_value.isoformat()
                row[field_name] = field_value
            rows.append(row)
        
        # 获取列名
        columns = [f.name for f in model._meta.fields]
        
        return JsonResponse({
            'table': table_name,
            'columns': columns,
            'rows': rows
        })
    except Exception as e:
        import traceback
        print(f"获取表数据时发生错误: {e}")
        print(traceback.format_exc())
        return JsonResponse({'error': str(e), 'traceback': traceback.format_exc()}, status=500)
