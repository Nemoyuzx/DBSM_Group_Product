from django.http import JsonResponse
from .models import (
    Person, Student, Staff, Course, Department, Program,
    CourseOffering, Address, Institution
)

def api_person_search(request):
    """简单的API接口用于搜索人员"""
    query = request.GET.get('q', '')
    if not query or len(query) < 2:
        return JsonResponse({'results': []})
        
    people = Person.objects.filter(legal_name__icontains=query)[:10]
    results = [{'id': p.person_id, 'name': p.legal_name} for p in people]
    return JsonResponse({'results': results})
