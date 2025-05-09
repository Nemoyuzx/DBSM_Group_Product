from django.shortcuts import render
from django.http import JsonResponse
from .models import (
    Person, Student, Staff, Course, Department, Program,
    CourseOffering, Address, Institution
)

def index(request):
    """首页，显示简单统计数据"""
    stats = {
        'people_count': Person.objects.count(),
        'student_count': Student.objects.count(),
        'staff_count': Staff.objects.count(),
        'course_count': Course.objects.count(),
        'department_count': Department.objects.count(),
        'program_count': Program.objects.count(),
    }
    return render(request, 'DBMS/index.html', {'stats': stats})

def person_list(request):
    """人员列表页"""
    people = Person.objects.all()[:50]  # 限制显示50条，避免数据过多
    return render(request, 'DBMS/person_list.html', {'people': people})

def student_list(request):
    """学生列表页"""
    students = Student.objects.select_related('student_id').all()[:50]
    return render(request, 'DBMS/student_list.html', {'students': students})

def staff_list(request):
    """教职工列表页"""
    staffs = Staff.objects.select_related('staff_id').all()[:50]
    return render(request, 'DBMS/staff_list.html', {'staffs': staffs})

def course_list(request):
    """课程列表页"""
    courses = Course.objects.all()[:50]
    return render(request, 'DBMS/course_list.html', {'courses': courses})

def department_list(request):
    """部门列表页"""
    departments = Department.objects.all()
    return render(request, 'DBMS/department_list.html', {'departments': departments})

def program_list(request):
    """项目列表页"""
    programs = Program.objects.all()
    return render(request, 'DBMS/program_list.html', {'programs': programs})

def person_detail(request, person_id):
    """人员详情页"""
    try:
        person = Person.objects.get(person_id=person_id)
        # 检查是否是学生或教职工
        student = None
        staff = None
        try:
            student = Student.objects.get(student_id=person_id)
        except Student.DoesNotExist:
            pass
            
        try:
            staff = Staff.objects.get(staff_id=person_id)
        except Staff.DoesNotExist:
            pass
            
        return render(request, 'DBMS/person_detail.html', {
            'person': person,
            'student': student,
            'staff': staff
        })
    except Person.DoesNotExist:
        return JsonResponse({'error': 'Person not found'}, status=404)

def course_detail(request, course_code):
    """课程详情页"""
    try:
        course = Course.objects.get(course_code=course_code)
        offerings = CourseOffering.objects.filter(course_code=course)
        return render(request, 'DBMS/course_detail.html', {
            'course': course,
            'offerings': offerings
        })
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)

def api_person_search(request):
    """简单的API接口用于搜索人员"""
    query = request.GET.get('q', '')
    if not query or len(query) < 2:
        return JsonResponse({'results': []})
        
    people = Person.objects.filter(legal_name__icontains=query)[:10]
    results = [{'id': p.person_id, 'name': p.legal_name} for p in people]
    return JsonResponse({'results': results})
