from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class Class(models.Model):
    name = models.CharField(max_length=255)
    grade = models.IntegerField()

    def __str__(self):
        return self.name


class Student(models.Model):
    stu_id = models.CharField(
        max_length=8,
        primary_key=True,
        unique=True,
        validators=[RegexValidator(r'^\d{8}$')],
        verbose_name="Mã học sinh"
    )
    name = models.CharField(max_length=255, verbose_name="Tên học sinh")
    dob = models.DateField(verbose_name="Ngày sinh")
    grade_level = models.IntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(12)],
        verbose_name="Khối"
    )
    classroom = models.CharField(max_length=255, verbose_name="Lớp học")

    def __str__(self):
        return f"{self.name} - {self.dob} - {self.grade_level} - {self.classroom} - {self.stu_id}"

    class Meta:
        verbose_name = "Học sinh"
        verbose_name_plural = "Học sinh"


class Score(models.Model):
    SCORE_TYPES = [
        ('15m', '15 phút'),
        ('hk', 'Học kỳ'),
        ('thi', 'Thi'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Học sinh")
    subject = models.CharField(max_length=255, verbose_name="Môn học")
    score = models.FloatField(verbose_name="Điểm")
    score_type = models.CharField(max_length=10, choices=SCORE_TYPES, default='15m', verbose_name="Loại điểm")

    def __str__(self):
        return f"{self.student.name} - {self.subject} - {self.score}"
