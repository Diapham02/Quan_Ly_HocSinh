from django.contrib import admin
from django.urls import path
from ..App import views  # Import views.py từ thư mục App

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_student/', views.add_student, name='add_student'),
    path('edit_student/<int:pk>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:pk>/', views.delete_student, name='delete_student'),
    path('import_students/', views.import_students, name='import_students'),
    # Thêm các URL cho các chức năng khác nếu cần...
]
