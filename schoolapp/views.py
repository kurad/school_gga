from django.shortcuts import render, redirect, Http404
from django.contrib import messages
from . models import *
from .forms import SubjectForm, ContentForm
import bcrypt
from django.views.generic import CreateView

def index(request):
    return render(request, 'home/index.html')

def registerteacher(request):
    return render(request, 'teachers/teacherRegister.html')

def dashboard(request):
    form = SubjectForm
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'all_subjects': Subject.objects.all() #get(teacher_id=request.session['id'])
    }
    return render(request, 'teachers/dashboard.html')

def saveteacher(request):
    errors = Teacher.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/teacher/register')
    else:
        pwd = bcrypt.hashpw(request.POST['password'].encode('utf-8'),bcrypt.gensalt()).decode()
        new_teacher = Teacher.objects.create(first_name=request.POST['first_name'], middle_name=request.POST['middle_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pwd)
        request.session['teacher'] = new_teacher.first_name+ " "+new_teacher.last_name
        request.session['id'] = new_teacher.id
        return redirect('/teacher/level')
def teacher_login(request):
    result = Teacher.objects.authenticate(request.POST['email'], request.POST['password'])
    if result ==False:
        messages.error(request, "Invalid Email/Password")
    else:
        teachers = Teacher.objects.get(email=request.POST['email'])
        request.session['teacher'] = teachers.first_name+ " "+teachers.last_name
        request.session['id'] = teachers.id
        return redirect('/teacher/subjects')
    return redirect('/teacher/teacherlogin')

    if len(results) > 0:
        if bcrypt.checkpw(request.POST['password'].encode(), results[0].password.encode()):
            request.session['id'] = results[0].id
            return redirect('/teacher/dashboard')
    else:
        messages.error(request, "This email has not been registered.")
        return redirect("/teacher/teacherlogin")
def logout(request):
    request.session.flush()
    return redirect('/')
def get_teacher_login(request):
    return render(request, 'teachers/teacher_login.html')
def levels(request):
    try:
        levels = Level.objects.filter(teacher=request.session['id'])
    except Level.DoesNotExist:
        raise Http404("No Class you don't teach found")
    context = {
        'all_subjects': Subject.objects.all(),
        'levels':levels,
        'levels_not':Level.objects.exclude(teacher=request.session['id']),
    }
    return render(request, 'teachers/levels.html', context)
def level_view(request, id):
    try:
        levels = Level.objects.get(teacher=request.session['id'], id = id)
    except Level.DoesNotExist:
        raise Http404("No Class you don't teach found")
    context = {
        'all_subjects': Subject.objects.all(),
        'levels':levels,
        'levels_not':Level.objects.exclude(teacher=request.session['id']),
    }
    return render(request, 'teachers/levels_view.html', context)
def add_subject(request, id):
    all_levels = Level.objects.get(id=id)
    levels = Level.objects.filter(teacher=request.session['id'])
    context = {
        'levels':levels,
        'all_levels':all_levels,
    }
    return render(request, "teachers/add_subject.html")
def subjects(request):
    context = {
        'all_subjects': Subject.objects.filter(teacher=request.session['id']),
        'levels': Level.objects.filter(teacher=request.session['id']),
        'units': Unit.objects.select_related('subject').filter(subject__teacher=request.session['id']),
    }
    return render(request,"teachers/subjects.html", context)
def save_subject(request):
    teacher = Teacher.objects.get(id=request.session['id'])
    level = Level.objects.get(id=request.POST['level'])
    Subject.objects.create(
            sub_name=request.POST['sub_name'], 
            units=request.POST['units'], 
            level=level,
            teacher=teacher
            )
    return redirect('/teacher/subjects')

def level_youteach(request, id):
    this_teacher = Teacher.objects.get(id=request.session['id'])
    level = Level.objects.get(id= id)
    level.teacher.add(this_teacher)
    return redirect('/teacher/level')

def remove_level_youteach(request, id):
    this_teacher = Teacher.objects.get(id=request.session['id'])
    level = Level.objects.get(id= id)
    level.teacher.remove(this_teacher)
    return redirect('/teacher/level')

def add_unit(request, id):    
    context = {
        'subjects': Subject.objects.get(id=id),
        'units': Unit.objects.filter(subject__teacher=request.session['id'],subject=id),
    }
    return render(request, 'teachers/units.html', context)
def units(request):
    subjects = Subject.objects.filter(teacher=request.session['id'])
    context = {
        'all_subjects': subjects,
        'units': Unit.objects.filter(subject__teacher=request.session['id']),
        #'related':related,
    }
    return render(request, 'teachers/units.html', context)

def post_unit(request, id):
    subject = Subject.objects.get(id=id)
    Unit.objects.create(
        unit_number=request.POST['unit_number'],
        unit_title=request.POST['unit_title'],
        subject=subject
    )
    return redirect(f'/teacher/addunit/{id}')

def add_topic(request, id):
    context = {
        #'subjects': Subject.objects.filter(subject__unit=id),
        'units': Unit.objects.get(id=id),
        #'units': Unit.objects.filter(subject__teacher=request.session['id'],subject=id),
    }   
    return render(request, 'teachers/add_content.html',context)

def post_topic(request, id):
    unit = Unit.objects.get(id = id)
    Topic.objects.create(
        topic_title = request.POST['title'],
        objectives = request.POST['objective'],
        content = request.POST['content'],
        video = request.POST['video'],
        unit =unit
    )
    return redirect(f"/teacher/addtopic/{id}")
def contents(request):
    context = {
        'all_content':Topic.objects.filter(unit__subject__teacher=request.session['id'])

    }
    return render(request, "teachers/contents.html", context)

def content_view(request, id):
    try:
        topics = Topic.objects.get(id = id)
    except Topic.DoesNotExist:
        raise Http404("No content for this unit available")
    context = {
        'topics': topics ,
        'all_content':Topic.objects.filter(unit__subject__teacher=request.session['id']),
    }   
    return render(request, 'teachers/contents_view.html',context)

def content_edit(request, id):
    try:
        topics = Topic.objects.get(id = id)
    except Topic.DoesNotExist:
        raise Http404("No content for this unit available")
    context = {
        'topics': topics ,
        'all_content':Topic.objects.filter(unit__subject__teacher=request.session['id']),
    }   
    return render(request, 'teachers/content_edit.html',context)

    # ======================= Students ===========================

def student_index(request):
    context = {
        'levels': Level.objects.all(),
    }
    return render(request, "students/student_login.html", context)
def student_dashboard(request):
    std = Student.objects.select_related('level').get(id=request.session['id'])
    sub = Subject.objects.filter(students=request.session['id'])
    if 'id' not in request.session:
        return redirect('/')

    context = {
        
        #'all_subjects': Subject.objects.all(),
        'all_subjects': Subject.objects.filter(level__id=std.level.id), 
        'subjects_not_added': Subject.objects.exclude(level__id=std.level.id),
        'subject_register_for': sub,    
    }
    return render(request, 'students/dashboard.html', context)

def save_student(request):
    level = Level.objects.get(id=request.POST['level'])
    std = Student.objects.select_related('level').get(id=request.session['id'])

    errors = Student.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/teacher/register')
    else:
        pwd = bcrypt.hashpw(request.POST['password'].encode('utf-8'),bcrypt.gensalt()).decode()
        new_student = Student.objects.create(
            first_name=request.POST['first_name'], 
            middle_name=request.POST['middle_name'], 
            last_name=request.POST['last_name'], 
            email=request.POST['email'], 
            password=pwd,
            level = level
            )
        request.session['student'] = new_student.first_name+ " "+new_student.last_name
        request.session['id'] = new_student.id

        context = {
        'levels': Level.objects.filter(student=request.session['id']),
        'all_subjects': Subject.objects.filter(level__id=std.level.id),
        #'all_subjects': Subject.objects.filter(student=request.session['id']),    
        }
        return redirect('/student/dashboard', context)

def student_login(request):
    result = Student.objects.authenticate(request.POST['email'], request.POST['password'])
    if result ==False:
        messages.error(request, "Invalid Email/Password")
    else:
        students = Student.objects.get(email=request.POST['email'])
        request.session['students'] = students.first_name+ " "+students.last_name
        request.session['id'] = students.id
        return redirect('/student/dashboard')
    return redirect('/student/login')

    if len(results) > 0:
        if bcrypt.checkpw(request.POST['password'].encode(), results[0].password.encode()):
            request.session['id'] = results[0].id
            return redirect('/student/dashboard')
    else:
        messages.error(request, "This email has not been registered.")
        return redirect("/student/login")
def student_logout(request):
    request.session.flush()
    return redirect('/student/login')

def subject_view(request, id):
    try:
        levels = Level.objects.get(student=request.session['id'], id = id)
    except Level.DoesNotExist:
        raise Http404("No Class you don't teach found")
    context = {
        'all_subjects': Subject.objects.all(),
        'levels':levels,
        #'levels_not':Level.objects.exclude(teacher=request.session['id']),
    }
    return render(request, 'students/choose_subjects.html', context)

def choose_subject(request, id):
    this_student = Student.objects.get(id=request.session['id'])
    subject = Subject.objects.get(id= id)
    subject.students.add(this_student)
    return redirect('/student/dashboard')

def remove_subj_choice(request, id):
    this_student = Student.objects.get(id=request.session['id'])
    subject = Subject.objects.get(id= id)
    subject.students.remove(this_student)
    return redirect('/student/dashboard')

def units_student(request, subject_id):
    if 'id' not in request.session:
        return redirect('/')

    context = {
        'units': Unit.objects.filter(subject_id=subject_id),
    }
    return render(request, 'students/units.html', context)

def content(request, unit_id):
    try:
        topics = Topic.objects.get(unit_id=unit_id)
    except Topic.DoesNotExist:
        raise Http404("No content for this unit available")
    context = {
        'topics': topics ,
    }   
    return render(request, 'students/contents.html',context)
