from db_models_shared.symbol import Symbol
from yfinance import Ticker
from common_util.singleton import Singleton
from common_util.logger import Logger
from db_models_shared.symbol_history_entry import SymbolHistoryEntry


class EtlSymbolHistory(metaclass=Singleton):

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    def run_pipeline(self, symbol, period="3mo"):
        self.logger.log(f"Import starting for symbol: {symbol}")

        ticker = Ticker(symbol)

        symbol_instance = Symbol.objects.get(symbol=symbol)
        # https://docs.djangoproject.com/en/5.1/topics/db/queries/#limiting-querysets
        # https://stackoverflow.com/a/20049773/13163112
        last_entry = SymbolHistoryEntry.objects.filter(symbol=symbol_instance.id).order_by('-timestamp').first()

        ticker_history = ticker.history(period=period) if not last_entry else ticker.history(start=last_entry.timestamp.strftime("%Y-%m-%d"))

        # https://docs.djangoproject.com/en/5.1/ref/models/querysets/#bulk-create
        # https://stackoverflow.com/a/29816143/13163112
        # https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.Timestamp.to_pydatetime.html#pandas.Timestamp.to_pydatetime
        symbol_history_entries = SymbolHistoryEntry.objects.bulk_create(
            [SymbolHistoryEntry(
                symbol=symbol_instance,
                timestamp=entry.get('Date').to_pydatetime(),
                close_price=entry.get('Close'),
                volume=entry.get('Volume'),

            ) for entry in ticker_history.reset_index().to_dict('records')],
            ignore_conflicts=True
        )

        self.logger.log(f"Import finished for symbol: {symbol}")

        return symbol_history_entries
