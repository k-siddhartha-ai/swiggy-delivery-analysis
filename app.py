import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gradio as gr
import plotly.express as px
from scipy.stats import linregress

# ----------------------------
# Global styling
# ----------------------------
sns.set_style("whitegrid")

# ----------------------------
# Paths (HF + PyCharm safe)
# ----------------------------
RAW_XLSX_PATH = "swiggy.xlsx"
CLEANED_XLSX_PATH = "cleaned_swiggy_data.xlsx"

# ----------------------------
# Data Loading & Cleaning
# ----------------------------
def load_and_clean_data(force_reload: bool = False) -> pd.DataFrame:
    """
    Loads Swiggy data from Excel.
    Uses cached cleaned Excel if available (faster).
    """

    # Use cached cleaned data if available
    if os.path.exists(CLEANED_XLSX_PATH) and not force_reload:
        return pd.read_excel(CLEANED_XLSX_PATH)

    if not os.path.exists(RAW_XLSX_PATH):
        raise FileNotFoundError(
            f"Required file '{RAW_XLSX_PATH}' not found in project root."
        )

    # Load raw data
    df = pd.read_excel(RAW_XLSX_PATH)

    # Drop junk columns safely
    drop_cols = ["Unnamed: 0", "rider_id"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # Numeric columns → median
    numeric_cols = [
        "age",
        "ratings",
        "multiple_deliveries",
        "pickup_time_minutes",
        "order_time_hour",
        "distance",
        "time_taken",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    # Categorical columns → "Unknown"
    cat_cols = [
        "weather",
        "traffic",
        "festival",
        "city_type",
        "order_time_of_day",
        "type_of_order",
        "city_name",
    ]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # Feature engineering
    df["Is_Late"] = (df["time_taken"] > 45).astype(int)

    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    if "multiple_deliveries" in df.columns:
        df["multiple_deliveries"] = df["multiple_deliveries"].astype(int)

    # Save cleaned cache
    df.to_excel(CLEANED_XLSX_PATH, index=False)

    return df


# Load data once (Gradio-safe)
df = load_and_clean_data()


# ----------------------------
# Analysis Function
# ----------------------------
def analyze_swiggy():
    outputs = []

    # Header
    outputs.append(
        gr.Markdown(
            f"### 📊 Swiggy Delivery Analysis ({len(df):,} Orders)"
        )
    )
    outputs.append(gr.Dataframe(df.head(10)))

    # Stats
    outputs.append(gr.Markdown("### 📈 Key Statistics"))
    stats_cols = ["time_taken", "distance", "ratings", "age", "multiple_deliveries"]
    stats_df = df[stats_cols].agg(["mean", "median", "std"]).round(2)
    outputs.append(gr.Dataframe(stats_df))

    # Late delivery
    late_rate = df["Is_Late"].mean()
    city_late = (
        df.groupby("city_name", as_index=False)["Is_Late"]
        .mean()
        .sort_values("Is_Late", ascending=False)
        .head(10)
    )

    outputs.append(
        gr.Markdown(f"**⏱️ Late Delivery Rate: {late_rate:.1%}**")
    )
    outputs.append(city_late.rename(columns={"Is_Late": "Late Probability"}))

    # Correlation
    r = linregress(df["distance"], df["time_taken"]).rvalue
    outputs.append(
        gr.Markdown(f"**📐 Distance vs Time Correlation (R = {r:.2f})**")
    )

    # ----------------------------
    # Plots
    # ----------------------------

    # Histogram
    fig1, ax = plt.subplots(figsize=(9, 5))
    sns.histplot(df["time_taken"], bins=30, kde=True, ax=ax)
    ax.axvline(45, color="red", linestyle="--", label="Late Threshold (45 min)")
    ax.set_title("Delivery Time Distribution")
    ax.legend()
    outputs.append(gr.Plot(fig1))

    # Bar chart
    fig2 = px.bar(
        city_late,
        x="city_name",
        y="Is_Late",
        title="Top 10 Cities by Late Delivery Probability",
        labels={"Is_Late": "Late Probability", "city_name": "City"},
    )
    outputs.append(gr.Plot(fig2))

    # Scatter (HF marker fix)
    fig3 = px.scatter(
        df.sample(min(5000, len(df))),
        x="distance",
        y="time_taken",
        color="traffic",
        size="multiple_deliveries",
        hover_data=["weather", "city_name"],
        title="Delivery Time vs Distance",
    )
    fig3.update_traces(marker=dict(size=7, opacity=0.7))
    fig3.add_hline(y=45, line_dash="dash", line_color="red")
    outputs.append(gr.Plot(fig3))

    outputs.append(gr.Markdown("### 📌 Additional Insights"))

    # Box plot
    fig4 = px.box(
        df,
        x="weather",
        y="time_taken",
        title="Delivery Time by Weather",
    )
    outputs.append(gr.Plot(fig4))

    # ✅ FIXED PIE CHART (NO ERROR)
    order_counts = df["type_of_order"].value_counts().reset_index()
    order_counts.columns = ["type_of_order", "count"]

    fig5 = px.pie(
        order_counts,
        names="type_of_order",
        values="count",
        title="Order Type Distribution",
    )
    outputs.append(gr.Plot(fig5))

    # Violin
    fig6 = px.violin(
        df,
        x="multiple_deliveries",
        y="time_taken",
        color="festival",
        box=True,
        title="Multiple Deliveries vs Time",
    )
    outputs.append(gr.Plot(fig6))

    return outputs


# ----------------------------
# Gradio UI
# ----------------------------
with gr.Blocks(
    title="Swiggy Delivery Performance Dashboard",
    theme=gr.themes.Soft(),
) as demo:

    gr.Markdown("# 🍛 Swiggy Delivery Performance Dashboard")
    gr.Markdown("Same output as your original Hugging Face app")

    run_btn = gr.Button("🚀 Run Full Analysis", variant="primary")

    outputs = [
        gr.Markdown(),
        gr.Dataframe(),
        gr.Markdown(),
        gr.Dataframe(),
        gr.Markdown(),
        gr.Dataframe(),
        gr.Markdown(),
        gr.Plot(),
        gr.Plot(),
        gr.Plot(),
        gr.Markdown(),
        gr.Plot(),
        gr.Plot(),
        gr.Plot(),
    ]

    run_btn.click(analyze_swiggy, outputs=outputs)

demo.launch()
