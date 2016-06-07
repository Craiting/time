from django.conf.urls import patterns, include, url
import os
from django.contrib import admin
admin.autodiscover()

# Not sure about this:
from apps.core.views import *

urlpatterns = patterns('',
    url(r'^$', SplashPage.as_view(), name='splash'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^contact_us/', ContactUs.as_view(), name='contact_us'),
    url(r'^submission/', Submission.as_view(), name='submission'),
    url(r'^login/?$', Login.as_view(), name='login_user'),
    url(r'^logout/?$', 'apps.core.views.logout_user', name='logout'),
    url(r'^clock/?$', Clocking.as_view(), name='clock'),
    url(r'^end_clock/(?P<userId>\d+)/?$', EndClock.as_view(), name='no'),
    url(r'^jobcost/?$', EndClock.as_view(), name='jobcost'),
    url(r'^update_clock/(?P<userId>\d+)/?$', UpdateClock.as_view(), name='clocking'),
    url(r'^time_card/?$', TimeCard.as_view(), name='time_card'),
    url(r'^employees/?$', Employees.as_view(), name='employees'),
    url(r'^selectedEmployee/(?P<userId>\d+)/?$', SelectedEmployee.as_view(), name='selEmp'),
    url(r'^account/?$', Account.as_view(), name='account'),
    url(r'^account/edit/?$', EditAccount.as_view(), name='edit_account'),
    url(r'^account/change_password/?$', ChangePassword.as_view(), name='change_password'),
    url(r'^add_employee/?$', AddEmployee.as_view(), name='Add Employee'),
    url(r'^saveNewEmployee/?$', SaveNewEmployee.as_view(), name='saveNewEmployee'),
    url(r'^dateRange/?$', DateRange.as_view(), name='dateRange'),
    url(r'^jobCostDateRange/?$', JobCostDateRange.as_view(), name='jobCostDateRange'),
    url(r'^manage/?$', ManageCompany.as_view(), name='manage_company'),
    url(r'^manage/addProject/?$', AddProject.as_view(), name='AddProject'),
    url(r'^manage/addGroup/?$', AddGroup.as_view(), name='AddGroup'),
    url(r'^manage/addToGroup/?$', AddToGroup.as_view(), name='Add To Group'),
    url(r'^user/password/reset/$', 'django.contrib.auth.views.password_reset', {'post_reset_redirect' : '/user/password/reset/done/'}, name="password_reset_form"),
    url(r'^user/password/reset/done/$','django.contrib.auth.views.password_reset_done'),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect' : '/user/password/done/'}, name='password_reset_confirm'),
    url(r'^user/password/done/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^reports/?$', Reports.as_view(), name="reports"),
    url(r'^reports/employee?$', EmployeeReports.as_view(), name='reports'),
    url(r'^reports/jobCosting?$', JobCostingReports.as_view(), name='jobCostingReports'),
    url(r'^reports/info?$', EmployeeReportList.as_view(), name='info'),
    url(r'^reports/jobCostingData?$', JobCostingData.as_view(), name='jobCostingData'),
    url(r'^datepicker/emp/(?P<userId>\d+)/?$', EmployeeDate.as_view(), name='employeeDate'),
    url(r'^employee/timecard/(?P<userId>\d+)/?$', EmployeeTime.as_view(), name='emp time')
)
