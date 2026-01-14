import pandas as pd

def advanced_statistics(df: pd.DataFrame) -> str:
    """
    Computes advanced statistical insights from the Swiggy dataset.
    Returns a formatted markdown string.
    """

    if df.empty:
        return "❌ No data available for statistics."

    # Correlation
    corr = df['distance'].corr(df['time_taken'])

    # Percentiles
    p90 = df['time_taken'].quantile(0.90)
    p95 = df['time_taken'].quantile(0.95)

    # Late delivery share
    late_rate = df['Is_Late'].mean() * 100

    result = (
        f"### 📊 Advanced Statistics\n"
        f"- **Distance ↔ Time Correlation:** `{corr:.2f}`\n"
        f"- **90th Percentile Delivery Time:** `{p90:.1f} min`\n"
        f"- **95th Percentile Delivery Time:** `{p95:.1f} min`\n"
        f"- **Late Delivery Rate (>45 min):** `{late_rate:.2f}%`"
    )

    return result
