from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import subject_student_list, send_notification

urlpatterns = [
    path('',views.home,name='home'),
    path('about/', views.about,name='about'),
    path('course/',views.course,name='course'),
    path('update/<int:student_id>/',views.update,name='update'),
    path('edit/<int:student_id>/', views.edit, name='edit'),
    path('send_notification', send_notification, name='send_notification'),
    path('feedback/', views.feedback, name='feedback'),
    path('admin_feedback/', views.admin_feedback, name='admin_feedback'),
    # path('compose_message/', views.compose_message, name='compose_message'),
    path('send_feedback/', views.send_feedback, name='send_feedback'),
    path('teacher_feedback/<int:teacher_id>/', views.teacher_feedback, name='teacher_feedback'),
    path('admin_feedbacks/', views.admin_feedbacks, name='admin_feedbacks'),

    path('student_reg',views.student_reg,name='student_reg'),
    path('student_login',views.student_login,name='student_login'),
    path('student_home',views.student_home,name='student_home'),
    path('view_marks',views.view_marks,name='view_marks'),
    path('view_elective_marks/',views.view_elective_marks,name='view_elective_marks'),
    path('logout',views.logout,name='logout'),
    path('add/', views.add_elective_course, name='add_elective_course'),
    path('allot/', views.elective_subject_allotment, name='elective_subject_allotment'),
    path('register/', views.student_registration, name='student_registration'),
    path('teacher/elective_subject/<int:elective_subject_id>/', views.subject_students, name='subject_students'),

    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('student_list/',views.student_list,name='student_list'),
    path('handle_approval/', views.handle_approval, name='handle_approval'),
    path('add_course',views.add_course,name='add_course'),
    path('subject_allot',views.subject_allot,name='subject_allot'),

    path('teacher_reg',views.teacher_reg,name='teacher_reg'),
    path('teacher_login',views.teacher_login,name='teacher_login'),
    path('teacher_home',views.teacher_home,name='teacher_home'),
    path('teacher_list',views.teacher_list,name='teacher_list'),
    path('handle_approvals',views.handle_approvals,name='handle_approvals'),
    path('subject/student_list/<int:subject_id>/', subject_student_list, name='subject_student_list'),
]

