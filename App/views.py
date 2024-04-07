from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
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
            return render(request, "students/add_student.html")

        if Student.objects.filter(stu_id=stu_id).exists():
            messages.error(request, "Mã học sinh đã tồn tại. Vui lòng nhập lại mã học sinh khác.")
            return render(request, "students/add_student.html")

        student = Student(stu_id=stu_id, name=name, dob=dob, grade_level=grade_level, classroom=classroom)
        try:
            student.full_clean()
        except ValidationError as e:
            messages.error(request, "Dữ liệu không hợp lệ: " + str(e))
            return render(request, "students/add_student.html")

        student.save()
        messages.success(request, "Thêm học sinh thành công!")

        # Redirect or render a template here...
        return redirect("list_students")

    else:
        return render(request, "students/add_student.html")


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
    return render(request, "students/edit_student.html", {'form': form, 'pk': pk})


def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Xóa học sinh thành công!")
        return redirect("list_students")
    return render(request, 'students/delete_student.html', {'pk': pk})


def list_students(request):
    students = Student.objects.all()
    student_info = None
    if request.method == 'POST':
        stu_id = request.POST.get('stu_id')
        if stu_id:
            try:
                student_info = Student.objects.get(stu_id=stu_id)
            except Student.DoesNotExist:
                messages.error(request, 'Không tìm thấy học sinh với mã học sinh đã cho.')
    return render(request, 'students/list_students.html', {'students': students, 'student_info': student_info})


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
            messages.error(request, form.errors)
    else:
        form = ScoreForm()
    return render(request, 'scores/add_score.html', {'form': form})


def edit_score(request, pk):
    score = Score.objects.get(pk=pk)
    if request.method == "POST":
        form = ScoreForm(request.POST, instance=score)
        if form.is_valid():
            form.save()
            return redirect('manage_scores')
    else:
        form = ScoreForm(instance=score)
    return render(request, 'scores/edit_score.html', {'form': form})


def delete_score(request, pk):
    score = Score.objects.get(pk=pk)
    if request.method == 'POST':
        score.delete()
        return redirect('list_scores')
    return render(request, 'scores/delete_score.html', {'score': score})


def calculate_average(request, stu_id):
    student_scores = Score.objects.filter(student__stu_id=stu_id)
    average_score = student_scores.aggregate(Avg('score'))
    return render(request, 'scores/average_score.html', {'average_score': average_score})


def list_scores(request):
    scores = Score.objects.all()
    return render(request, 'scores/list_scores.html', {'scores': scores})


def manage_scores(request):
    if request.method == 'POST':
        # Xử lý form thêm điểm
        student_id = request.POST.get('student')
        subject = request.POST.get('subject')
        score_type = request.POST.get('score_type')
        score_value = request.POST.get('score_value')

        # Kiểm tra xem score_value có phải là một số không âm không và có nằm trong khoảng từ 0 đến 10 không
        if not 0 <= float(score_value) <= 10:
            messages.error(request, "Điểm phải là một số từ 0 đến 10.")
            return redirect(reverse('manage_scores'))

        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            messages.error(request, "Không tìm thấy học sinh với mã đã cho.")
            return redirect(reverse('manage_scores'))

        Score.objects.create(
            student=student,
            subject=subject,
            score_type=score_type,
            score_value=score_value
        )

        return redirect(reverse('manage_scores'))

    else:
        # Hiển thị form thêm điểm và danh sách điểm
        students = Student.objects.all()
        scores = Score.objects.all()

        context = {
            'students': students,
            'scores': scores,
        }

        return render(request, 'scores/manage_scores.html', context)


################
# TRA CUU DIEM #
################
def search_score(request):
    student_name = request.GET.get('studentName')
    scores = []
    if student_name:
        student = get_object_or_404(Student, name=student_name)
        scores = Score.objects.filter(student=student)
    return render(request, 'scores/search_score.html', {'scores': scores})
