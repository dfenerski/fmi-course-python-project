# type: ignore

from django.db import transaction
from dashboard.models import Tracker
from common_util.default_symbol import DefaultSymbol
from dashboard.services.dashboard_base_service import DashboardBaseService


class DashboardIndexService(DashboardBaseService):
    def user_has_trackers(self, user):
        return Tracker.objects.filter(user=user).exists()

    @transaction.atomic
    def create_default_tracker(self, user):

        default_tracker = Tracker.objects.create(
            user=user,
            name="My first tracker",
            is_selected=True
        )

        default_tracker.symbols.add(self.get_symbol_graceful(DefaultSymbol.AAPL.value), through_defaults={'is_favorite': False, 'metadata': {}})
        default_tracker.symbols.add(self.get_symbol_graceful(DefaultSymbol.GOOG.value), through_defaults={'is_favorite': False, 'metadata': {}})
        default_tracker.symbols.add(self.get_symbol_graceful(DefaultSymbol.MSFT.value), through_defaults={'is_favorite': False, 'metadata': {}})
        default_tracker.symbols.add(self.get_symbol_graceful(DefaultSymbol.NVDA.value), through_defaults={'is_favorite': False, 'metadata': {}})
        default_tracker.symbols.add(self.get_symbol_graceful(DefaultSymbol.META.value), through_defaults={'is_favorite': False, 'metadata': {}})

        default_tracker.save()
