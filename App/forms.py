from django import forms
from .models import Student, Score


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['stu_id', 'name', 'dob', 'grade_level', 'classroom']
        labels = {
            'stu_id': 'Mã học sinh',
            'name': 'Tên học sinh',
            'dob': 'Ngày sinh',
            'grade_level': 'Khối',
            'classroom': 'Lớp học',
        }


class ImportStudentForm(forms.Form):
    file = forms.FileField()


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = '__all__'
