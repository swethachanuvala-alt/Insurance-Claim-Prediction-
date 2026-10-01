import pandas as pd
import streamlit as st

from utils.theme import card, hero, setup_page

setup_page("About", "ℹ️")
hero("About this project", "From raw CSV to a deployed prediction app.")

a, b = st.columns(2)
with a:
    card("1. Data", "1,338 policyholders, 7 input features, target = insuranceclaim (1 = claimed). No missing values.")
    card("2. Preprocessing", "Stratified 80/20 train-test split, StandardScaler, and SMOTE on the training set "
                             "to balance the claim / no-claim classes.")
with b:
    card("3. Modelling", "Six algorithms compared; Decision Tree, Random Forest and XGBoost tuned with "
                         "randomized / grid search and 5-fold cross validation.")
    card("4. Final model", "XGBoost (300 trees, depth 7, learning rate 0.01) saved with joblib together with its scaler.")

st.markdown("### Feature dictionary")
st.dataframe(pd.DataFrame([
    ["age", "Age of the policyholder"],
    ["sex", "0 = Female, 1 = Male"],
    ["bmi", "Body mass index"],
    ["children", "Number of dependants covered"],
    ["smoker", "0 = No, 1 = Yes"],
    ["region", "0 = Northeast, 1 = Northwest, 2 = Southeast, 3 = Southwest"],
    ["charges", "Medical charges billed"],
], columns=["Feature", "Meaning"]), use_container_width=True, hide_index=True)

st.warning("This app is a learning / portfolio project. Predictions are statistical estimates and "
           "must not be used for real underwriting or claim decisions.")
