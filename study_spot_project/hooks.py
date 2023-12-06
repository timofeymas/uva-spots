# https://pypi.org/project/django-google-sso/

def pre_login_user(user, request):

    if not user.username and user.email:
        user.username = user.email
        user.save()
        
    pass