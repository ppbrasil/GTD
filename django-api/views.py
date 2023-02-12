from django.shortcuts import render

def dashboard(request):
    context = {'user': request.user}
    return render(request, 'dashboard.html', context)
