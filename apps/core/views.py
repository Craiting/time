from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from models import TimeEntry
from .forms import ContactForm, LoginForm, addEmployeeForm, addProjectForm, addEmployeeGroupForm, UpdatePasswordForm
from .forms import UpdateAccountForm, DateRangeForm1, DateRangeForm2, JobCostForm
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
import datetime
import time
import calendar
import itertools
from django.views.generic import TemplateView, View
from models import Person, Company, Clocks, Project, EmployeeGroups, EmployeeInGroup, JobCostSave, GroupProject
from django.core.mail import send_mail

# Create your views here.

class SplashPage(TemplateView):
    template_name = 'splash.html'

class Submission(TemplateView):
    template_name = 'submission.html'

class ContactUs(TemplateView):
    template_name = 'contact_us.html'
    form_class = ContactForm

    def post(self,request):
        form = ContactForm(request.POST)
        print "Looking at the contact form"
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            url = form.cleaned_data['url']
            if (url == ' '):
                send_mail('Contact Form', 'Name: ' + name + ' ' +'Email: ' + email + ' ' + 'Message: ' + message, 'aetas.me@gmail.com', ['jrthom18@gmail.com'], fail_silently=False)
        return HttpResponseRedirect("/submission")


class UpdateClock(View):
    def get(self, request, userId):
        userID = request.user.id
        now = datetime.datetime.now()
        clock = Clocks(user=request.user, start_time=now, is_active=True, total_time=0.0)
        clock.save()
        person = Person.objects.get(user=request.user.id)
        person.curr_clock = clock
        person.save()
        return HttpResponseRedirect("/clock")
        #return render(request, 'clock.html', {'now':now, 'type':typeOfTime, 'userID':userID})


class EndClock(View):
    def get(self, request, userId):
        now = datetime.datetime.now()
        userID = request.user.id
        person = Person.objects.get(user=request.user.id)
        clock = person.curr_clock
        clock.end_time = now
        clock.is_active = False
        startTime = clock.start_time
        end_time = clock.end_time        
        totes = end_time- startTime
        t = totes.total_seconds()/60
        clock.total_time = t
        st = calendar.timegm(startTime.timetuple()) #ime.mktime(startTime.timetuple())
        et = calendar.timegm(end_time.timetuple())#time.mktime(end_time.timetuple())
        timedelta = et - st
        if timedelta < 60:
            timedelta = 0
        else:
            timedelta = timedelta / 60
        
        hours = timedelta / 60
        minutes = timedelta % 60
        if minutes < 10:
            minutes = '0' + str(minutes)
        total_time_formatted = str(hours) + ':' + str(minutes)

        clock.total_time = timedelta
        clock.save()
        currPerson = Person.objects.get(user=request.user.id)        
        if timedelta is 0:
            return HttpResponseRedirect("/clock")
        try:   
            currPerson = Person.objects.get(user=request.user.id)        
            ingroups = EmployeeInGroup.objects.filter(employee=currPerson)
            groups = [x.Group for x in ingroups]
            persons_projects = [group.groupproject_set.all() for group in groups]
            project_list = list(itertools.chain(*persons_projects))
        except:
            project_list = None
        manager = check_manager(request)
        return render(request,'jobcost.html',{'total_time':clock.total_time, 'total_time_formatted':total_time_formatted, 'projects':project_list, 'manager':manager})

    def post(self,request,userId):
        try:
            currPerson = Person.objects.get(user=request.user)        
            ingroups = EmployeeInGroup.objects.filter(employee=currPerson)
            groups = [x.Group for x in ingroups]
            persons_projects = [group.groupproject_set.all() for group in groups]
            project_list = list(itertools.chain(*persons_projects))
            percentages = request.POST.getlist('percent')
            form = JobCostForm(request.POST)
            
            for i in range(0,len(project_list)):
                if form.is_valid():
                    job = JobCostSave()
                    job.project = project_list[i].project
                    job.user = currPerson
                    #print int(percentages[i])
                    job.minutes = int(form.cleaned_data['total_time'])*int(percentages[i])/100 
                    job.date = datetime.datetime.now()
                    
                if(int(job.minutes) > 0):
                    job.save()
        except Exception as e:
            print 'error', e
            raise Exception('error endclock')
        return HttpResponseRedirect("/clock")

class EmployeeDate(View):
    def get(self, request, userId):
        return render(request, 'datepicker.html', {'userId':userId})

class Employees(View):
    def get(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        currPerson = Person.objects.get(user=request.user)
        myEmployees = Person.objects.filter(company=currPerson.company).exclude(user=currPerson.user)
        manager = check_manager(request)
        typeOfTime = "Clock in"
        clock = currPerson.curr_clock
        if clock is not None:
            if clock.is_active is True:
                typeOfTime = "Clock Out"
        return render(request, 'employees.html', {'manager':manager, 'type':typeOfTime, 'myEmployees':myEmployees})

class EmployeeTime(View):
    def get(self, request, userId):
        times = []
        form = DateRangeForm1(request.GET)
        manager = check_manager(request)
        if form.is_valid():
            user = User.objects.get(id=userId)
            clocks = Clocks.objects.filter(user=user).exclude(total_time=0)
            total_minutes = 0
            for c in clocks:
                
                # print(c.start_time.strftime('%m/%d/%Y'))
     
                #day = c.start_time.day
                #month = c.start_time.month
                #year = c.start_time.year
                
                if c.start_time.strftime('%m/%d/%Y') >= form['startDate'].data and c.start_time.strftime('%m/%d/%Y') <= form['endDate'].data:
                    total_minutes += c.total_time
                    times.append(c)
        else:
            state = 'please fill in both fields'
            return render_to_response('datepicker.html', {'state':state})
        hour = total_minutes / 60
        minutes = total_minutes - (hour * 60)
        if minutes < 10:
            minutes = "0" + str(minutes)
        return render(self.request, 'empTime.html', {'form':form, 'manager':manager, 'clocks':times,'hour':hour, 'startDate':form['startDate'].data,  'endDate':form['endDate'].data, 'minutes':minutes})

class SelectedEmployee(View):
    def get(self, request, userId):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        if not check_manager(request):
            return HttpResponseRedirect('/clock')
        currEmployee = Person.objects.get(user=userId)
        return render(request, 'selectedEmployee.html', {'Employee':currEmployee})

class Clocking (View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        person = Person.objects.get(user=request.user)
        now = datetime.datetime.now()
        typeOfTime = "Clock in"
        clock = person.curr_clock
        if clock is not None:
            if clock.is_active is True:
                typeOfTime = "Clock Out"
        userID = request.user.id
        manager = check_manager(request)
        if clock is not None:
            started = clock.start_time
            resume_time = int((now - started).total_seconds())
        else:
            resume_time = 0
        return render(request, 'clock.html', {'now':now, 'type': typeOfTime, 'userID':userID, 'manager':manager,'resume':resume_time})
        # send_mail('Test messages from server', 'Hi, you clocked in or out.', 'aetas.me@gmail.com', ['jrthom18@gmail.com'], fail_silently=False)
        

def check_if_exists(username_check, email_check):
    count = False
    returnValue = 'h'
    try:
        User.objects.get(email=email_check)

    except User.DoesNotExist:
        returnValue = 'not'

    if returnValue is not 'not':
        return 'email'

    try:
        User.objects.get(username=username_check)

    except User.DoesNotExist:
        returnValue = 'not'

    if returnValue is not 'not':
        return 'username'
    
    return 'valid'

class DateRange(FormView):
    template_name = 'time_card.html'
    form_class = DateRangeForm1
    success_url = '/time_card/'

    def get(self,request):
        times = []
        form = DateRangeForm1(request.GET)
        manager = check_manager(request)
        if form.is_valid():
            clocks = Clocks.objects.filter(user=request.user).exclude(total_time=0)
            total_minutes = 0
            for c in clocks:
                
                # print(c.start_time.strftime('%m/%d/%Y'))
     
                #day = c.start_time.day
                #month = c.start_time.month
                #year = c.start_time.year
                
                if c.start_time.strftime('%m/%d/%Y') >= form['startDate'].data and c.start_time.strftime('%m/%d/%Y') <= form['endDate'].data:
                    total_minutes += c.total_time
                    times.append(c)
        else:
            return HttpResponseRedirect('/time_card')

        hour = total_minutes / 60
        minutes = total_minutes - (hour * 60)
        if minutes < 10:
            minutes = "0" + str(minutes)
        return render(self.request, 'time_card.html', {'form':form, 'manager':manager, 'clocks':times,'hour':hour, 'startDate':form['startDate'].data,  'endDate':form['endDate'].data, 'minutes':minutes})

class JobCostDateRange(FormView):
    template_name = 'reports.html'
    form_class = DateRangeForm2
    success_url = '/reports/'

    def get(self,request):
        jobCostSaves = []
        form = DateRangeForm(request.GET)
        manager = check_manager(request)
        currPerson = Person.objects.get(user=request.user)
        company = currPerson.company
        projects = company.project_set.all()
        if form.is_valid():
            clocks = Clocks.objects.filter(user=request.user).exclude(total_time=0)
            total_minutes = 0
            print(form['startDate'].data)
            print(form['endDate'].data)

            #for c in clocks:
            #for save in project.jobcostsave_set.all:
                
                # print(c.start_time.strftime('%m/%d/%Y'))
     
                #day = c.start_time.day
                #month = c.start_time.month
                #year = c.start_time.year
                
            #if c.start_time.strftime('%m/%d/%Y') >= form['startDate'].data and c.start_time.strftime('%m/%d/%Y') <= form['endDate'].data:
            #    total_minutes += c.total_time
            #    jobCostSaves.append(c)
        else:
            return HttpResponseRedirect('/reports')

        hour = total_minutes / 60
        minutes = total_minutes - (hour * 60)
        if minutes < 10:
            minutes = "0" + str(minutes)
        return render(self.request, 'reports.html', {'projects':projects,'form':form, 'manager':manager}) #, 'clocks':jobCostSaves,'hour':hour, 'startDate':form['startDate'].data,  'endDate':form['endDate'].data, 'minutes':minutes})

class Login(FormView):
    template_name = 'auth.html'
    form_class = LoginForm
    success_url = '/clock/'
    state = " "
    
    def form_invalid(self, form):
        state = "Please enter a username and password"
        # form.errors['non_field_errors'] = ['Invalid login']
        return render(self.request, 'auth.html', {'state': state, 'form':form})

    def form_valid(self, form):

        user = authenticate(username=form.cleaned_data['username'], 
                            password=form.cleaned_data['password'])

        if user is not None:
            if user.is_active:
                userId = user.id
                currentPerson = Person.objects.get(user=userId)
                self.request.session['currentPerson'] = userId
                login(self.request, user)
                return super(Login, self).form_valid(self.request)
            else:
                state = "Your account is not active"
                return render(self.request, 'auth.html', {'state': state, 'form': form})
        else:
            state = "Invalid login"
            return render(self.request, 'auth.html', {'state': state, 'form': form})


class TimeCard(View):
    def get(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        currPerson = Person.objects.get(user=request.user)
        typeOfTime = "Clock in"
        clock = currPerson.curr_clock
        if clock is not None:
            if clock.is_active is True:
                typeOfTime = "Clock Out"
        manager = check_manager(request)
        clocks = Clocks.objects.filter(user=request.user).exclude(total_time=0)
        total_minutes = 0
        for c in clocks:
            total_minutes += c.total_time
        hour = total_minutes / 60
        minutes = total_minutes - (hour * 60)
        if minutes < 10:
            minutes = "0" + str(minutes)
        return render(request, 'time_card.html', {'manager':manager, 'type':typeOfTime, 'clocks':clocks, 'hour':hour, 'minutes':minutes})


class AddEmployee(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        manager = check_manager(request)
        return render(request, 'addEmployee.html', {'manager':manager})


class Account(View):
    def get(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        currPerson = Person.objects.get(user=request.user)
        typeOfTime = "Clock in"
        clock = currPerson.curr_clock
        if clock is not None:
            if clock.is_active is True:
                typeOfTime = "Clock Out"
        manager = check_manager(request)
        return render(request, 'accounts/account.html', {'manager':manager, 'type':typeOfTime, 'currPerson':currPerson})


class EditAccount(View):
    def get(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        currPerson = Person.objects.get(user=request.user)
        form = UpdateAccountForm(instance=currPerson)
        manager = check_manager(request)
        return render(request, 'accounts/edit_account.html', {'manager':manager,
                                                     'form': form })
    def post(self,request):
        currPerson = Person.objects.get(user=request.user)
        form = UpdateAccountForm(request.POST, instance=currPerson)
        manager = check_manager(request)
        form.save()
        msg = "Account details updated"
        return render(request, 'accounts/account.html', {'manager':manager,
                                                         'form': form,
                                                          'message':msg })

class ChangePassword(View):
    def get(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        currPerson = Person.objects.get(user=request.user)
        form = UpdatePasswordForm(request.GET)
        manager = check_manager(request)
        message = ["","",""]
        return render(request, 'accounts/change_password.html', {'manager':manager,'form':zip(form,message),'currPerson':currPerson})
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        currPerson = Person.objects.get(user=request.user)
        form = UpdatePasswordForm(request.POST)
        manager = check_manager(request)
        message = ["","",""]
        if form.is_valid(): # If the form is filled in
            old_password_is_correct, new_passwords_match = False, False
            user = request.user
            current_password = form.cleaned_data['currentPassword']
            new_password = form.cleaned_data['newPassword']
            confirm_new_password = form.cleaned_data['confirmNewPassword']
            if not user.check_password(current_password):
                message[0] = "Password is incorrect"
            else:
                old_password_is_correct = True
            if new_password != confirm_new_password:
                message[1] = "New password did not match"
            else:
                new_passwords_match = True
            if old_password_is_correct and new_passwords_match:
                user.set_password(new_password)
                user.save()
                message = "Password successfully updated"
                return render(request, 'accounts/account.html', {'manager':manager,'message':message,'currPerson':currPerson})

        return render(request, 'accounts/change_password.html', {'manager':manager,'form':zip(form,message),'currPerson':currPerson})


def check_manager(request):
    person = Person.objects.get(user=request.user.id)
    if person.manager is True:
        use = 'yes'
    else:
        use = 'no'
    return use

def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/login/')


class ManageCompany(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/')
        currPerson = Person.objects.get(user = request.user)
        typeOfTime = "Clock in"
        clock = currPerson.curr_clock
        if clock is not None:
            if clock.is_active is True:
                typeOfTime = "Clock Out"
        manager = check_manager(request)
        projects = Project.objects.filter(company=currPerson.company)
        groups = EmployeeGroups.objects.filter(company=currPerson.company)
        employees = Person.objects.filter(company=currPerson.company)
        company = Company.objects.get(id=currPerson.company.id)
        return render(request, 'manage/manage.html', {'manager':manager, 'type':typeOfTime, 'currPerson':currPerson, 'projects':projects,
         'groups':groups, 'Employees':employees, 'comp':company})

class AddProject(View):
    def get(self, request):
        form = addProjectForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['projectName']
            description = form.cleaned_data['description']
            curUser = Person.objects.get(user=request.user)
            company = curUser.company
            group = EmployeeGroups.objects.get(id=request.GET['group'])
            newProject = Project(name=name, description=description, company=company)
            newProject.save()

            newGroup = GroupProject(group=group, project=newProject)
            newGroup.save()
            return HttpResponseRedirect('/manage/')
        return HttpResponseRedirect('/manage/')


class AddToGroup(View):
    def get(self, request):
        gro = request.GET['group']
        emp = request.GET['emp']
        currentUser = Person.objects.get(user=request.user)
        company = currentUser.company
        employee = Person.objects.get(id=emp)
        group = EmployeeGroups.objects.get(id=gro)

        # only add employee to group if they are not already in the group
        if EmployeeInGroup.objects.filter(employee=employee, Group=group, company=company).exists() is False:
            newAddedEmp = EmployeeInGroup(employee=employee, Group=group, company=company)
            newAddedEmp.save()
        
        return HttpResponseRedirect('/manage/')


class AddGroup(View):
    def get(self, request):
        form = addEmployeeGroupForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['name']
            currPerson = Person.objects.get(user=request.user)
            company = currPerson.company
            newGroup = EmployeeGroups(name=name, company=company)
            newGroup.save()
        return HttpResponseRedirect('/manage/')

class Reports(View):
    def get(self, request):
        manager = check_manager(request)
        currPerson = Person.objects.get(user=request.user)
        typeOfTime = "Clock in"
        clock = currPerson.curr_clock
        if clock is not None:
            if clock.is_active is True:
                typeOfTime = "Clock Out"
        company = currPerson.company
        projects = company.project_set.all()
        return render_to_response('reports.html', {'manager':manager, 'type':typeOfTime, 'projects':projects})


class EmployeeReports(View):
    def get(self, request):
        return render_to_response('employee_date.html')

class JobCostingReports(View):
    def get(self, request):
        currPerson = Person.objects.get(user=request.user)
        company = currPerson.company
        projects = company.project_set.all()
        return render_to_response('jobCostReportsDatePicker.html', {'Projects':projects})

class EmployeeReportList(View):
    def get(self, request):
        names = []
        totalTime = []
        form = DateRangeForm1(request.GET)
        startDate = form['startDate'].data
        endDate = form['endDate'].data
        manager = check_manager(request)
        currPerson = Person.objects.get(user=request.user)
        count = 0
        if form.is_valid():
            myEmployees = Person.objects.filter(company=currPerson.company)
            for emp in myEmployees:
                times = []
                names.append(emp.first_name + " " + emp.last_name)
                total_minutes = 0
                empUser = emp.user
                clocks = Clocks.objects.filter(user=empUser).exclude(total_time=0)
                for c in clocks:
                    if c.start_time.strftime('%m/%d/%Y') >= form['startDate'].data and c.start_time.strftime('%m/%d/%Y') <= form['endDate'].data:
                        total_minutes += c.total_time
                        times.append(c)
                hour = total_minutes / 60
                minutes = total_minutes - (hour * 60)
                if minutes < 10:
                    minutes = "0" + str(minutes)
                time = str(hour) + ":" + str(minutes)
                totalTime.append(time)
                count += 1
            return render_to_response('employee_reports.html', {'startDate':startDate,'endDate':endDate,'names':names, 'totalTimes':totalTime, 'count':count})
        else:
            state = 'please fill in both fields'
            return render_to_response('employee_date.html', {'state':state})

class JobCostingData(View):
    #template_name = 'reports.html'
    #form_class = DateRangeForm
    #success_url = '/reports/'

    def get(self,request):
        jobCostSaves = []
        form = DateRangeForm2(request.GET)
        manager = check_manager(request)
        startDate = form['startDate'].data
        endDate = form['endDate'].data
        projectName = form['projectName'].data
        currPerson = Person.objects.get(user=request.user)
        company = currPerson.company
        projects = company.project_set.all()
        for project in projects:
            if project.name == projectName:
                currentProject = project

        state = ""
        if form.is_valid():
            clocks = Clocks.objects.filter(user=request.user).exclude(total_time=0)
            total_minutes = 0
            timePerEmployeeInMinutes = currentProject.get_time_per_employee_in_minutes(startDate,endDate)
            totalProjectTimeFormatted = currentProject.get_time_spent_formatted(startDate,endDate)
            timePerEmployeeFormatted = currentProject.get_time_per_employee_formatted(startDate,endDate)

            manager = check_manager(request)
            print currentProject.id
            typeOfTime = "Clock in"
            clock = currPerson.curr_clock
            if clock is not None:
                if clock.is_active is True:
                    typeOfTime = "Clock Out"
            return render_to_response('jobCostReports.html', {'timePerEmployeeFormatted':timePerEmployeeFormatted,'totalProjectTimeFormatted':totalProjectTimeFormatted,'timePerEmployeeInMinutes':timePerEmployeeInMinutes,'selectedProject':currentProject,'projectName':currentProject.name,'startDate':startDate,'endDate':endDate,'manager':manager, 'type':typeOfTime, 'projects':projects })
        else:
            state = "Please enter both fields for start and end date."
            return render_to_response('jobCostReportsDatePicker.html', {'state':state})

class SaveNewEmployee(View):
    def get(self, request):

        currPerson = Person.objects.get(user=request.user)
        manager = check_manager(request)
        form = addEmployeeForm(request.GET)
        
        if form.is_valid():
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            phoneNumber = form.cleaned_data['phoneNumber']
            password = form.cleaned_data['password']
            userName = form.cleaned_data['userName']

            valid = check_if_exists(userName, email)
            if valid is not 'valid':
                if valid is 'username':
                    state = 'Please select a unique username'
                    return render(request, 'addEmployee.html', {'firstName':firstName, 'lastName':lastName, 'email':email,
                        'phoneNumber':phoneNumber, 'state':state, 'manager':manager})
                if valid is 'email':
                    state = 'The email you have entered is already registered'
                    return render(request, 'addEmployee.html', {'firstName':firstName, 'lastName':lastName, 'userName':userName,
                        'phoneNumber':phoneNumber, 'state':state, 'manager':manager})

            state = 'Successfully registered employee'
            newUser = User.objects.create_user(username=userName, email=email, password=password)
            newUser.save()
            uId = newUser.id
                #create person now
            person = Person.objects.get(user=request.session['currentPerson'])
            companyUse = person.company
            newPerson = Person(user=newUser, first_name=firstName, last_name=lastName, phone_number=phoneNumber, company=companyUse)
            newPerson.save()
            return render(request, 'addEmployee.html', {'state':state})
        state = 'Please fill in all the information'
        firstName = request.GET.get('firstName')
        lastName = request.GET.get('lastName')
        email = request.GET.get('email')
        phoneNumber = request.GET.get('phoneNumber')
        password = request.GET.get('password')
        userName = request.GET.get('userName')
        return render_to_response('addEmployee.html', {'firstName':firstName, 'lastName':lastName, 'email':email,
            'phoneNumber':phoneNumber, 'state':state, 'userName':userName, 'manager':manager}, context_instance=RequestContext(request))


