from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models


class Student(models.Model):
    code = models.CharField(max_length=250)
    username = models.CharField(max_length=250)
    firstname = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    email = models.EmailField()
    course = models.CharField(max_length=250)
    year = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    cpassword = models.CharField(max_length=250)
    is_saved = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)  # Default to False

    def __str__(self):
        return self.username


class Teacher(models.Model):
    teachername = models.CharField(max_length=250)
    firstname = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    password = models.CharField(max_length=250)
    cpassword = models.CharField(max_length=250)
    is_saved = models.BooleanField(default=False)

    def __str__(self):
        return self.teachername


class MCA_student(models.Model):
    code = models.CharField(max_length=250)
    username = models.CharField(max_length=250)


class MSc_student(models.Model):
    code = models.CharField(max_length=250)
    username = models.CharField(max_length=250)


class MCA_firstyear_student(models.Model):
    code = models.CharField(max_length=250)
    username = models.CharField(max_length=250)


class MCA_secondyear_student(models.Model):
    code = models.CharField(max_length=250)
    username = models.CharField(max_length=250)


class MSc_firstyear_student(models.Model):
    code = models.CharField(max_length=250)
    username = models.CharField(max_length=250)


class MSc_secondyear_student(models.Model):
    code = models.CharField(max_length=250)
    username = models.CharField(max_length=250)


class Course(models.Model):
    name = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='subjects')

    def __str__(self):
        return self.name


class SubjectAllotment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subject_allotments')
    students = models.ManyToManyField(Student, related_name='subject_allotments')

    def __str__(self):
        return f"{self.course.name} - {self.subject.name} - {self.teacher.teachername if self.teacher else 'Not allotted'}"


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    attendance = models.IntegerField()
    assignment = models.IntegerField()
    seminar = models.IntegerField()
    test1 = models.IntegerField()
    test2 = models.IntegerField()
    total_marks = models.IntegerField()
    marks_saved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student} - {self.subject}'


class Notification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Feedback(models.Model):
    student_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    internal_marks = models.IntegerField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.student_name


class ElectiveSubject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ElectiveCourse(models.Model):
    course = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    elective_subjects = models.ManyToManyField(ElectiveSubject)

    def __str__(self):
        return f"{self.course}"


class ElectiveSubjectAllotment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    elective_subjects = models.ManyToManyField(ElectiveSubject)

    def __str__(self):
        return f"Allotment for {self.teacher}"


class StudentRegistration(models.Model):
    username = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(ElectiveCourse, on_delete=models.CASCADE)
    semester = models.IntegerField()
    elective_subject = models.ManyToManyField(ElectiveSubject)  # Use ManyToManyField for elective subjects

    def __str__(self):
        return self.username.username


class ElectiveMarks(models.Model):
    student = models.ForeignKey(StudentRegistration, on_delete=models.CASCADE,unique=True)
    elective_subject = models.ForeignKey(ElectiveSubject, on_delete=models.CASCADE)
    attendance = models.IntegerField()
    assignment = models.IntegerField()
    seminar = models.IntegerField()
    test1 = models.IntegerField()
    test2 = models.IntegerField()
    total_elective_marks = models.IntegerField()
    elective_marks_saved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student} - {self.elective_subject}'


class Send_Feedback(models.Model):
    teacher_name = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.teacher_name
