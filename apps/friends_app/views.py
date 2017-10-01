from django.shortcuts import render, redirect, reverse
from ..loginreg_app.models import User
# Create your views here.





def index(request):
    current_user = User.objects.current_user(request)
    friends = current_user.friended.all()
    other_users = User.objects.exclude(id__in=friends).exclude(id = current_user.id)

    context = {
        'user': current_user,
        'friends': friends,
        'people': other_users,
    }
    return render(request, 'friends_app/index.html', context)

def add(request, id):
    current_user = User.objects.current_user(request)
    friend = User.objects.filter(id=id).first()

    current_user.friended.add(friend)

    return redirect(reverse('all_friends'))

def remove(request, id):
    current_user = User.objects.current_user(request)
    friend = User.objects.filter(id=id).first()

    current_user.friended.remove(friend)

    return redirect(reverse('all_friends'))

def user(request, id):

    context = {
        'user' : User.objects.filter(id=id).first(),
    }
    return render(request, "friends_app/user.html", context)
