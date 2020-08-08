from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        labels ={'sub_name':'Subject Name', 'units':'Number of Units', 'combination':'Combination'}

