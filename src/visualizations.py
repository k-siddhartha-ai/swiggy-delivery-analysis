import matplotlib.pyplot as plt
import seaborn as sns
from src.config import COLUMNS

sns.set_style("whitegrid")


def delivery_time_distribution(df):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df[COLUMNS["delivery_time"]], kde=True, ax=ax)
    ax.set_title("Delivery Time Distribution")
    return fig


def late_probability_by_city(df):
    city_late = df.groupby(COLUMNS["city"])[COLUMNS["is_late"]].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=city_late, x=COLUMNS["city"], y=COLUMNS["is_late"], ax=ax)
    ax.set_title("Late Delivery Probability by City")
    return fig




