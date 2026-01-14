import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def train_late_delivery_model(df: pd.DataFrame) -> str:
    """
    Trains a Logistic Regression model to predict late deliveries.
    Returns model accuracy as a formatted string.
    """

    required_cols = [
        'distance',
        'pickup_time_minutes',
        'multiple_deliveries',
        'Is_Late'
    ]

    if not all(col in df.columns for col in required_cols):
        return "❌ Required columns not found for ML training."

    X = df[['distance', 'pickup_time_minutes', 'multiple_deliveries']]
    y = df['Is_Late']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))

    return (
        f"### 🤖 ML Model Result\n"
        f"- **Late Delivery Prediction Accuracy:** `{accuracy:.2%}`\n"
        f"- **Model Used:** Logistic Regression"
    )
