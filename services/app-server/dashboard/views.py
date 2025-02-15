from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def index(request):
    print(request.user)
    print(request.user.id)
    return render(request, 'dashboard.html', {
        "my_symbols": 4
    })

