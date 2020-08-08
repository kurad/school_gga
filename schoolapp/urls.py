from django.urls import path, include
from . import views

urlpatterns = [
    
    path('', views.index),
    path('teacher/register', views.registerteacher),
    path('teacher/dashboard', views.dashboard),
    path('teacher/create', views.saveteacher),
    path('teacher/subjects', views.subjects),
    path('teacher/level', views.levels),
    path('teacher/add_subject/<int:id>', views.add_subject),
    path('teacher/addunit', views.add_unit),
    path('teacher/unit', views.units),
    #path('teacher/postsubject', views.post_subject),
    path('teacher/savesubject', views.save_subject),
    path('teacher/teacherlogin', views.get_teacher_login),
    path('teacher/login', views.teacher_login),
    path('teacher/logout', views.logout),
    path('teacher/addlevel/<int:id>', views.level_youteach),

]