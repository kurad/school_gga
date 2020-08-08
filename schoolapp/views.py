from django.shortcuts import render, redirect, Http404
from django.contrib import messages
from . models import *
from .forms import SubjectForm
import bcrypt

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
    return redirect('/teacher/teacherlogin')
def get_teacher_login(request):
    return render(request, 'teachers/teacher_login.html')
def levels(request):
    try:
        levels = Level.objects.filter(teacher=request.session['id'])
    except Level.DoesNotExist:
        raise Http404("No Class you don't teach found")
    context = {
        'all_subjects': Subject.objects.filter(teacher=request.session['id']),
        'all_combination': Combination.objects.all(),
        'levels':levels,
        'data': [1, 2, 3, 4, 5, 6, 7, 8, 9],
        'levels_not':Level.objects.exclude(teacher=request.session['id']),
    }
    return render(request, 'teachers/levels.html', context)

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
def add_unit(request):

    return render(request, 'teachers/unit.html')
def units(request):
    #all_levels = Level.objects.get(id=id)
    #units = Unit.objects.all(),
    #related = Unit.objects.filter(subject_id = Subject.objects.get(id=subject_id)).all(),
    context = {
        'all_subjects': Subject.objects.filter(teacher=request.session['id']),
        'units':Unit.objects.filter(subject_id=Subject.objects.get(id = 6)),
        #'related':related,
    }
    return render(request, 'teachers/units.html', context)

def add_unit(request):
    subject = Subject.objects.get(id=request.POST['subject'])
    Unit.objects.create(
        unit_number=request.POST['unit_number'],
        unit_title=request.POST['unit_title'],
        subject=subject
    )
    return redirect('/teacher/subjects')