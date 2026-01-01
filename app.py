import gradio as gr
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from scipy.stats import linregress

from src.data_generation import ensure_dataset

sns.set_style("whitegrid")


def run_analysis():
    df = ensure_dataset()

    # ---------- TEXT + TABLES ----------
    title_md = f"### 📊 Swiggy Delivery Analysis ({len(df)} Orders)"
    sample_df = df.head(10)

    stats_md = "### 📈 Key Statistics"
    stats_df = (
        df[
            [
                "Avg_Meal_Price_INR",
                "Customer_Rating",
                "Total_Delivery_Time_Min",
                "Rider_Distance_KM",
            ]
        ]
        .agg(["mean", "median", "std"])
        .round(2)
    )

    late_prob = df["Is_Late"].mean()
    late_md = f"### ⏱️ Late Delivery Probability: **{late_prob:.1%}**"

    city_late_df = (
        df.groupby("City")["Is_Late"]
        .mean()
        .reset_index()
        .rename(columns={"Is_Late": "Late Probability"})
    )

    corr = linregress(
        df["Total_Delivery_Time_Min"], df["Customer_Rating"]
    ).rvalue
    corr_md = f"### 🔗 Correlation (Delivery Time vs Rating): **{corr:.2f}**"

    # ---------- PLOTS ----------
    fig1, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df["Total_Delivery_Time_Min"], kde=True, ax=ax)
    ax.set_title("Delivery Time Distribution")

    fig2 = px.bar(
        city_late_df,
        x="City",
        y="Late Probability",
        title="Late Delivery Probability by City",
    )

    fig3 = px.scatter(
        df,
        x="Total_Delivery_Time_Min",
        y="Customer_Rating",
        color="City",
        title="Delivery Time vs Rating",
    )

    extra_md = "### 🔍 Additional Insights"

    fig4 = px.box(
        df,
        x="City",
        y="Avg_Meal_Price_INR",
        title="Meal Price Distribution by City",
    )

    fig5 = px.pie(
        df["Cuisine"].value_counts().reset_index(),
        names="Cuisine",
        values="count",
        title="Cuisine Popularity",
    )

    fig6 = px.scatter(
        df,
        x="Rider_Distance_KM",
        y="Total_Delivery_Time_Min",
        color="Is_Late",
        size="Avg_Meal_Price_INR",
        title="Distance vs Delivery Time",
    )

    # ✅ EXACTLY 14 outputs — types match Gradio components
    return (
        title_md,
        sample_df,
        stats_md,
        stats_df,
        late_md,
        city_late_df,
        corr_md,
        fig1,
        fig2,
        fig3,
        extra_md,
        fig4,
        fig5,
        fig6,
    )


# ---------- UI ----------
with gr.Blocks(title="Swiggy Delivery Analysis") as demo:
    gr.Markdown("# 🍛 Swiggy Delivery Analysis Dashboard")
    gr.Markdown("Industry-grade EDA & insights on food delivery performance")

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

    run_btn.click(run_analysis, outputs=outputs)

demo.launch()






