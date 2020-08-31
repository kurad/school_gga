from django import forms
from .models import Subject, Topic
from tinymce.widgets import TinyMCE

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        labels ={'sub_name':'Subject Name', 'units':'Number of Units', 'combination':'Combination'}

class ContentForm(forms.ModelForm):
    #text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))
    class Meta:
        model = Topic
        fields = '__all__'
        labels = {
            'topic_title':'Title',
            'objectives':'Learning Objectves',
            'video':'Video if Any'
        }