from django import template
from ccsit_internal_mark_app.models import Student

register = template.Library()

@register.filter
def is_approved(code):
    return Student.objects.filter(student_code=code).exists()

@register.filter
def dict_contains(dictionary, value):
    return value in dictionary


@register.filter
def key_exists(dictionary, key):
    return key in dictionary


@register.filter
def index(dictionary, key):
    try:
        return dictionary[key]
    except (KeyError, TypeError):
        return None


@register.filter
def get_dict_value(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_total_marks(marks_dict, student_id):
    try:
        marks = marks_dict.get(student_id)
        return marks.total_marks
    except AttributeError:
        return None


@register.filter
def get_attendance_marks(marks_dict, student_id):
    try:
        marks = marks_dict.get(student_id)
        return marks.attendance
    except AttributeError:
        return None


@register.filter
def get_assignment_marks(marks_dict, student_id):
    try:
        marks = marks_dict.get(student_id)
        return marks.assignment
    except AttributeError:
        return None


@register.filter
def get_seminar_marks(marks_dict, student_id):
    try:
        marks = marks_dict.get(student_id)
        return marks.seminar
    except AttributeError:
        return None


@register.filter
def get_test1_marks(marks_dict, student_id):
    try:
        marks = marks_dict.get(student_id)
        return marks.test1
    except AttributeError:
        return None


@register.filter
def get_test2_marks(marks_dict, student_id):
    try:
        marks = marks_dict.get(student_id)
        return marks.test2
    except AttributeError:
        return None



@register.filter
def get_admin_message(feedbacks, teachername):
    admin_feedback = feedbacks.filter(teachername=None, reply__isnull=True, teachername__teachername=teachername).first()
    return admin_feedback.message if admin_feedback else ''


@register.filter
def get_teacher_reply(feedbacks, teachername):
    teacher_reply = feedbacks.filter(teachername__teachername=teachername, reply__isnull=False).order_by('-timestamp').first()
    return teacher_reply.reply if teacher_reply else ''


@register.filter
def calculate_total_marks(attendance, assignment, seminar, test1, test2):
    total_marks = attendance + assignment + seminar + test1 + test2
    return total_marks


@register.filter
def get_total_elective_marks(elective_marks_dict, student_id):
    try:
        elective_marks = elective_marks_dict.get(student_id)
        return elective_marks.total_elective_marks
    except AttributeError:
        return None


@register.filter
def get_attendance_elective_marks(elective_marks_dict, student_id):
    try:
        elective_marks = elective_marks_dict.get(student_id)
        return elective_marks.attendance
    except AttributeError:
        return None


@register.filter
def get_assignment_elective_marks(elective_marks_dict, student_id):
    try:
        elective_marks = elective_marks_dict.get(student_id)
        return elective_marks.assignment
    except AttributeError:
        return None


@register.filter
def get_seminar_elective_marks(elective_marks_dict, student_id):
    try:
        elective_marks = elective_marks_dict.get(student_id)
        return elective_marks.seminar
    except AttributeError:
        return None


@register.filter
def get_test1_elective_marks(elective_marks_dict, student_id):
    try:
        elective_marks = elective_marks_dict.get(student_id)
        return elective_marks.test1
    except AttributeError:
        return None


@register.filter
def get_test2_elective_marks(elective_marks_dict, student_id):
    try:
        elective_marks = elective_marks_dict.get(student_id)
        return elective_marks.test2
    except AttributeError:
        return None


@register.filter
def calculate_total_elective_marks(attendance, assignment, seminar, test1, test2):
    total_elective_marks = attendance + assignment + seminar + test1 + test2
    return total_elective_marks


