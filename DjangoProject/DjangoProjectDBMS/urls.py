"""
URL configuration for DjangoProjectDBMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from DBMS import views
from DBMS import api_views

# 创建API路由器
router = DefaultRouter()
router.register(r'persons', api_views.PersonViewSet)
router.register(r'students', api_views.StudentViewSet)
router.register(r'staffs', api_views.StaffViewSet)
router.register(r'courses', api_views.CourseViewSet)
router.register(r'departments', api_views.DepartmentViewSet)
router.register(r'programs', api_views.ProgramViewSet)
router.register(r'addresses', api_views.AddressViewSet)
router.register(r'institutions', api_views.InstitutionViewSet)
router.register(r'terms', api_views.TermViewSet)
router.register(r'academic-ranks', api_views.AcademicRankViewSet)
router.register(r'instructor-roles', api_views.InstructorRoleViewSet)
router.register(r'admin-positions', api_views.AdminPositionViewSet)
router.register(r'admin-roles', api_views.AdminRoleViewSet)
router.register(r'name-histories', api_views.NameHistoryViewSet)
router.register(r'accommodation-types', api_views.AccommodationTypeViewSet)
router.register(r'disability-accommodations', api_views.DisabilityAccommodationViewSet)
router.register(r'program-affiliations', api_views.ProgramAffiliationViewSet)
router.register(r'student-programs', api_views.StudentProgramViewSet)
router.register(r'classes', api_views.ClassViewSet)
router.register(r'student-classes', api_views.StudentClassViewSet)
router.register(r'class-advisors', api_views.ClassAdvisorViewSet)
router.register(r'course-requisites', api_views.CourseRequisiteViewSet)
router.register(r'teach-assignments', api_views.TeachAssignmentViewSet)
router.register(r'class-course-plans', api_views.ClassCoursePlanViewSet)
router.register(r'enrollments', api_views.EnrollmentViewSet)
router.register(r'enrollment-overrides', api_views.EnrollmentOverrideViewSet)
router.register(r'assessment-items', api_views.AssessmentItemViewSet)
router.register(r'assessment-submissions', api_views.AssessmentSubmissionViewSet)
router.register(r'assessment-feedbacks', api_views.AssessmentFeedbackViewSet)
router.register(r'grade-appeals', api_views.GradeAppealViewSet)
router.register(r'leave-reasons', api_views.LeaveReasonViewSet)
router.register(r'leaves-of-absence', api_views.LeaveOfAbsenceViewSet)
router.register(r'exchange-enrollments', api_views.ExchangeEnrollmentViewSet)
router.register(r'transferred-credits', api_views.TransferredCreditViewSet)
router.register(r'course-waiver-requests', api_views.CourseWaiverRequestViewSet)
router.register(r'instructor-leaves', api_views.InstructorLeaveViewSet)
router.register(r'academic-incidents', api_views.AcademicIncidentViewSet)
router.register(r'competencies', api_views.CompetencyViewSet)
router.register(r'student-competencies', api_views.StudentCompetencyViewSet)
router.register(r'learning-events', api_views.LearningEventViewSet)
router.register(r'project-teams', api_views.ProjectTeamViewSet)
router.register(r'team-members', api_views.TeamMemberViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API路由
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    
    # 保留API搜索接口
    path('api/persons/search/', views.api_person_search, name='api_person_search'),
    
    # 添加数据表统计API
    path('api/table-counts/', views.api_table_counts, name='api_table_counts'),
    
    # 添加根路径处理，重定向到API根路径
    path('', lambda request: JsonResponse({'message': 'API服务正常运行', 'endpoints': '/api/'})),
]
