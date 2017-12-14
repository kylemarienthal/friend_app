from django.shortcuts import render, redirect, reverse
from ..log_reg_app.models import User

# Create your views here.
def all_friends(request):
    current_user = User.objects.current_user(request)
    friends = current_user.friends.all()
    other_people = User.objects.exclude(id=current_user.id).exclude(id__in=friends)
    context = {
        'user' : current_user,
        'friends' : friends,
        'other_people' : other_people,
    }
    return render(request, 'friend_app/all_friends.html', context)

def user_profile(request, id):
    other_persons_profile = User.objects.filter(id=id).first()
    context = {
        'other_persons_profile' : other_persons_profile
    }
    return render(request, 'friend_app/profile.html', context)

def add_friend(request, id):
    current_user = User.objects.current_user(request)
    friend = User.objects.filter(id=id).first()
    current_user.friends.add(friend)
    return redirect(reverse('dashboard'))

def remove_friend(request, id):
    current_user = User.objects.current_user(request)
    friend = User.objects.filter(id=id).first()
    current_user.friends.remove(friend)
    return redirect(reverse('dashboard'))
