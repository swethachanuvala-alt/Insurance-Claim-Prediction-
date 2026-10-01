"""Training pipeline - identical to the notebook (GGST_5.ipynb). No Streamlit imports."""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "Insurance.csv"
MODEL_PATH = ROOT / "models" / "xg_boost_model.pkl"
SCALER_PATH = ROOT / "models" / "scaler.pkl"

FEATURES = ["age", "sex", "bmi", "children", "smoker", "region", "charges"]
TARGET = "insuranceclaim"

# Best parameters found by RandomizedSearchCV in the notebook
BEST_PARAMS = dict(subsample=1.0, n_estimators=300, max_depth=7,
                   learning_rate=0.01, colsample_bytree=1.0)


def get_split(df):
    X, y = df[FEATURES], df[TARGET]
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


def train_and_save(save=True):
    from imblearn.over_sampling import SMOTE
    from xgboost import XGBClassifier

    df = pd.read_csv(DATA_PATH)
    X_train, X_test, y_train, y_test = get_split(df)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    X_res, y_res = SMOTE(random_state=42).fit_resample(X_train_scaled, y_train)

    model = XGBClassifier(random_state=42, eval_metric="logloss", **BEST_PARAMS)
    model.fit(X_res, y_res)

    if save:
        try:
            MODEL_PATH.parent.mkdir(exist_ok=True)
            joblib.dump(model, MODEL_PATH)
            joblib.dump(scaler, SCALER_PATH)
        except OSError:
            pass  # read-only file system - fine, keep in memory
    return model, scaler


if __name__ == "__main__":
    train_and_save()
    print("Saved:", MODEL_PATH, "and", SCALER_PATH)
