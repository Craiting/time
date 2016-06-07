from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return view
        # result = login_required(view)
        # print result
        # return result
        # redirect("/login/")