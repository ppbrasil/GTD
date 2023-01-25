from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
   print("I'm inside dashboard function")
   return render(request, 'dashboard.html')
   