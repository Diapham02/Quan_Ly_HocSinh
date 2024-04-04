from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('admin/', admin.site.urls),
    # Quan li hoc sinh
    path('add_student/', views.add_student, name='add_student'),
    path('edit_student/<int:pk>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:pk>/', views.delete_student, name='delete_student'),
    path('view_students/', views.list_students, name='list_students'),  # Changed from 'students/' to 'view_students/'
    # Quan li diem
    path('add_score/', views.add_score, name='add_score'),
    path('edit_score/<int:pk>/', views.edit_score, name='edit_score'),
    path('delete_score/<int:pk>/', views.delete_score, name='delete_score'),
    path('calculate_average/<str:stu_id>/', views.calculate_average, name='calculate_average'),
    path('list_scores/', views.list_scores, name='list_scores'),
    # Tra cuu diem
    path('search_score/', views.search_score, name='search_score'),
]
