# type: ignore

from django.db import transaction
from etl.etl_symbol import EtlSymbol
from etl.etl_symbol_history import EtlSymbolHistory
from visualizer.kpi_service import KpiService
from visualizer.chart_service import ChartService
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

        symbol_aapl = self.get_symbol_graceful(DefaultSymbol.AAPL.value)
        symbol_goog = self.get_symbol_graceful(DefaultSymbol.GOOG.value)
        symbol_msft = self.get_symbol_graceful(DefaultSymbol.MSFT.value)
        symbol_nvda = self.get_symbol_graceful(DefaultSymbol.NVDA.value)
        symbol_meta = self.get_symbol_graceful(DefaultSymbol.META.value)

        default_tracker.symbols.add(symbol_aapl, through_defaults={'is_favorite': False, 'metadata': {}})
        default_tracker.symbols.add(symbol_goog, through_defaults={'is_favorite': False, 'metadata': {}})
        default_tracker.symbols.add(symbol_msft, through_defaults={'is_favorite': False, 'metadata': {}})
        default_tracker.symbols.add(symbol_nvda, through_defaults={'is_favorite': False, 'metadata': {}})
        default_tracker.symbols.add(symbol_meta, through_defaults={'is_favorite': False, 'metadata': {}})

        default_tracker.save()

    def generate_kpi_data(self, kpi_name, tracker_symbols):
        assert kpi_name in [
            "kpi_market_cap_pie",
            "kpi_buy_recommendations",
            "kpi_employee_count"
        ]

        tracker_symbols_daily = EtlSymbol().run_enhancements(tracker_symbols, ('marketCap', 'recommendationKey', 'fullTimeEmployees'))

        kpi_data = None
        if kpi_name == "kpi_market_cap_pie":
            kpi_data = KpiService().generate_market_cap_pie(tracker_symbols_daily)
        elif kpi_name == "kpi_buy_recommendations":
            kpi_data = KpiService().generate_buy_recommendations(tracker_symbols_daily)
        elif kpi_name == "kpi_employee_count":
            kpi_data = KpiService().generate_kpi_employee_count(tracker_symbols_daily)

        return kpi_data

    def generate_chart_data(self, chart_name, tracker_symbols):
        assert chart_name in [
            "chart_price_historical",
            "chart_price_historical_ma",
        ]

        tracker_symbols_history = []
        for symbol in tracker_symbols:
            tracker_symbols_history.append({
                "symbol": symbol,
                "data": EtlSymbolHistory().run_pipeline(symbol),
            })

        chart_data = None
        if chart_name == "chart_price_historical":
            chart_data = ChartService().generate_price_historical(tracker_symbols_history)
        elif chart_name == "chart_price_historical_ma":
            chart_data = ChartService().generate_price_historical_ma(tracker_symbols_history)

        return chart_data
