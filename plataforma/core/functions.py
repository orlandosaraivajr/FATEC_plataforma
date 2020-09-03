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
    else:
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
