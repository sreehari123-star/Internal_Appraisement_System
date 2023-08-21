from django.db.models.signals import post_save
from django.dispatch import receiver
from ccsit_internal_mark_app.models import Student, Course, Subject, SubjectAllotment, Teacher

@receiver(post_save, sender=Student)
def register_student_for_subjects(sender, instance, created, **kwargs):
    if created:
        course = Course.objects.get(name=instance.course)
        subjects = Subject.objects.filter(course=course, year=instance.year)
        teacher = Teacher.objects.get(teachername='Default Teacher')  # Replace with the desired teacher

        for subject in subjects:
            SubjectAllotment.objects.create(course=course, subject=subject, teacher=teacher, student=instance)