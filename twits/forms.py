from django import forms

from twits import models
from captcha.fields import CaptchaField

class CompanyForm(forms.ModelForm):
    captcha = CaptchaField()
    company_description = forms.CharField(max_length=200, help_text="200 Character Max. This field for Company Desc, not for hating. Please enter 'Get Your Hate On' for hating!", widget=forms.Textarea)
    class Meta:
        model = models.Company
        fields = ('company_name', 'company_category', 'company_description')

class HateForm(forms.ModelForm):
    captcha = CaptchaField()
    hate_entry = forms.CharField(max_length=200, help_text="200 Character Max", widget=forms.Textarea)
    class Meta:
        model = models.Hate
        fields = ('hate_company', 'hate_title', 'hate_entry')
