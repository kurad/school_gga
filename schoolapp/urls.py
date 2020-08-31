from django.urls import path, include
from . import views

urlpatterns = [
    
    path('', views.index),
    path('teacher/register', views.registerteacher),
    path('teacher/dashboard', views.dashboard),
    path('teacher/create', views.saveteacher),
    path('teacher/subjects', views.subjects),
    path('teacher/level', views.levels),
    path('teacher/level/<int:id>', views.level_view),
    path('teacher/removelevel/<int:id>', views.remove_level_youteach),
    path('teacher/add_subject/<int:id>', views.add_subject),
    path('teacher/addunit/<int:id>', views.add_unit),
    path('teacher/postunit/<int:id>', views.post_unit),
    path('teacher/addtopic/<int:id>', views.add_topic),
    path('teacher/posttopic/<int:id>', views.post_topic),
    path('teacher/topics', views.contents),
    path('teacher/savesubject', views.save_subject),
    path('teacher/teacherlogin', views.get_teacher_login),
    path('teacher/login', views.teacher_login),
    path('teacher/logout', views.logout),
    path('teacher/addlevel/<int:id>', views.level_youteach),
    path('teacher/viewcontent/<int:id>', views.content_view),
    path('teacher/editcontent/<int:id>', views.content_edit),

    # ===================== Students =========================
    path('student/login', views.student_index),
    path('student/postlogin', views.student_login),
    path('student/logout', views.student_logout),
    path('student/create', views.save_student),
    path('student/dashboard', views.student_dashboard),
    path('student/units/<int:subject_id>', views.units_student),
    path('student/content/<int:unit_id>', views.content),
    path('student/choosesubject/<int:id>', views.choose_subject),
    path('student/removesubject/<int:id>', views.remove_subj_choice),

]