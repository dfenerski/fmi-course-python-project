# type: ignore

from common_util.singleton import Singleton
from django.db import transaction
from dashboard.models import Tracker
from db_models_shared.symbol import Symbol
from etl.etl_symbol import EtlSymbol
from common_util.default_symbol import DefaultSymbol


class DashboardIndexService(metaclass=Singleton):
    def user_has_trackers(self, user):
        return Tracker.objects.filter(user=user).exists()

    def run_pipeline(self, symbol):
        symbol_instance = Symbol.objects.create(
            name="",
            symbol=symbol,
            industry="",
            sector="",
            businessSummary="",
            irWebsite=""
        )
        return symbol_instance

    def get_symbol_graceful(self, symbol):
        if not Symbol.objects.filter(symbol=symbol).exists():
            symbol_instance = EtlSymbol().run_pipeline(symbol)
            return symbol_instance
        else:
            return Symbol.objects.get(symbol=symbol)

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
