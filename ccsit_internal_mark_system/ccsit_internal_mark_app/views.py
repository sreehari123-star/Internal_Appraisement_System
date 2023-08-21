import json
from functools import wraps

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sessions.backends.db import SessionStore
from django.urls import reverse
from prompt_toolkit.validation import ValidationError
from .models import Student, ElectiveSubject, ElectiveMarks

from ccsit_internal_mark_app.forms import CourseForm, MarksForm, FeedbackForm, ElectiveCourseForm, ElectiveMarksForm, \
    Send_Feedback_Form
from ccsit_internal_mark_app.models import Student, Teacher, MCA_student, MCA_firstyear_student, \
    MCA_secondyear_student, MSc_student, MSc_firstyear_student, MSc_secondyear_student, Course, Subject, \
    SubjectAllotment, Marks, Notification, Feedback, ElectiveSubjectAllotment, StudentRegistration, ElectiveCourse, \
    Send_Feedback

# Create your views here.

def login_required_customss(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.session.get('admin'):
            return redirect('admin_login')  # Redirect to the login page
        return view_func(request, *args, **kwargs)
    return wrapped_view


def login_required_custom(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.session.get('username'):
            return redirect('student_login')  # Redirect to the login page
        return view_func(request, *args, **kwargs)
    return wrapped_view


def add_elective_course(request):
    if request.method == 'POST':
        form = ElectiveCourseForm(request.POST)
        if form.is_valid():
            # Process the comma-separated input and save each subject as a separate entry in the database
            subjects = [subject.strip() for subject in form.cleaned_data['elective_subjects'].split(',')]
            course = form.save(commit=False)
            course.save()
            for subject in subjects:
                course.elective_subjects.create(name=subject)
            return redirect('admin_home')  # Replace 'success_page' with the name of the success page URL pattern
    else:
        form = ElectiveCourseForm()

    return render(request, 'add_elective_course.html', {'form': form})


@login_required_customss
def elective_subject_allotment(request):
    teachers = Teacher.objects.all()

    if request.method == 'POST':
        selected_elective_subjects = request.POST.getlist('selected_elective_subjects')
        teacher_id = request.POST['teacher']

        teacher = get_object_or_404(Teacher, id=teacher_id)

        # Delete existing allotments
        existing_allotments = ElectiveSubjectAllotment.objects.filter(teacher=teacher)
        existing_allotments.delete()

        # Create a new ElectiveSubjectAllotment instance
        elective_subject_allotment = ElectiveSubjectAllotment.objects.create(teacher=teacher)

        # Set the elective subjects for the allotment using .set()
        elective_subject_allotment.elective_subjects.set(selected_elective_subjects)

        # Redirect to a success page or do something else
        return render(request, 'elective_subject_allotment.html')
    else:
        elective_courses = ElectiveCourse.objects.all()
        return render(request, 'elective_subject_allotment.html', {'elective_courses': elective_courses, 'teachers': teachers})


@login_required_custom
def student_registration(request):
    # Retrieve the student's username from the session
    # student_username = request.session.get('student_username')
    student_username = request.session.get('username')

    if not student_username:
        # If student is not logged in, redirect to a login page or show an error message
        return render(request, 'student_login.html', {'error_message': "You are not logged in."})

    student = Student.objects.get(username=student_username)

    if request.method == 'POST':
        username = request.POST.get('username')
        course = request.POST.get('course')
        semester = int(request.POST.get('semester'))
        elective_subject_ids = request.POST.getlist('elective_subject')  # List of selected subject IDs

        # Fetch the student based on the username
        student = Student.objects.get(username=username)

        matching_courses = ElectiveCourse.objects.filter(course=course)

        elective_subjects_objs = ElectiveSubject.objects.filter(id__in=elective_subject_ids)

        # Check if the student registration already exists for the selected course and semester
        existing_registration = StudentRegistration.objects.filter(username=student, course__in=matching_courses,
                                                                   semester=semester)

        if not existing_registration.exists():
            registration = StudentRegistration.objects.create(
                username=student,
                course=matching_courses[0],  # Assuming only one course per student per semester
                semester=semester
            )
            registration.elective_subject.set(elective_subjects_objs)  # Associate selected subjects

        return redirect('student_home')  # Replace with your success page URL pattern

    else:
        courses = ElectiveCourse.objects.all()
        elective_subjects = ElectiveSubject.objects.all()
        return render(request, 'student_registration.html',
                      {'student': student, 'courses': courses, 'elective_subjects': elective_subjects})


def about(request):
    return render(request,'about.html')


def course(request):
    courses = Course.objects.all()
    subjects = Subject.objects.all()
    subject_allot = SubjectAllotment.objects.all()
    context = {
        'courses' : courses,
        'subjects' : subjects,
        'subject_allot' : subject_allot
    }
    return render(request,'course.html',context)


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_home')  # Redirect to the admin feedback view
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form})


def admin_feedback(request):
    feedback_list = Feedback.objects.all().order_by('-timestamp')
    return render(request, 'admin_feedback.html', {'feedback_list': feedback_list})


def send_notification(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Notification.objects.create(title=title, content=content)
        return redirect('home')  # Assuming the URL name for the home page is 'home'

    # notifications = Notification.objects.all()  # Fetch all notifications from the database
    # print(notifications)  # Add this line to check if notifications are being fetched
    return render(request, 'notification_form.html')


def login_required_customs(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.session.get('teachername'):
            return redirect('teacher_login')  # Redirect to the login page
        return view_func(request, *args, **kwargs)
    return wrapped_view


def home(request):
    notifications = Notification.objects.all()  # Fetch all notifications from the database
    subject_allot = SubjectAllotment.objects.all()
    courses = Course.objects.all()
    subjects = Subject.objects.all()
    total_teachers = Teacher.objects.count()
    total_students = Student.objects.count()
    online_students = Student.objects.filter(is_online=True).count()
    offline_students = total_students - online_students
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'online_students': online_students,
        'offline_students': offline_students,
        'courses': courses,
        'subjects': subjects,
        'subject_allot': subject_allot,
        'notifications': notifications
    }
    return render(request,'home.html',context)


def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            students = Student.objects.filter(username=username)  # Use filter() instead of get()
            if students.exists():  # Check if any students match the query
                for student in students:
                    if student.is_saved:
                        if student.password == password:
                            request.session['username'] = username
                            return redirect('student_home')
                        else:
                            messages.info(request, 'Invalid username or password.')
                            return render(request, 'student_login.html')
                    else:
                        messages.info(request, 'Your account is not approved yet.')
                        return render(request, 'student_login.html')
            else:
                messages.info(request, 'Invalid username or password.')
                return render(request, 'student_login.html')

        except Student.DoesNotExist:
            messages.info(request, 'Invalid username or password.')
            return render(request, 'student_login.html')

    return render(request, 'student_login.html')


@login_required_custom
def student_home(request):
    subject_allot = SubjectAllotment.objects.all()
    courses = Course.objects.all()
    subjects = Subject.objects.all()
    total_teachers = Teacher.objects.count()
    total_students = Student.objects.count()
    online_students = Student.objects.filter(is_online=True).count()
    offline_students = total_students - online_students
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'online_students': online_students,
        'offline_students': offline_students,
        'courses': courses,
        'subjects':subjects,
        'subject_allot':subject_allot
    }
    return render(request,'student_home.html',context)


def logout(request):
    auth.logout(request)
    return redirect('/')


def admin_login(request):
    if request.method == 'POST':
        admin_name = request.POST['admin_name']
        password = request.POST['password']

        if admin_name == 'admin' and password == '1234':
            request.session['admin'] = True
            return redirect('admin_home')
        else:
            messages.info(request,'Invalid username or password.')
            return render(request, 'admin_login.html')

    return render(request,'admin_login.html')


@login_required_customss
def admin_home(request):
    elective_course = ElectiveCourse.objects.all()
    elective_allot = ElectiveSubject.objects.all()
    courses = Course.objects.all()
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()
    is_logged_in = True  # Assume the decorator has already checked for login status
    subject_allot = SubjectAllotment.objects.all()
    total_teachers = Teacher.objects.count()
    total_students = Student.objects.count()
    online_students = Student.objects.filter(is_online=True).count()
    offline_students = total_students - online_students
    return render(request, 'admin_home.html', {'teachers': teachers,'is_logged_in':is_logged_in,'courses':courses,'subjects':subjects,'elective_course':elective_course,'elective_allot':elective_allot,'subject_allot':subject_allot,
                                               'total_teachers':total_teachers,'total_students':total_students,'offline_students':offline_students})


@login_required_customss
def student_list(request):
    student = Student.objects.all()
    return render(request,'student_list.html',{'student':student})


# Define a nested dictionary to store course and year limits
COURSE_YEAR_LIMITS = {
    'MCA': {
        'first year': 10,
        'second year': 10,
    },
    'MSc': {
        'first year': 5,
        'second year': 5,
    },
    # Add other courses and their corresponding year limits as needed
}

@login_required_customss
def handle_approval(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        action = request.POST.get('action')

        if action == 'approve':
            student = Student.objects.get(id=student_id)
#count.........................................
            course = student.course
            year = student.year

            # Check if the course and year exist in the dictionary, otherwise use a default limit
            year_limits = COURSE_YEAR_LIMITS.get(course, {})
            year_limit = year_limits.get(year, 2)

            # Check the number of students registered for the course and year
            student_count_for_course_and_year = Student.objects.filter(course=course, year=year, is_saved=True).count()

            if student_count_for_course_and_year >= year_limit:
                # Maximum limit reached, show error message
                messages.info(request,f'The maximum limit of {year_limit} students for {course} {year} has been reached.')
                return redirect('student_list')

            #count    .................................................

            student.is_saved = True
            student.save()
            if student.course == 'MCA':
                mca_student = MCA_student(
                    code = student.code,
                    username = student.username
                )
                mca_student.save()
                if student.year == 'first year':
                    mca_firstyear_student = MCA_firstyear_student(
                        code = student.code,
                        username = student.username
                    )
                    mca_firstyear_student.save()
                elif student.year == 'second year':
                    mca_secondyear_student = MCA_secondyear_student(
                        code = student.code,
                        username = student.username
                    )
                    mca_secondyear_student.save()
            elif student.course == 'MSc':
                msc_student = MSc_student(
                    code = student.code,
                    username = student.username
                )
                msc_student.save()
                if student.year == 'first year':
                    msc_firstyear_student = MSc_firstyear_student(
                        code = student.code,
                        username = student.username
                    )
                    msc_firstyear_student.save()
                elif student.year == 'second year':
                    msc_secondyear_student = MSc_secondyear_student(
                        code = student.code,
                        username = student.username
                    )
                    msc_secondyear_student.save()
        elif action == 'reject':
            student = Student.objects.get(id=student_id)
            student.delete()

    return redirect('student_list')


@login_required_customss
def handle_approvals(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        action = request.POST.get('action')

        if action == 'approve':
            teacher = Teacher.objects.get(id=teacher_id)

            teacher.is_saved = True
            teacher.save()

        elif action == 'reject':
            teacher = Teacher.objects.get(id=teacher_id)
            teacher.delete()

    return redirect('teacher_list')


@login_required_customss
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course_name = form.cleaned_data['course_name']
            semester = form.cleaned_data['semester']
            subjects = form.cleaned_data['subjects'].split(',')

            # Check if a course with the same name and semester already exists
            if Course.objects.filter(name=course_name, semester=semester).exists():
                messages.error(request,f"A course with the name '{course_name}' and semester '{semester}' already exists.")
                return render(request, 'add_course.html', {'form': form})

            # Create the course
            course = Course.objects.create(name=course_name, semester=semester)

            # Create the subjects
            for subject_name in subjects:
                Subject.objects.create(name=subject_name.strip(), course=course)

            messages.info(request, 'Course added successfully.')
            # Redirect to a success page or do something else
            return redirect('add_course')
    else:
        form = CourseForm()

    return render(request, 'add_course.html', {'form': form})


@login_required_customss
def subject_allot(request):
    teachers = Teacher.objects.all()

    if request.method == 'POST':
        selected_subjects = request.POST.getlist('selected_subjects')
        teacher_id = request.POST['teacher']

        teacher = get_object_or_404(Teacher, id=teacher_id)

        existing_allotments = SubjectAllotment.objects.filter(teacher=teacher)
        existing_allotments.delete()

        for subject_id in selected_subjects:
            subject = Subject.objects.get(id=subject_id)

            subject_allotment = SubjectAllotment.objects.create(
                course=subject.course,
                subject=subject,
                teacher=teacher
            )

            # Get the selected students
            selected_students = request.POST.getlist(f'students_{subject_id}')

            # Add the selected students to the subject allotment
            subject_allotment.students.set(selected_students)

        # Redirect to a success page or do something else
        return render(request, 'subject_allot.html')
    else:
        courses = Course.objects.all()
        return render(request, 'subject_allot.html', {'courses': courses, 'teachers': teachers})


def teacher_reg(request):
    if request.method == 'POST':
        teachername = request.POST['teachername']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if Teacher.objects.filter(email=email).exists():
                messages.info(request,'Email Already Exists.')
                return redirect('teacher_reg')
            else:
                teacher = Teacher(teachername=teachername,firstname=firstname,lastname=lastname,email=email,password=password)
                teacher.save()
                return redirect('teacher_login')
        else:
            messages.info(request,'Password is not Matching.')
            return redirect('teacher_reg')

    return render(request,'teacher_reg.html')


def teacher_login(request):
    if request.method == 'POST':
        teachername = request.POST.get('teachername')
        password = request.POST.get('password')
        try:
            teacher = Teacher.objects.get(teachername=teachername)
            if teacher.is_saved:
                if teacher.password == password:
                    request.session['teachername'] = teachername
                    return redirect('teacher_home')
                else:
                    messages.info(request, 'Invalid teachername or password.')
                    return render(request, 'teacher_login.html')
            else:
                messages.info(request, 'Wait for the Admin Approval.')
                return render(request, 'teacher_login.html')
        except Teacher.DoesNotExist:
            messages.info(request, 'Invalid teachername or password.')
            return render(request, 'teacher_login.html')

    return render(request, 'teacher_login.html')


@login_required_customs
def subject_students(request, elective_subject_id):
    elective_subject = get_object_or_404(ElectiveSubject, id=elective_subject_id)
    students = StudentRegistration.objects.filter(elective_subject=elective_subject)  # Filter students by the elective subject

    # Get the students based on the conditions
    # if elective_subject.name in ['1', '2']:
    # students = StudentRegistration.objects.filter(elective_subject=elective_subject)  # Filter students by the elective subject
    # elif elective_subject.name in ['3', '4']:
    # students = StudentRegistration.objects.filter(elective_subject=elective_subject)  # Filter students by the elective subject
    # else:
    #     students = []

    elective_marks_saved = request.session.get('elective_marks_saved', False)  # Get marks_saved state from the session
    saved_elective_subject_ids = ElectiveMarks.objects.filter(student__in=students, elective_subject=elective_subject).values_list('elective_subject_id', flat=True)

    if request.method == 'POST':
        saved_elective_subject_ids = []  # Initialize a list to store the IDs of saved subjects
        deleted_elective_subject_ids = []  # Initialize a list to store the IDs of deleted subjects

        for student in students:
            attendance = request.POST.get(f'attendance_{student.id}')
            assignment = request.POST.get(f'assignment_{student.id}')
            seminar = request.POST.get(f'seminar_{student.id}')
            test1 = request.POST.get(f'test1_{student.id}')
            test2 = request.POST.get(f'test2_{student.id}')

            try:
                total_elective_marks = calculate_total_elective_marks(attendance, assignment, seminar, test1, test2)

                elective_marks = ElectiveMarks.objects.create(student=student, elective_subject=elective_subject, attendance=attendance,
                                             assignment=assignment, seminar=seminar, test1=test1, test2=test2,
                                             total_elective_marks=total_elective_marks)
                elective_marks.save()
                saved_elective_subject_ids.append(str(elective_subject.id))  # Add the subject ID as a string
            except ValueError as e:
                # Handle the case when there is an error in calculating or saving the marks
                print(f"Error: {str(e)}")
                # You can display an error message to the user if required

        if not saved_elective_subject_ids:
            deleted_elective_subject_ids.append(elective_subject.id)

        request.session['elective_marks_saved'] = True  # Set marks_saved state in the session
        request.session['saved_elective_subject_ids'] = saved_elective_subject_ids  # Store the list of saved subject IDs in the session
        request.session['deleted_elective_subject_ids'] = deleted_elective_subject_ids

        return redirect('subject_students', elective_subject_id=elective_subject_id)  # Redirect back to the same page

    elective_marks_data = ElectiveMarks.objects.filter(student__in=students, elective_subject=elective_subject)
    elective_marks_dict = {}
    for electivemarks in elective_marks_data:
        elective_marks_dict[electivemarks.student_id] = electivemarks

    context = {'elective_subject': elective_subject, 'students': students, 'elective_marks_dict': elective_marks_dict, 'elective_marks_saved': elective_marks_saved,
               'saved_elective_subject_ids': saved_elective_subject_ids}  # Add saved_subject_ids to the context
    return render(request, 'subject_students.html', context)


def calculate_total_elective_marks(attendance, assignment, seminar, test1, test2):
    # Convert the input values to integers
    attendance = int(attendance) if attendance else 0
    assignment = int(assignment) if assignment else 0
    seminar = int(seminar) if seminar else 0
    test1 = int(test1) if test1 else 0
    test2 = int(test2) if test2 else 0

    # Validate the maximum marks for each field
    if attendance > 5 or assignment > 5 or seminar > 10 or test1 > 15 or test2 > 15:
        raise ValueError("Maximum marks exceeded.")

    total_elective_marks = attendance + assignment + seminar + test1 + test2

    # Validate the total marks
    if total_elective_marks > 50:
        raise ValueError("Total marks cannot exceed 50.")

    return total_elective_marks


def edit(request, student_id):
    elective_marks_instance = get_object_or_404(ElectiveMarks, student_id=student_id)

    if request.method == 'POST':
        attendance = request.POST.get('attendance')
        assignment = request.POST.get('assignment')
        seminar = request.POST.get('seminar')
        test1 = request.POST.get('test1')
        test2 = request.POST.get('test2')

        if attendance and assignment and seminar and test1 and test2:
            # Calculate total elective marks
            total_elective_marks = int(attendance) + int(assignment) + int(seminar) + int(test1) + int(test2)

            # Update the instance
            elective_marks_instance.attendance = int(attendance)
            elective_marks_instance.assignment = int(assignment)
            elective_marks_instance.seminar = int(seminar)
            elective_marks_instance.test1 = int(test1)
            elective_marks_instance.test2 = int(test2)
            elective_marks_instance.total_elective_marks = total_elective_marks
            elective_marks_instance.save()

            return redirect('subject_students', elective_subject_id=elective_marks_instance.elective_subject.id)

    return render(request, 'edit.html', {'elective_marks_instance': elective_marks_instance})


@login_required_customs
def teacher_home(request):
    total_teachers = Teacher.objects.count()
    total_students = Student.objects.count()
    online_students = Student.objects.filter(is_online=True).count()
    offline_students = total_students - online_students
    teachername = request.session.get('teachername')
    if not teachername:
        return redirect('teacher_login')

    teacher = Teacher.objects.get(teachername=teachername)
    subject_allotments = teacher.subject_allotments.all()
    elective_subject_allotment, created = ElectiveSubjectAllotment.objects.get_or_create(teacher=teacher)

    # Feedback handling
    feedback_list = Send_Feedback.objects.filter(teacher_name=teacher.teachername).order_by('-timestamp')

    if request.method == 'POST':
        form = Send_Feedback_Form(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.teacher_name = teacher.teachername
            feedback.save()
            return redirect('teacher_home')  # Redirect to the teacher's homepage after successful feedback submission

    else:
        form = Send_Feedback_Form()

    return render(request, 'teacher_home.html', {
        'teacher': teacher,
        'subject_allotments': subject_allotments,
        'elective_subject_allotment': elective_subject_allotment,
        'feedback_list': feedback_list,
        'form': form,
        'total_teachers':total_teachers,
        'offline_students':offline_students,
        'online_students': online_students,
        'total_students':total_students
    })


def teacher_list(request):
    teacher = Teacher.objects.all()
    return render(request,'teacher_list.html',{'teacher':teacher})


@login_required_customs
def subject_student_list(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    # Get the students based on the conditions
    if subject.course.semester in ['1', '2']:
        students = subject.students.filter(year='first year')
    elif subject.course.semester in ['3', '4']:
        students = subject.students.filter(year='second year')
    else:
        students = []

    marks_saved = request.session.get('marks_saved', False)  # Get marks_saved state from the session
    saved_subject_ids = Marks.objects.filter(student__in=students, subject=subject).values_list('subject_id', flat=True)

    if request.method == 'POST':
        saved_subject_ids = []  # Initialize a list to store the IDs of saved subjects
        deleted_subject_ids = []  # Initialize a list to store the IDs of deleted subjects

        for student in students:
            attendance = request.POST.get(f'attendance_{student.id}')
            assignment = request.POST.get(f'assignment_{student.id}')
            seminar = request.POST.get(f'seminar_{student.id}')
            test1 = request.POST.get(f'test1_{student.id}')
            test2 = request.POST.get(f'test2_{student.id}')

            try:
                total_marks = calculate_total_marks(attendance, assignment, seminar, test1, test2)

                marks = Marks.objects.create(student=student, subject=subject, attendance=attendance,
                                             assignment=assignment, seminar=seminar, test1=test1, test2=test2,
                                             total_marks=total_marks)
                marks.save()
                saved_subject_ids.append(str(subject.id))  # Add the subject ID as a string
            except ValueError as e:
                # Handle the case when there is an error in calculating or saving the marks
                print(f"Error: {str(e)}")
                # You can display an error message to the user if required

        if not saved_subject_ids:
            deleted_subject_ids.append(subject.id)

        request.session['marks_saved'] = True  # Set marks_saved state in the session
        request.session['saved_subject_ids'] = saved_subject_ids  # Store the list of saved subject IDs in the session
        request.session['deleted_subject_ids'] = deleted_subject_ids

        return redirect('subject_student_list', subject_id=subject_id)  # Redirect back to the same page

    marks_data = Marks.objects.filter(student__in=students, subject=subject)
    marks_dict = {}
    for marks in marks_data:
        marks_dict[marks.student_id] = marks

    context = {'subject': subject, 'students': students, 'marks_dict': marks_dict, 'marks_saved': marks_saved,
               'saved_subject_ids': saved_subject_ids}  # Add saved_subject_ids to the context
    return render(request, 'subject_student_list.html', context)


def calculate_total_marks(attendance, assignment, seminar, test1, test2):
    # Convert the input values to integers
    attendance = int(attendance) if attendance else 0
    assignment = int(assignment) if assignment else 0
    seminar = int(seminar) if seminar else 0
    test1 = int(test1) if test1 else 0
    test2 = int(test2) if test2 else 0

    # Validate the maximum marks for each field
    if attendance > 5 or assignment > 5 or seminar > 10 or test1 > 15 or test2 > 15:
        raise ValueError("Maximum marks exceeded.")

    total_marks = attendance + assignment + seminar + test1 + test2

    # Validate the total marks
    if total_marks > 50:
        raise ValueError("Total marks cannot exceed 50.")

    return total_marks


def update(request, student_id):
    marks = Marks.objects.filter(student_id=student_id)

    if marks.count() == 0:
        # Handle the case when no Marks object is found
        raise Http404("Marks object not found.")
    elif marks.count() == 1:
        # Only one Marks object found, proceed with updating
        marks = marks.first()
        form = MarksForm(request.POST or None, instance=marks)

        if form.is_valid():
            form.save()
            subject_id = marks.subject.id
            return HttpResponseRedirect(reverse('subject_student_list', args=[subject_id]))
    else:
        # Multiple Marks objects found, handle the case accordingly
        # For example, you can choose to update the first object in the queryset
        marks = marks.first()
        form = MarksForm(request.POST or None, instance=marks)
        if form.is_valid():
            form.save()
            subject_id = marks.subject.id
            return HttpResponseRedirect(reverse('subject_student_list', args=[subject_id]))

    return render(request, 'edit.html', {'form': form, 'marks': marks})


def student_reg(request):
    courses = Course.objects.all()
    # Create a set to store unique course names
    unique_course_names = set()

    # Filter out duplicate course names and add them to the set
    unique_courses = []
    for course in courses:
        if course.name not in unique_course_names:
            unique_courses.append(course)
            unique_course_names.add(course.name)
    if request.method == 'POST':
        code = request.POST['code']
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        course = request.POST['course']
        year = request.POST['year']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if Student.objects.filter(code=code).exists():
                messages.info(request, 'Student ID already exists.')
                return redirect('student_reg')
            elif Student.objects.filter(email=email).exists():
                messages.info(request, 'Email ID already exists.')
                return redirect('student_reg')
            else:
                with transaction.atomic():
                    student = Student(
                        code=code,
                        username=username,
                        firstname=firstname,
                        lastname=lastname,
                        email=email,
                        course=course,
                        year=year,
                        password=password,
                        cpassword=cpassword,
                        is_saved=False
                    )
                    session = SessionStore()
                    session['student_id'] = student.id
                    student.save()

                    # Subject allotment based on the course
                    if course == 'MCA':
                        # Get MCA subjects
                        mca_course = Course.objects.filter(name='MCA')
                        mca_subjects = Subject.objects.filter(course__in=mca_course)

                        # Assign subjects to the student
                        for subject in mca_subjects:
                            subject.students.add(student)

                    elif course == 'MSc':
                        # Get MSc subjects
                        msc_course = Course.objects.filter(name='MSc')
                        msc_subjects = Subject.objects.filter(course__in=msc_course)

                        # Assign subjects to the student
                        for subject in msc_subjects:
                            subject.students.add(student)

                return redirect('home')
        else:
            messages.info(request, 'Password does not match.')
            return redirect('student_reg')

    return render(request, 'student_reg.html',{'courses':unique_courses})


def view_marks(request):
    if request.method == 'POST':
        semester = request.POST.get('semester')

        # Get the username from the session
        username = request.session.get('username')

        # Check if the username exists in the session and retrieve the student object
        try:
            student = Student.objects.get(username=username)

        except Student.DoesNotExist:
            # Handle the case when the username is not found in the session
            error_message = "You are not logged in as a student."
            return render(request, 'view_marks.html', {'error_message': error_message})

        # Filter the marks for the logged-in student only
        marks = Marks.objects.filter(student=student, subject__course__semester=semester)

        if marks:
            return render(request, 'view_marks.html', {'marks': marks, 'semester': semester})
        else:
            error_message = "No marks found for the provided semester."
            return render(request, 'view_marks.html', {'error_message': error_message})

    return render(request, 'view_marks.html')


def view_elective_marks(request):
    if request.method == 'POST':
        # Get the semester from the form
        semester = int(request.POST.get('semester'))

        # Get the username from the session
        username = request.session.get('username')

        try:
            # Get the student registration for the provided username and semester
            student_registration = StudentRegistration.objects.get(username__username=username, semester=semester)

            # Filter the marks for the provided student and semester
            elective_marks = ElectiveMarks.objects.filter(student=student_registration)

            if elective_marks:
                return render(request, 'view_elective_marks.html', {'elective_marks': elective_marks, 'semester': semester})
            else:
                error_message = "No marks found for the provided semester."
                return render(request, 'view_elective_marks.html', {'error_message': error_message})

        except StudentRegistration.DoesNotExist:
            # Handle the case when the student with the provided name and semester is not found in the database
            error_message = "Student with the provided name and semester not found."
            return render(request, 'view_elective_marks.html', {'error_message': error_message})

    return render(request, 'view_elective_marks.html')


def send_feedback(request):
    if request.method == 'POST':
        form = Send_Feedback_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_home')  # Redirect to the admin feedback view
    else:
        form = Send_Feedback_Form()

    return render(request, 'send_feedback.html', {'form': form})


def teacher_feedback(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)  # Use pk instead of id to match the primary key
    feedback_list = Send_Feedback.objects.filter(teacher_name=teacher.teachername).order_by('-timestamp')
    return render(request, 'teacher_home.html', {'teacher': teacher, 'feedback_list': feedback_list})


def admin_feedbacks(request):
    feedback_list = Send_Feedback.objects.all().order_by('-timestamp')
    return render(request, 'admin_feedbacks.html', {'feedback_list': feedback_list})
