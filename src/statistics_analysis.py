import pandas as pd
from src.config import COLUMNS


def compute_statistics(df: pd.DataFrame) -> dict:
    return {
        "mean_order_value": round(df[COLUMNS["price"]].mean(), 2),
        "median_order_value": round(df[COLUMNS["price"]].median(), 2),
        "std_delivery_time": round(df[COLUMNS["delivery_time"]].std(), 2),
        "late_probability": round(df[COLUMNS["is_late"]].mean(), 2),
    }


