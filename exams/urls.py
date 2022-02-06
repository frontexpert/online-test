from django.urls import path
from django.conf.urls import handler404

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginn, name='login'),
    path('logout', views.logoutt, name='logout'),
    path('register', views.register, name='register'),
    path('contact', views.contact, name='contact'),
    path('membership', views.membership, name='membership'),
    path('exam/dashboard', views.exam_dashboard, name='exam dashboard'),
    path('exam/goto/<int:schedule_id>', views.exam_goto, name='exam goto'),
    path('exam/start/<int:schedule_id>', views.exam_start, name='exam start'),
    path('exam/next_question', views.exam_next_question),
    path('exam/prev_question', views.exam_prev_question),
    path('exam/submit', views.exam_submit, name="exam submit"),
    path('exam/prompted/<int:score_id>', views.exam_prompted, name='exam goto prompted'),
]