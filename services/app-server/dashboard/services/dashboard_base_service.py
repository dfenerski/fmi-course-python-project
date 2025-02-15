# type: ignore

from common_util.singleton import Singleton
from db_models_shared.symbol import Symbol
from etl.etl_symbol import EtlSymbol


class DashboardBaseService(metaclass=Singleton):
    def get_symbol_graceful(self, symbol):
        if not Symbol.objects.filter(symbol=symbol).exists():
            symbol_instance = EtlSymbol().run_pipeline(symbol)
            return symbol_instance
        else:
            return Symbol.objects.get(symbol=symbol)
