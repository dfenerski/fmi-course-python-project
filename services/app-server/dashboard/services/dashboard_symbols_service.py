# type: ignore

from dashboard.models import Tracker
from dashboard.services.dashboard_base_service import DashboardBaseService
from django.db import transaction


class DashboardSymbolsService(DashboardBaseService):

    @transaction.atomic
    def add_symbol_to_tracker(self, symbol, tracker_id):

        symbol_instance = self.get_symbol_graceful(symbol)

        Tracker.objects.get(pk=tracker_id).symbols.add(symbol_instance, through_defaults={'is_favorite': False, 'metadata': {}})

        return symbol_instance

    @transaction.atomic
    def remove_symbol_from_tracker(self, symbol, tracker_id):

        symbol_instance = self.get_symbol_graceful(symbol)

        Tracker.objects.get(pk=tracker_id).symbols.remove(symbol_instance)

        return symbol_instance
