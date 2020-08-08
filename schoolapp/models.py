from django.db import models
import re
import bcrypt

class StudentManager(models.Manager):
    def basic_validator(self, post_Data):
        errors = {}
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_Data['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters"
        if not email_checker.match(post_Data['email']):
            errors['email'] = 'Email must be valid'
        if post_Data['password'] != post_Data['confpass']:
            errors['password'] = 'Password and Confirm Password do not match'
        return errors

class TeacherManager(models.Manager):
    def basic_validator(self, post_Data):
        errors = {}
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_Data['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters"
        if not email_checker.match(post_Data['email']):
            errors['email'] = 'Email must be valid'
        if post_Data['password'] != post_Data['confpass']:
            errors['password'] = 'Password and Confirm Password do not match'
        return errors 
    def authenticate(self, email, password):
    	users_with_email = self.filter(email=email)
    	if not users_with_email:
    		return False
    	user = users_with_email[0]
    	return bcrypt.checkpw(password.encode(), user.password.encode())

class Combination(models.Model):
    combName = models.CharField(max_length=50)

    class Meta:
        db_table = "combination"

    def __str__(self):
        return self.combName

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    combination = models.ForeignKey(Combination, related_name='student_combination', on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = StudentManager()
    class Meta:
        db_table = "student"

    def __str__(self):
        return f"{{self.first_name}} {{self.middle_name}} {{self.last_name}}"

class Teacher(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TeacherManager()
    class Meta:
        db_table = "teacher"

    def __str__(self):
        return f"{{self.first_name}} {{self.middle_name}} {{self.last_name}}"

class Level(models.Model):
    levelName = models.CharField(max_length=20)
    teacher = models.ManyToManyField(Teacher)

    class Meta:
        db_table = "level"

    def __str__(self):
        return self.levelName

class Subject(models.Model):
    sub_name = models.CharField(max_length=255)
    units = models.IntegerField()
    level = models.ForeignKey(Level, related_name='level_subjects', default=1, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name="taught_by", on_delete=models.CASCADE)
    class Meta:
        db_table = "subject"
    def __str__(self):
        return self.sub_name

class Unit(models.Model):
    unit_number = models.IntegerField()
    unit_title = models.CharField(max_length=150)
    subject = models.ForeignKey(Subject, related_name="subject_unit", on_delete=models.CASCADE)

    class Meta:
        db_table = "unit"

class Topic(models.Model):
    topic_title = models.CharField(max_length=200)
    objectives = models.TextField()
    unit = models.ForeignKey(Unit, related_name="topics_unit", on_delete=models.CASCADE, null=True)
    video = models.FileField(upload_to='media/videos/%Y/%m/%d/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "topic"