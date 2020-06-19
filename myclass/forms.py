from django import forms
from . import models
from guardian.shortcuts import assign_perm, remove_perm
from multi_email_field import forms as emails_forms
from django.contrib.auth.models import User
import datetime
from django.conf import settings

class CreateClassForm(forms.ModelForm):
	slug =  forms.SlugField(max_length=50)
	subject = forms.CharField(max_length=100)
	description = forms.CharField(max_length=250, widget=forms.Textarea(), required=False)

	class Meta:
		model = models.Class
		fields = ('slug', 'subject', 'description')

	def save(self, commit=True):
		myclass = super().save(commit=False)   
		myclass.slug = self.cleaned_data.get('slug')
		myclass.subject = self.cleaned_data.get('subject')
		myclass.description = self.cleaned_data.get('description')
		if commit:
			myclass.save()
		return myclass
		
class UpdateClassForm(forms.ModelForm):
	slug =  forms.SlugField(help_text="Enter a 'slug', a single string of \
							 letters, numbers, underscores or hyphens.")
	subject = forms.CharField()
	description = forms.CharField(widget=forms.Textarea(), required=False)

	class Meta:
		model = models.Class
		fields = ('slug', 'subject', 'description')

	def save(self, commit=True):
		myclass = super().save(commit=False)   
		myclass.slug = self.cleaned_data.get('slug')
		myclass.subject = self.cleaned_data.get('subject')
		myclass.description = self.cleaned_data.get('description')
		if commit:
			myclass.save()
		return myclass

class ExistUserForm(forms.ModelForm):
    username = forms.CharField(required=False);
    email = forms.EmailField(required=False);
    
    class Meta:
        model = User
        fields = ['username', 'email',]

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data['email']

        if email != '':
            if not User.objects.filter(email=email).exists():
                raise forms.ValidationError(u'Email "%s" is not in use.' % email)
        return email

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data['username']
        if username != '':
            if not User.objects.filter(username=username).exists():
                raise forms.ValidationError(u'Username "%s" is not in use.' % username)
        return username

    def clean(self):
        #super(UserChangeForm, self).clean()
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        if (username == '') & (email == ''):
            raise forms.ValidationError('You cannot leave both fields empty.')
        return self.cleaned_data


class ContactForm(forms.Form):
	to = emails_forms.MultiEmailField(help_text='Enter one email address per line.')
	subject = forms.CharField(max_length=50)
	content = forms.CharField(max_length=2000, widget=forms.Textarea())
	#source = forms.CharField(max_length=50, widget=forms.HiddenInput(), required=False)
    # source is a hidden input for internal use that tells from which page the user sent the message

class ClassInviteForm(ContactForm):
	content = forms.CharField(max_length=500, widget=forms.Textarea(), 
								help_text='Optional short message to be added to the standard content.')
	subject = None 


class PriorityInviteForm(forms.ModelForm):
	to = emails_forms.MultiEmailField(help_text='Enter one email address per line.')
	expiry_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, required=True, 
									help_text="The accepted format for this field is mm/dd/yyyy.") #['%d-%m-%Y']
	expiry_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'), 
									required=True, help_text="The accepted format for this field is hh:mm.")

	class Meta:
		model = models.Priority
		fields = ('to','expiry_date','expiry_time')

	def clean_to(self, *args, **kwargs):
		to = self.cleaned_data.get('to')
		for email in to:
			if User.objects.filter(email=email).exists() == False:
				raise forms.ValidationError("%s does not belong to a recognized user."%email)
		return to


	def clan(self):
		expiry_date = self.cleaned_data.get('expiry_date')
		expiry_time = self.cleaned_data.get('expiry_time')
		expiry_dt = datetime.datetime.combine(expiry_date, expiry_time)
		current_datetime_dt = datetime.datetime.now()

		if (expiry_dt > current_datetime_dt):
			raise forms.ValidationError("%s has already passed. Enter a future date and time."%expiry_dt)
		return self.cleaned_data


		
class GroupingForm(PriorityInviteForm):
	number_of_groups = forms.IntegerField(required=True, help_text='Enter the number of groups.')
	max_size = forms.IntegerField(required=True, help_text='Enter the maximum number of users per group.')
	to = None


	class Meta:
		model = models.ClassGroup
		fields = ('number_of_groups', 'max_size', 'expiry_date','expiry_time')






