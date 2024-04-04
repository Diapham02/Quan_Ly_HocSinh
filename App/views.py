from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404

from .forms import StudentForm, ScoreForm
from .models import Student, Score


####################
# QUAN LY HOC SINH #
####################
def home_page(request):
    stu_id = request.POST.get('stu_id')
    students = Student.objects.filter(stu_id=stu_id)
    return render(request, 'home.html', {'students': students})


def add_student(request):
    if request.method == "POST":
        stu_id = request.POST.get('stu_id')
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        grade_level = request.POST.get('grade_level')
        classroom = request.POST.get('classroom')

        # Validate data here...
        if not stu_id or not name or not dob or not grade_level or not classroom:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin!")
            return render(request, "add_student.html")

        if Student.objects.filter(stu_id=stu_id).exists():
            messages.error(request, "Mã học sinh đã tồn tại. Vui lòng nhập lại mã học sinh khác.")
            return render(request, "add_student.html")

        student = Student(stu_id=stu_id, name=name, dob=dob, grade_level=grade_level, classroom=classroom)
        try:
            student.full_clean()
        except ValidationError as e:
            messages.error(request, "Dữ liệu không hợp lệ: " + str(e))
            return render(request, "add_student.html")

        student.save()
        messages.success(request, "Thêm học sinh thành công!")

        # Redirect or render a template here...
        return redirect("list_students")

    else:
        return render(request, "add_student.html")


def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Sửa học sinh thành công!")
            return redirect("list_students")
    else:
        form = StudentForm(instance=student)
    return render(request, "edit_student.html", {'form': form, 'pk': pk})


def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Xóa học sinh thành công!")
        return redirect("list_students")
    return render(request, 'delete_student.html', {'pk': pk})


def list_students(request):
    students = Student.objects.all()
    return render(request, 'list_students.html', {'students': students})


################
# QUAN LY DIEM #
################
def add_score(request):
    if request.method == "POST":
        form = ScoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_scores')
    else:
        form = ScoreForm()
    return render(request, 'add_score.html', {'form': form})


def edit_score(request, pk):
    score = Score.objects.get(pk=pk)
    if request.method == "POST":
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            form.save()
            return redirect('list_scores')
    else:
        form = ScoreForm(instance=score)
    return render(request, 'edit_score.html', {'form': form})


def delete_score(request, pk):
    score = Score.objects.get(pk=pk)
    if request.method == 'POST':
        score.delete()
        return redirect('list_scores')
    return render(request, 'delete_score.html', {'score': score})


def calculate_average(request, stu_id):
    student_scores = Score.objects.filter(student__stu_id=stu_id)
    average_score = student_scores.aggregate(Avg('score'))
    return render(request, 'average_score.html', {'average_score': average_score})


def list_scores(request):
    scores = Score.objects.all()
    return render(request, 'list_scores.html', {'scores': scores})


################
# TRA CUU DIEM #
################
def search_score(request):
    stu_id = request.POST.get('stu_id')
    student = Student.objects.get(stu_id=stu_id)
    scores = Score.objects.filter(student__stu_id=stu_id)
    return render(request, 'search_score.html', {'student': student, 'scores': scores})
