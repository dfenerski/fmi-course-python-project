# type: ignore

import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from dashboard.services.dashboard_symbols_service import DashboardSymbolsService
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


class DashboardSymbols(View):
    def get(self, request, tracker_id):
        user = request.user
        # dashboard_symbols_svc = DashboardSymbolsService()

        # Validate ownership
        if not Tracker.objects.filter(pk=tracker_id, user=user).exists():
            return HttpResponseBadRequest("Invalid request")

        tracker_symbols = TrackerSymbols.objects.filter(tracker=tracker_id).select_related()

        return render(request, 'dashboard_symbols.html', {
            "tracker_name": tracker_symbols[0].tracker.name,
            "tracker_symbols": tracker_symbols
        })

    def post(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            return HttpResponseBadRequest(f'Invalid JSON: {e}')

        return JsonResponse({'message': 'Data received', 'payload': payload})
