from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect('fingerprint')
    user = request.user
    in_relationship = user.participation and user.participation.relationship
    relationship, partner = None, None
    if in_relationship:
        relationship = user.participation.relationship
        partner: User = relationship.participants.exclude(pk=user.pk).first()
    return render(request, 'home.html', context={
            'user': request.user,
            'in_relationship': in_relationship,
            'relationship': relationship,
            'partner': partner,
        })
