# type: ignore

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Tracker, TrackerSymbols
from .services.dashboard_index_service import DashboardIndexService


@login_required(login_url='/login')
def index(request):

    user = request.user
    dashboard_index_svc = DashboardIndexService()

    if not dashboard_index_svc.user_has_trackers(user):
        dashboard_index_svc.create_default_tracker(user)

    tracker = Tracker.objects.get(user=user)

    return render(request, 'dashboard.html', {
        "tracker_name": tracker.name,
        "tracker_symbol_count": TrackerSymbols.objects.filter(tracker=tracker).count()
    })
