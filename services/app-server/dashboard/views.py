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
        "tracker_id": tracker.id,
        "tracker_name": tracker.name,
        "tracker_symbol_count": TrackerSymbols.objects.filter(tracker=tracker).count()
    })


class DashboardSymbols(View):
    def get(self, request, tracker_id):
        user = request.user

        # Validate ownership
        if not Tracker.objects.filter(pk=tracker_id, user=user).exists():
            return HttpResponseBadRequest("Invalid request")

        # Extract tracker symbols
        tracker_symbols = TrackerSymbols.objects.filter(tracker=tracker_id).select_related()

        return render(request, 'dashboard_symbols.html', {
            "tracker_name": tracker_symbols[0].tracker.name,
            "tracker_symbols": tracker_symbols
        })

    def post(self, request, tracker_id):
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            return HttpResponseBadRequest(f'Invalid JSON: {e}')

        user = request.user
        dashboard_symbols_svc = DashboardSymbolsService()

        # Validate ownership
        tracker = Tracker.objects.filter(pk=tracker_id, user=user)
        if not tracker.exists():
            return HttpResponseBadRequest("Invalid request")

        # Add new symbol to tracker
        symbol = dashboard_symbols_svc.add_symbol_to_tracker(payload.get('symbol'), tracker[0].id)
        tracker_symbol = TrackerSymbols.objects.filter(tracker=tracker_id, symbol=symbol.id).select_related()[0]

        return JsonResponse({
            "id": tracker_symbol.id,
            "symbol_name": tracker_symbol.symbol.name,
            "symbol_symbol": tracker_symbol.symbol.symbol,
            "symbol_industry": tracker_symbol.symbol.industry,
            "symbol_sector": tracker_symbol.symbol.sector,
            "symbol_businessSummary": tracker_symbol.symbol.businessSummary,
            "symbol_ir_website": tracker_symbol.symbol.irWebsite,
            "created_at": tracker_symbol.created_at,
            "modified_at": tracker_symbol.modified_at,
            "metadata": tracker_symbol.metadata,
        })

    def delete(self, request, tracker_id):
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            return HttpResponseBadRequest(f'Invalid JSON: {e}')

        user = request.user
        dashboard_symbols_svc = DashboardSymbolsService()

        # Validate ownership
        tracker = Tracker.objects.filter(pk=tracker_id, user=user)
        if not tracker.exists():
            return HttpResponseBadRequest("Invalid request")

        # Remove symbol from tracker
        symbol = payload.get('symbol')
        dashboard_symbols_svc.remove_symbol_from_tracker(symbol, tracker[0].id)

        return JsonResponse({'deleted': symbol})
