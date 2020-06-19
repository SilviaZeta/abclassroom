from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
#from rolepermissions.roles import assign_role, get_user_roles
from guardian.shortcuts import get_user_perms
from guardian.shortcuts import assign_perm
from guardian.shortcuts import remove_perm
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User

from django.template.loader import get_template
#from django.template.loader import render_to_string

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.mail import BadHeaderError
#from templated_mail.mail import BaseEmailMessage
from django.core.mail import get_connection
from django.http import JsonResponse
import datetime
import random
from .decorators import user_is_approved
from . import forms
from . import models

@login_required
def create_class_view(request, username):

	if request.method == 'POST':
		form = forms.CreateClassForm(request.POST)

		if form.is_valid():
			class_item = form.save(commit=False)
			class_item.save()

			request.user.myclass.add(class_item) 

			#user permissions for class creator
			teacher_perms = ['delete_class', 'change_class','view_class']
			update_class_perm(class_item, request.user, teacher_perms, action="assign")

			#permissions are:
			print(get_user_perms(request.user, class_item)) 
			
			return redirect('dashboard', username)
	
	else:
		form = forms.CreateClassForm()

	context = {"form": form}
	return render(request, 'class_form.html', context)


@login_required
def update_class_view(request, username, pk):

	class_item = models.Class.objects.get(id=pk)

	if request.method == 'POST':
		form = forms.UpdateClassForm(request.POST, instance=class_item)

		if form.is_valid():
			form.save()
			return redirect('dashboard', username)
	else:
		form = forms.UpdateClassForm(instance=class_item)
	
	context = {"form": form}
	return render(request, 'class_form.html', context)


@login_required
def delete_class_view(request, username, pk):

	class_item = models.Class.objects.get(id=pk)
	
	if request.method == 'POST':
		class_item.delete()
		return redirect('dashboard', username)
	
	context = {"class": class_item}
	return render(request, 'delete_class.html', context)

@login_required
def delete_priority_view(request, username, pk, pk1):
	if request.method == 'POST':
		models.Priority.objects.get(pk=pk1).delete()
	return redirect('class_dashboard', username, pk)


@login_required
def assign_priority_view(request, username, pk, pk1):

	priority = models.Priority.objects.get(pk=pk1)
	
	element = request.user.username+' '+request.user.email
	
	if request.method == 'POST':
		if priority.mylist != None:
			if element in priority.mylist:
				return HttpResponse('')
	
		priority.set_list(element)
		priority.save()
	return redirect('class_dashboard', request.user.username, pk)

	
@login_required
def profile_view(request, username):

    logged_user = request.user
    qs_class = models.Class.objects.none()
    if logged_user.myclass.all().count() > 0:
        qs_class = models.Class.objects.filter(user=logged_user)

        for item in qs_class:
            item.users_count = item.user.all().count()
            item.role = get_user_role(logged_user, item)

                
    context = {"class_obj": qs_class}
    return render(request, 'dashboard.html', context)


@login_required
def enrolled_users_view(request, username):

	if request.is_ajax and request.method == "POST":

		class_id = request.POST.get('class_id', None)
		

		if class_id != None:

			class_item = models.Class.objects.get(id=class_id)

			users = class_item.user.all().values()

			data = {'id':[],'username':[],'role':[],'email':[]}
			for user in users:
				data['id'].append(user['id'])
				data['username'].append(user['username'])
				data['email'].append(user['email'])

			for user in class_item.user.all():
				data['role'].append(get_user_role(user, class_item))
	   
			return JsonResponse({"data": data}, status=200)
		else:
		 	return HttpResponse("")	
	else:
		return JsonResponse({"error": ""}, status=400)


@login_required
def add_user_view(request, username, pk=None):
    '''add a new user to the class with id equal to pk.'''
    
    class_item = models.Class.objects.get(id=pk)

    if request.method == 'POST':
        form = forms.ExistUserForm(request.POST) 

        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            
            if username != '':
                user = User.objects.get(username=username)
                message = "The user %s has been added."%username
            if email != '':
                user = User.objects.get(email=email)
                message = "The user with email %s has been added."%email
            
            class_item.user.add(user) #add user to class
            update_class_perm(class_item, user, ['view_class',], action="assign")
        else:
             message = "The username or the email you entered does \
             				not belong to a recognized user."
        return render(request, 'add_user_outcome.html', {'message':message} )     #
    else:
        form = forms.ExistUserForm()

    context = {'form': form}
    return render(request, "class_user_form.html", context)


@login_required
def remove_user_view(request, username, pk, pk1):
    '''remove a user from the class'''

    if request.method == 'GET':
	    class_item = models.Class.objects.get(id=pk)
	    user = User.objects.get(id=pk1)

	    update_class_perm(class_item, user, ['view_class',], action="remove")
	    class_item.user.remove(user)

    return redirect('dashboard', username)

def get_user_role(user, class_item):
	if 'change_class' in get_user_perms(user, class_item):
		return 'Teacher'
	elif 'view_class' in get_user_perms(user, class_item):
		return 'Student'
	else:
		return 'Pending'	


@login_required
def get_standard_context(request):
	context = {
				'from' : request.user.username,
				'domain' : settings.DEFAULT_DOMAIN,
				}
	return context


@login_required
def class_invite_view(request, username, pk):

	from_email = settings.EMAIL_HOST_USER

	class_item = models.Class.objects.get(id=pk)

	template_name = "class_invite_email.html"		

	if request.method == 'POST':

		form = forms.ClassInviteForm(request.POST)
		
		if form.is_valid():

			#retrieve data from form
			to_email = form.cleaned_data['to']
			content = form.cleaned_data['content']
			
			#define email context
			context = get_standard_context(request)
			print(context['from'])
			context['class'] = class_item
			if len(content)>0:
				context['message'] = content 

			#send email
			send_group_email(from_email, to_email, "Class Invite", context, template_name)

			return redirect('invite_confirm', username, pk)
		else:
			return render(request, '404.html')
	else:
		form = forms.ClassInviteForm()
	
	context = {'form': form}
	return render(request, "class_invite_form.html", context)


@login_required
def priority_invite_view(request, username, pk):

	from_email = settings.EMAIL_HOST_USER

	class_item = models.Class.objects.get(id=pk)

	template_name = "priority_invite_email.html"

	if request.method == 'POST':
		form = forms.PriorityInviteForm(request.POST)

		if form.is_valid():
			
			#retrieve data from form
			to_email = form.cleaned_data.get('to')
			expiry_date = form.cleaned_data.get('expiry_date')
			expiry_time = form.cleaned_data.get('expiry_time')

			#combine together date and time and convert to string
			expiry_datetime = get_expiryDate(expiry_date, expiry_time, 'template')
			
			#define email context
			context = get_standard_context(request)
			context['class'] = class_item
			context['expiry'] = expiry_datetime
			context['num_invites'] = len(to_email)

			#send email
			send_group_email(from_email, to_email, "Priority Invite", context, template_name)

			#save priority object
			priority = form.save(commit=False)
			priority.myclass = class_item
			priority.save()
			
			return redirect('invite_confirm', username, pk)

	else:
		form = forms.PriorityInviteForm()

	context = {'form': form}
	return render(request, "priority_invite_form.html", context)


def get_expiryDate(expiry_date, expiry_time, output):
	'''combine date and time in datetime and convert to string.
	Arguemnts:
	----------
	expiry_date : 	datetime object for data, as from Priority model
	expiry_time : 	datetime object for time, as from Priority model
	output		:	string, 'js_countdown' or 'template' for type of output
	'''

	expiry_dt = datetime.datetime.combine(expiry_date, expiry_time)
	if output == 'template':
		return datetime.datetime.strftime(expiry_dt, 'at %H:%M, on %d/%m/%Y')
	elif output == 'js_countdown':
		return datetime.datetime.strftime(expiry_dt, "%b %d %Y %H:%M:00") #example: Wed 10 2020 3:15




def send_group_email(from_email, to_email, subject, context, template_name):
	'''send a group email where all recepient are in bcc'''
	try:
		connection = get_connection()
		connection.open()

		msg = EmailMultiAlternatives(subject, '', from_email, 
										bcc=to_email, connection=connection
									)
		html_custom_content = get_template(template_name).render(context)
		msg.attach_alternative(html_custom_content, "text/html")
		msg.send()
		
	except BadHeaderError:
		return HttpResponse('Invalid header found.')

	finally:
		connection.close()


@login_required
def invite_confirm_view(request, username, pk):
	return render(request, "invite_confirm.html")


@login_required
def add_priority_context(request, class_item, context):

	if class_item.priority.all().count() > 0:

		context['any_priority'] = True 
		context['priority'] = []

		for priority in class_item.priority.all():

			priority.expiry = get_expiryDate(priority.expiry_date, priority.expiry_time, 'js_countdown')
			priority.users = priority.get_list()

			element = request.user.username+' '+request.user.email
			if element in priority.users:
				priority.position = priority.users.index(element)+1
			else:
				priority.position = len(priority.users)+1

			priority.status = 'done' if element in priority.users else 'pending'

			context['priority'].append(priority)

	return context


@login_required
def add_grouping_context(request, class_item, context):

	if class_item.class_group.all().count() > 0:

		context['any_groups'] = True 
		context['mygroup'] = None
		context['groups'] = []
		colors = [ "#abdec7", "#a7cdd8", "#dda6ac", "#e0a89a", "#a1ddd7", "#adbadc", "#abe3c4"]
		element = request.user.username+' '+request.user.email

		count=1;
		for group_item in class_item.class_group.all():

			expiry = get_expiryDate(group_item.expiry_date, group_item.expiry_time, 'js_countdown')

			group_item.num = count
			count += 1
			group_item.expiry = expiry
			group_item.places_left = group_item.max_size - group_item.len_list()
			group_item.color = random.choice(colors)

			if group_item.get_list() != None:
				group_item.users = group_item.get_list()
			else:
				group_item.users = []
			context['groups'].append(group_item) 

			if group_item.mylist != None:
				if element in group_item.mylist:
					context['mygroup'] = group_item.id
		
	return context


@login_required
def delete_group_view(request, username, pk, pk1):
	if request.method == 'POST':
		models.ClassGroup.objects.get(pk=pk1).delete()
	return redirect('class_dashboard', username, pk)

@login_required
@user_is_approved
def class_page_view(request, username, pk):

	class_item = models.Class.objects.get(id=pk)


	context = {
				'class': class_item, 
				'user_role': get_user_role(request.user, class_item)
				}

	context = add_priority_context(request, class_item, context)

	context = add_grouping_context(request, class_item, context)

	return render(request, 'class_dashboard.html', context)



@login_required
def grouping_invite_view(request, username, pk):

	class_item = models.Class.objects.get(id=pk)
	from_email = settings.EMAIL_HOST_USER

	template_name = "grouping_invite_email.html"

	if request.method == 'POST':
		form = forms.GroupingForm(request.POST)

		if form.is_valid():
			
			#retrieve data from form
			num_groups = form.cleaned_data.get('number_of_groups')
			max_size = form.cleaned_data.get('max_size')
			expiry_date = form.cleaned_data.get('expiry_date')
			expiry_time = form.cleaned_data.get('expiry_time')

			#combine together date and time and convert to string
			expiry_datetime = get_expiryDate(expiry_date, expiry_time, 'template')
			
			#define email context
			context = get_standard_context(request)
			context['class'] = class_item
			context['expiry'] = expiry_datetime

			#send email to all class users
			to_email = []
			for user in class_item.user.all():
			    to_email.append(user.email)
			
			send_group_email(from_email, to_email, "Grouping Invite", context, template_name)

			#save groups object
			class_group = form.save(commit=False)
			class_group.myclass = class_item

			for i in range(num_groups):
				class_group.pk = None
				class_group.save()
			
			return redirect('class_dashboard', username, pk)

	else:
		form = forms.GroupingForm()

	context = {'form': form}
	return render(request, "grouping_invite_form.html", context)


@login_required
def join_group_view(request, username, pk, pk1):

	group_item = models.ClassGroup.objects.get(pk=pk1)
	class_item = models.Class.objects.get(pk=pk)
	element = request.user.username+' '+request.user.email

	if request.method == 'POST':
		for this_group in class_item.class_group.all():
			if this_group.mylist != None:
				if element in this_group.mylist:
					return HttpResponse('')

		group_item.set_list(element)
		group_item.save()

	return redirect('class_dashboard', request.user.username, pk)


@login_required
def leave_group_view(request, username, pk, pk1):

	group_item = models.ClassGroup.objects.get(pk=pk1)
	element = request.user.username+' '+request.user.email

	
	if request.method == 'POST':
		group_item.remove_list(element)
		group_item.save()
		print(group_item.mylist)
	
	return redirect('class_dashboard', request.user.username, pk)


@login_required
def search_class_view(request, username):

	if request.is_ajax and request.method == "POST":

		print("I am in class search")

		class_slug = request.POST.get('class_slug', None)

		if class_slug != None:

			obj = models.Class.objects.filter(slug__icontains=class_slug).order_by('slug')

			data = {'id':[],'slug':[],'subject':[],'description':[]}
			for item in obj:
				data['id'].append(item.id)
				data['slug'].append(item.slug)
				data['subject'].append(item.subject)
				data['description'].append(item.description)

			return JsonResponse({"data": data}, status=200)
		else:
			return JsonResponse({"error": ""}, status=400)
	else:
		return JsonResponse({"error": ""}, status=400)


@login_required
def join_class_view(request, username, pk=None):

	class_item = models.Class.objects.get(id=pk)

	if request.method == "GET": #this should be a post

		qs = class_item.user.all().filter(username__iexact=username)

		if not qs.exists():
			user = User.objects.get(username=username)
			class_item.user.add(user)

			#permissions are:
			print(get_user_perms(request.user, class_item)) 

	return redirect('dashboard', username)


def update_class_perm(class_item, user, perms_list, action):

	#user permissions for class creator
	for codename in perms_list:
		perm_obj = Permission.objects.get(codename=codename)
		if action == "assign":
			assign_perm(perm_obj, user, class_item)
		elif action == "remove":
			remove_perm(perm_obj, user, class_item)
	return class_item


@login_required
def approve_user_view(request, username, pk, pk1):

	if request.method == "GET": #this should be a post
		class_item = models.Class.objects.get(id=pk)
		user = User.objects.get(id=pk1)
		update_class_perm(class_item, user, ['view_class',], action="assign")

	return redirect('dashboard', username)




