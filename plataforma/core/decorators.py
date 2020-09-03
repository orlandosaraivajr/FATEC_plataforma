from django.shortcuts import redirect
from plataforma import settings


def area_student(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = settings.HOME_URL

    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_student:
                return function(request, *args, **kwargs)
            else:
                return redirect(redirect_url)
        else:
            return redirect(settings.LOGIN_URL)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def area_teacher(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = settings.HOME_URL

    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_teacher:
                return function(request, *args, **kwargs)
            else:
                return redirect(redirect_url)
        else:
            return redirect(settings.LOGIN_URL)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def area_trainee_coordinador(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = settings.HOME_URL

    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_trainee_coordinator:
                return function(request, *args, **kwargs)
            else:
                return redirect(redirect_url)
        else:
            return redirect(settings.LOGIN_URL)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def area_company(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = settings.HOME_URL

    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_company:
                return function(request, *args, **kwargs)
            else:
                return redirect(redirect_url)
        else:
            return redirect(settings.LOGIN_URL)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def area_admin(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = settings.HOME_URL

    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return function(request, *args, **kwargs)
            else:
                return redirect(redirect_url)
        else:
            return redirect(settings.LOGIN_URL)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
