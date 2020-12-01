from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.utils.datastructures import MultiValueDictKeyError


def auth_request(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
        except MultiValueDictKeyError:
            return False
        user = authenticate(email=username, password=password)
        if user is not None:
            auth_login(request, user)
            return True
    return False


def authenticate(email=None, password=None):
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password) and user.is_active:
            return user
    return None


def register_new_student(email=None, password=None):
    if email and password:
        User = get_user_model()
        novo_aluno = User.objects.create_user(
            email, email, password, is_student=True)
        novo_aluno.save()
        return True
    else:
        return False


def register_student(**kwargs):
    name = kwargs.get('first_name', None)
    last_name = kwargs.get('last_name', None)
    email = kwargs.get('username', None)
    password = kwargs.get('password', None)
    if name and email and password:
        User = get_user_model()
        novo_aluno = User.objects.create_user(
            first_name=name, last_name=last_name,
            username=email, email=email,
            password=password, is_student=True)
        novo_aluno.save()
        return True
    else:
        return False


def register_new_teacher(email=None, password=None):
    if email and password:
        User = get_user_model()
        novo_professor = User.objects.create_user(
            email, email, password, is_teacher=True)
        novo_professor.save()
        return True
    else:
        return False


def register_new_company(email=None, password=None):
    if email and password:
        User = get_user_model()
        novo_professor = User.objects.create_user(
            email, email, password, is_company=True)
        novo_professor.save()
        return True
    else:
        return False


def register_new_admin(email=None, password=None):
    if email and password:
        User = get_user_model()
        novo_admin = User.objects.create_user(
            email, email, password, is_superuser=True)
        novo_admin.save()
        return True
    else:
        return False


def update_user(id=None, password=None, first_name='', last_name=''):
    if id and password:
        User = get_user_model()
        usuario = User.objects.get(id=id)
        usuario.set_password(password)
        usuario.first_name = first_name
        usuario.last_name = last_name
        usuario.save()
        return True
    else:
        return False
