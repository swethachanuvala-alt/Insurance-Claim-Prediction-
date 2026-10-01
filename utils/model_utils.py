import joblib
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score, roc_curve)

from utils.training import (DATA_PATH, FEATURES, MODEL_PATH, SCALER_PATH, TARGET,
                            get_split, train_and_save)

SEX = {0: "Female", 1: "Male"}
SMOKER = {0: "No", 1: "Yes"}
REGION = {0: "Northeast", 1: "Northwest", 2: "Southeast", 3: "Southwest"}


@st.cache_data(show_spinner=False)
def load_data():
    return pd.read_csv(DATA_PATH)


@st.cache_resource(show_spinner="Loading model...")
def load_artifacts():
    """Load saved model + scaler; if missing/incompatible, train them from the CSV."""
    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        sample = load_data()[FEATURES].head(2)
        model.predict_proba(scaler.transform(sample))  # sanity check
        return model, scaler
    except Exception:
        return train_and_save(save=True)


def predict_df(df):
    model, scaler = load_artifacts()
    X = scaler.transform(df[FEATURES])
    return model.predict(X), model.predict_proba(X)[:, 1]


def predict_one(age, sex, bmi, children, smoker, region, charges):
    row = pd.DataFrame([[age, sex, bmi, children, smoker, region, charges]], columns=FEATURES)
    pred, prob = predict_df(row)
    return int(pred[0]), float(prob[0])


@st.cache_data(show_spinner="Evaluating model...")
def evaluate():
    model, scaler = load_artifacts()
    df = load_data()
    _, X_test, _, y_test = get_split(df)
    Xs = scaler.transform(X_test)
    pred = model.predict(Xs)
    prob = model.predict_proba(Xs)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, prob)
    return {
        "metrics": {
            "Accuracy": accuracy_score(y_test, pred),
            "Precision": precision_score(y_test, pred),
            "Recall": recall_score(y_test, pred),
            "F1 Score": f1_score(y_test, pred),
            "ROC-AUC": roc_auc_score(y_test, prob),
        },
        "cm": confusion_matrix(y_test, pred).tolist(),
        "fpr": np.asarray(fpr), "tpr": np.asarray(tpr),
        "importance": dict(zip(FEATURES, [float(v) for v in model.feature_importances_])),
        "n_test": int(len(y_test)),
    }
