import pandas as pd
from src.config import COLUMNS


def analyze_outliers(df: pd.DataFrame) -> dict:
    q1 = df[COLUMNS["delivery_time"]].quantile(0.25)
    q3 = df[COLUMNS["delivery_time"]].quantile(0.75)
    iqr = q3 - q1

    normal = df[
        (df[COLUMNS["delivery_time"]] >= q1 - 1.5 * iqr)
        & (df[COLUMNS["delivery_time"]] <= q3 + 1.5 * iqr)
    ]

    outlier = df.drop(normal.index)

    return {
        "normal_mean": round(normal[COLUMNS["delivery_time"]].mean(), 2),
        "outlier_mean": round(outlier[COLUMNS["delivery_time"]].mean(), 2),
    }
