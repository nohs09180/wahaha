from django import forms
from .models import Query

class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = 'form-control'