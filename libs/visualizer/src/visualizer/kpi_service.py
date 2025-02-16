import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from common_util.singleton import Singleton


class KpiService(metaclass=Singleton):
    def generate_market_cap_pie(self, tracker_symbols_daily):
        sns.set_theme(style="whitegrid")

        labels = [entry.get("symbol") for entry in tracker_symbols_daily]
        sizes = [entry.get("marketCap") for entry in tracker_symbols_daily]

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 14})
        ax.set_position([0, 0, 1, 1])

        # https://stackoverflow.com/a/38061400/13163112
        plot_file = io.BytesIO()
        plt.savefig(plot_file, format='png')
        plot_file.seek(0)

        return base64.b64encode(plot_file.read()).decode()

    def generate_buy_recommendations(self, tracker_symbols_daily):
        sns.set_theme(style="whitegrid")

        rating_map = {
            'strong_buy': 4,
            'buy': 3,
            'hold': 2,
            'sell': 1,
            'strong_sell': 0,
            'No Data': -1
        }
        df = pd.DataFrame(tracker_symbols_daily)
        df['rating'] = df['recommendationKey'].map(rating_map)

        plt.figure(figsize=(8, 5))
        sns.barplot(x='symbol', y='rating', data=df, palette='viridis')
        plt.ylabel("Rating (Higher is Better)")
        plt.ylim(-1.5, 4.5)

        plot_file = io.BytesIO()
        plt.savefig(plot_file, format='png', bbox_inches='tight')
        plot_file.seek(0)
        return base64.b64encode(plot_file.read()).decode()

    def generate_kpi_employee_count(self, tracker_symbols_daily):
        sns.set_theme(style="whitegrid")

        df = pd.DataFrame(tracker_symbols_daily)

        plt.figure(figsize=(8, 5))
        sns.barplot(x="symbol", y="fullTimeEmployees", data=df, palette="viridis")
        plt.xlabel("Stock", fontsize=12)
        plt.ylabel("Employees", fontsize=12)

        # Save the plot with no extra margins
        plot_file = io.BytesIO()
        plt.savefig(plot_file, format='png', bbox_inches='tight')
        plot_file.seek(0)
        return base64.b64encode(plot_file.read()).decode()
