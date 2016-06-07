from django.test import TestCase, RequestFactory
from django.core.urlresolvers import resolve
from apps.core.views import SplashPage, Login
from django.http import HttpRequest
from django.contrib.auth.models import User
from apps.core.models import Company, Person
from apps.core.forms import LoginForm

class AetasTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_root_url_resolves_to_home_page(self):
        home_view = resolve('/')
        self.assertEqual(home_view.func.func_name, SplashPage.as_view().func_name)

    def test_login_view(self):
        login_view = resolve('/login')
        self.assertEqual(login_view.func.func_name, Login.as_view().func_name)

    def test_can_login(self):
        user = User.objects.create(username="test", password="test")
        company = Company.objects.create()
        person = Person.objects.create(user=user, company=company)        
        request = self.factory.post('/login')
        request.POST = {"username": user.username, "password": "test"}
        login_view = Login.as_view()
        response = login_view(request)
        self.assertEqual(response.status_code, 200)

    def test_bad_login(self):
        user = User.objects.create(username="test", password="test")
        company = Company.objects.create()
        person = Person.objects.create(user=user, company=company)
        request = HttpRequest()
        request.POST = {"username":"badusername","password":user.password}
        form = LoginForm(request.POST)
        login_view = Login()
        login_view.request = request
        response = login_view.post(form)
        self.assertEqual(response.status_code, 200)
