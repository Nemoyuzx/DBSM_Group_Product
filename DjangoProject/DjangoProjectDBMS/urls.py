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
from django.urls import path
from DBMS import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('persons/', views.person_list, name='person_list'),
    path('persons/<int:person_id>/', views.person_detail, name='person_detail'),
    path('students/', views.student_list, name='student_list'),
    path('staffs/', views.staff_list, name='staff_list'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<str:course_code>/', views.course_detail, name='course_detail'),
    path('departments/', views.department_list, name='department_list'),
    path('programs/', views.program_list, name='program_list'),
    path('api/persons/search/', views.api_person_search, name='api_person_search'),
]
