from yfinance import Ticker
from common_util.singleton import Singleton
from common_util.logger import Logger
from db_models_shared.symbol import Symbol


class EtlSymbol(metaclass=Singleton):

    def __init__(self):
        self.logger = Logger(self.__class__.__name__)

    def run_pipeline(self, symbol):
        self.logger.log(f"Import starting for symbol: {symbol}")

        ticker = Ticker(symbol)
        ticker_info = ticker.info
        symbol_instance = Symbol.objects.create(
            name=ticker_info.get("shortName"),
            symbol=symbol,
            industry=ticker_info.get("industryKey"),
            sector=ticker_info.get("sectorKey"),
            businessSummary=ticker_info.get("longBusinessSummary"),
            irWebsite=ticker_info.get("irWebsite")
        )

        self.logger.log(f"Import finished for symbol: {symbol}")

        return symbol_instance

    def run_enhancements(self, symbols, enhancements):
        enhanced_data = []

        for symbol in symbols:
            print(symbol)
            enhanced_entry = {
                "symbol": symbol
            }

            ticker = Ticker(symbol)

            for enhancement in enhancements:
                enhanced_entry[enhancement] = ticker.info.get(enhancement)

            enhanced_data.append(enhanced_entry)

        return enhanced_data
