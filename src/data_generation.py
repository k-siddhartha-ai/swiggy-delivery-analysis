import pandas as pd
import numpy as np
import os
from src.config import DATA_PATH, COLUMNS, RANDOM_SEED, LATE_THRESHOLD_MIN


def ensure_dataset() -> pd.DataFrame:
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)

    np.random.seed(RANDOM_SEED)
    n = 200

    df = pd.DataFrame({
        COLUMNS["city"]: np.random.choice(
            ["Hyderabad", "Bangalore", "Mumbai", "Chennai"], n
        ),
        COLUMNS["cuisine"]: np.random.choice(
            ["Indian", "Chinese", "Italian", "Fast Food"], n
        ),
        COLUMNS["price"]: np.random.randint(150, 700, n),
        COLUMNS["rating"]: np.round(np.random.uniform(2.5, 5.0, n), 1),
        COLUMNS["prep_time"]: np.random.randint(10, 35, n),
        COLUMNS["distance"]: np.round(np.random.uniform(1, 10, n), 1),
    })

    df[COLUMNS["delivery_time"]] = (
        df[COLUMNS["prep_time"]] + df[COLUMNS["distance"]] * 4
    )

    df[COLUMNS["is_late"]] = (
        df[COLUMNS["delivery_time"]] > LATE_THRESHOLD_MIN
    ).astype(int)

    os.makedirs("data", exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

    return df



