from django.forms import ModelForm
from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields= ['title','description','location','sponsor','start_date','end_date']