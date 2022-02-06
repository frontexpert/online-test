from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='admin index'),
    path('login', views.get_login, name='get login'),
    path('adminlogout', views.adminlogout, name='adminlogout'),
    path('postlogin', views.post_login, name='post login'),
    path('subject', views.list_subject, name='list subject'),
    path('subject/create', views.create_subject, name='create subject'),
    path('subject_by_id/<int:subject_id>', views.get_subject, name='get subject by id'),
    path('subject/edit', views.edit_subject, name='edit subject'),
    path('subject/delete', views.delete_subject, name='delete subject'),

    path('section', views.list_section, name='list section'),
    path('section/<int:subject_id>', views.list_section_subject_id, name='list section subject id'),
    path('section/create', views.create_section, name='create section'),
    path('section_by_id/<int:section_id>', views.get_section, name='get section by id'),
    path('section/edit', views.edit_section, name='edit section'),
    path('section/delete', views.delete_section, name='delete section'),

    path('question', views.list_question, name='list question'),
    path('question/create', views.create_question, name='create question'),
    path('get_sections_by_subject_id/<int:subject_id>', views.get_sections_by_subject_id),
    path('question/save', views.save_question, name='save question'),
    path('question/edit/<int:question_id>', views.edit_question, name='edit question'),
    path('question/update', views.update_question, name='update question'),
    path('question/delete', views.delete_question, name='delete question'),

    path('paper', views.list_paper, name='list paper'),
    path('paper/create', views.create_paper, name='create paper'),
    path('get_questions', views.get_questions),
    path('paper/save', views.save_paper, name='save paper'),
    path('paper/edit/<int:paper_id>', views.edit_paper, name='edit paper'),
    path('paper/update', views.update_paper, name='update paper'),
    path('paper/delete', views.delete_paper, name='delete paper'),

    path('schedule', views.index_schedule, name='index schedule'),
    path('get_papers', views.get_papers),
    path('schedule/save', views.save_schedule, name='save schedule'),
]