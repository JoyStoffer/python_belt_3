from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import User


def flash_errors(errors, request):
    for error in errors:
        messages.error(request, error)

def current_user(request):
    return User.objects.get(id = request.session['user_id'])

def index(request):

    return render(request, 'loginreg_app/index.html')

# def success(request):
#     if 'user_id' in request.session:
#         context = {
#             'user':current_user(request)
#         }
#         return render(request, 'loginreg_app/success.html', context)
#
#     return render(reverse('landing'))

def register(request):
    if request.method =="POST":
            #validate form data
        errors = User.objects.validate_registration(request.POST)
        #check if errors don't exist
        if not errors:
            #create User
            user = User.objects.create_user(request.POST)

            #login the User
            request.session['user_id'] = user.id

            #redirect to success page
            return redirect(reverse('all_friends'))
        #flash errors
        flash_errors(errors, request)
    #redirect landing
    return redirect(reverse('landing'))


def login(request):
    if request.method == "POST":
        # validate my login data
        check = User.objects.validate_login(request.POST)

        #check if retrieved a valid user
        if 'user' in check:

            #login user
            request.session['user_id'] = check ["user"].id

            #redirect to success page
            return redirect(reverse('all_friends'))

        #Flash Error messages
        flash_errors(check['errors'], request)

    return redirect(reverse ('landing'))

def logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id')

    return redirect(reverse('landing'))
