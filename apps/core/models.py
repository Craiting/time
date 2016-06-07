from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import utc
import datetime

class Clocks(models.Model):
    def calc_time(self):
        if self.start_time != None and self.end_time != None:
            return self.end_time - self.start_time
        else:
            return None
    user = models.ForeignKey(User, blank=True, null=True)
    start_time = models.DateTimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)
    end_time = models.DateTimeField(null=True,blank=True)
    total_time = models.IntegerField(default=None,null=True,blank=True)

    def __unicode__(self):
        return str(self.id)
    

class TimeEntry(models.Model):
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True,null=True)
    user = models.ForeignKey(User, blank=True,null=True)

    def __unicode__(self):
        return self.description


class Company(models.Model):
    company_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    # fixing issue with adding new project?
    company_id = models.CharField(max_length=100, null=True, blank=True) 

    def __unicode__(self):
        return self.company_name


class Person(models.Model):

    user = models.ForeignKey(User, blank=True,null=True)
    curr_clock = models.ForeignKey(Clocks, blank=True, null=True)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=100, null=False, blank=False)
    company = models.ForeignKey(Company) #foreign key
    manager = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name


class EmployeeGroups(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    company = models.ForeignKey(Company, null= False, blank=False)
    def __unicode__(self):
        return self.name + "-" + self.company.company_name


class EmployeeInGroup(models.Model):
    employee = models.ForeignKey(Person, blank=False, null=False)
    Group = models.ForeignKey(EmployeeGroups, blank=False, null=False)
    company = models.ForeignKey(Company, blank=False, null=False)
    def __unicode__(self):
        return self.employee.first_name + " " + self.employee.last_name + "-" + self.Group.name + '-' + self.company.company_name


class Project(models.Model):
    # group = models.ForeignKey(EmployeeGroups,null=False,blank=False)
    company = models.ForeignKey(Company,null=False,blank=False)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    def get_time_spent_formatted(self,startDate,endDate):
        saves = self.jobcostsave_set.all()
        mins = 0
        for s in saves:
            if s.formatDate() >= startDate and s.formatDate() <= endDate:
                mins += s.minutes

        if mins%60 < 10:
            return str(mins/60) + ':0' + str(mins%60)
        else:
            return str(mins/60) + ':' + str(mins%60)
    
    def get_time_spent_in_minutes(self,startDate,endDate):
        saves = self.jobcostsave_set.all()
        mins = 0
        for s in saves:
            if s.formatDate() >= startDate and s.formatDate() <= endDate:
                mins += s.minutes
        return mins

    def get_total_time_in_minutes(self):
        saves = self.jobcostsave_set.all()
        mins = 0
        for s in saves:
            mins += s.minutes
        return mins

    # track time spent per employee per project
    def get_time_per_employee_formatted(self,startDate,endDate):
        saves = self.jobcostsave_set.all()
        mins = 0
        employeesOnProject = {}

        for s in saves:
            if not s.user in employeesOnProject:
                employeesOnProject[s.user] = 0
        for s in saves:
            if s.formatDate() >= startDate and s.formatDate() <= endDate:
                employeesOnProject[s.user] += s.minutes

        for key,value in employeesOnProject.items():
            if employeesOnProject[key]%60 < 10:
                employeesOnProject[key] = str(employeesOnProject[key]/60) + ':0' + str(employeesOnProject[key]%60)
            else:
                employeesOnProject[key] =  str(employeesOnProject[key]/60) + ':' + str(employeesOnProject[key]%60)
        return employeesOnProject

    def get_time_per_employee_in_minutes(self,startDate,endDate):
        saves = self.jobcostsave_set.all()
        mins = 0
        employeesOnProject = {}
        print startDate
        print endDate

        for s in saves:
            if not s.user in employeesOnProject:
                employeesOnProject[s.user] = 0
        for s in saves:
            print s.formatDate()
            if s.formatDate() >= startDate and s.formatDate() <= endDate:
                print("Save from " + str(s.date) + " added.")
                employeesOnProject[s.user] += s.minutes

        return employeesOnProject

    def __unicode__(self):
        return self.name #+ "-" + self.company.company_name


class GroupProject(models.Model):
    group = models.ForeignKey(EmployeeGroups, blank=False, null=False)
    project = models.ForeignKey(Project, blank=False, null=False)
    # fixing issue with adding new project?
    company = models.ForeignKey(Company, blank=False, null=True)

    def __unicode__(self):
        return self.group.name + "-" + self.project.name


class ProjectUsers(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(Person)


class JobCostSave(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(Person)
    minutes = models.IntegerField(default=None,null=True,blank=True)
    date = models.DateTimeField(null=True,blank=True)
    ugh = models.CharField(null=True, max_length=2, blank=True)

    def __unicode__(self):
        return str(self.project) + '-' + str(self.user) + '-min:' + str(self.minutes)

    def toHourAndMinutes(self):
        if self.minutes%60 < 10:
            return str(self.minutes/60) + ':0' + str(self.minutes%60)
        else:
            return str(self.minutes/60) + ':' + str(self.minutes%60)

    def formatDate(self):
        return self.date.strftime('%m/%d/%Y')

def get_time_diff(self):
    if self.time_posted:
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - self.time_posted
        return timediff.total_seconds()

