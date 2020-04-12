from django import forms
from . import models

class CreateClient(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ['fname','lname','addr','acct_num','mobile_num','email_addr']