from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Event

class NotificationForm(forms.Form):
    verb = forms.CharField(label='Title')
    description = forms.CharField(widget=CKEditorWidget())
    related_events = forms.ModelMultipleChoiceField(queryset=Event.objects.all())

