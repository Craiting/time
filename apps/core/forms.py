from django import forms
from django.contrib.auth import authenticate, login
from .models import Person, JobCostSave, Person
from django.contrib.auth.forms import SetPasswordForm


class DateRangeForm1(forms.Form):
    startDate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker1'}))
    endDate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker2'}))

class DateRangeForm2(forms.Form):
    startDate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker1'}))
    endDate = forms.DateField(widget=forms.TextInput(attrs={'class':'datepicker2'}))
    projectName = forms.CharField()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    url = forms.CharField()
    message = forms.CharField()


class addEmployeeForm(forms.Form):
	firstName = forms.CharField()
	lastName = forms.CharField()
	email = forms.CharField()
	phoneNumber = forms.CharField()
	userName = forms.CharField()
	password = forms.CharField()


class addProjectForm(forms.Form):
    projectName = forms.CharField()
    description = forms.CharField()


class addEmployeeGroupForm(forms.Form):
    name = forms.CharField()

class UpdatePasswordForm(forms.Form):
    currentPassword = forms.CharField(label='Current password:',widget=forms.PasswordInput,)
    newPassword = forms.CharField(label='New password:',widget=forms.PasswordInput)
    confirmNewPassword = forms.CharField(label='Confirm new password:',widget=forms.PasswordInput,)

    # We override init so we can add form-control to our text input class for bootstrap
    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(UpdatePasswordForm, self).clean()
        currentPassword = cleaned_data.get("currentPassword")
        newPassword = cleaned_data.get("newPassword")
        confirmNewPassword = cleaned_data.get("confirmNewPassword")

class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('user', 'curr_clock', 'manager', 'company',)
        widgets={
            # 'user': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
        }

class JobCostForm(forms.Form):
    percent = forms.CharField()
    total_time = forms.CharField()
