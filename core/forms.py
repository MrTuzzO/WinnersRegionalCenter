from django import forms

class JobCreatorForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20, required=False)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea, required=False)
