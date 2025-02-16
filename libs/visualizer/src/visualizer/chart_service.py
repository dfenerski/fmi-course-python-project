import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from common_util.singleton import Singleton


class ChartService(metaclass=Singleton):
    def generate_price_historical(self, tracker_symbols_history):
        sns.set_theme(style="whitegrid")

        rows = []
        for symbol_history in tracker_symbols_history:
            for symbol_instance in symbol_history.get('data'):
                rows.append({
                    'symbol': symbol_history.get('symbol'),
                    'timestamp': symbol_instance.timestamp,
                    'close_price': symbol_instance.close_price
                })

        df = pd.DataFrame(rows)

        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, x="timestamp", y="close_price", hue="symbol", marker='o')

        # https://stackoverflow.com/a/38061400/13163112
        plot_file = io.BytesIO()
        plt.savefig(plot_file, format='png')
        plot_file.seek(0)

        return base64.b64encode(plot_file.read()).decode()

    def generate_price_historical_ma(self, tracker_symbols_history):
        sns.set_theme(style="whitegrid")

        rows = []
        for symbol_history in tracker_symbols_history:
            for symbol_instance in symbol_history.get('data'):
                rows.append({
                    'symbol': symbol_history.get('symbol'),
                    'timestamp': symbol_instance.timestamp,
                    'close_price': symbol_instance.close_price
                })

        df = pd.DataFrame(rows)
        df['ma_50'] = df.groupby('symbol')['close_price'].transform(lambda x: x.rolling(window=50, min_periods=1).mean())

        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, x="timestamp", y="ma_50", hue="symbol", marker='o')

        plot_file = io.BytesIO()
        plt.savefig(plot_file, format='png')
        plot_file.seek(0)

        return base64.b64encode(plot_file.read()).decode()
