from src.data_generation import ensure_dataset
from src.statistics_analysis import compute_statistics
from src.outlier_analysis import analyze_outliers
from src.visualizations import (
    delivery_time_distribution,
    late_probability_by_city,
)


def main():
    print("SWIGGY DATA ANALYSIS PIPELINE")

    df = ensure_dataset()
    stats = compute_statistics(df)
    outliers = analyze_outliers(df)

    print("\nSTATISTICS")
    for k, v in stats.items():
        print(f"{k}: {v}")

    print("\nOUTLIER ANALYSIS")
    for k, v in outliers.items():
        print(f"{k}: {v}")

    print("\nPIPELINE COMPLETED SUCCESSFULLY 🎉")


if __name__ == "__main__":
    main()





