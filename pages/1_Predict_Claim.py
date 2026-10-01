import io

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.model_utils import REGION, SEX, SMOKER, predict_df, predict_one
from utils.theme import BLUES, hero, setup_page, style_fig
from utils.training import FEATURES

setup_page("Predict Claim", "🔮")
hero("Predict an Insurance Claim", "Fill in the policyholder details to estimate the probability of a claim.")

tab1, tab2 = st.tabs(["Single prediction", "Batch prediction (CSV)"])

with tab1:
    left, right = st.columns([1, 1], gap="large")
    with left:
        with st.form("predict_form"):
            c1, c2 = st.columns(2)
            age = c1.slider("Age", 18, 100, 35)
            bmi = c2.number_input("BMI", 10.0, 60.0, 28.0, step=0.1)
            sex = c1.selectbox("Sex", list(SEX.keys()), format_func=SEX.get)
            smoker = c2.selectbox("Smoker", list(SMOKER.keys()), format_func=SMOKER.get)
            children = c1.number_input("Children", 0, 10, 1)
            region = c2.selectbox("Region", list(REGION.keys()), format_func=REGION.get)
            charges = st.number_input("Medical charges ($)", 0.0, 200000.0, 13000.0, step=500.0)
            submitted = st.form_submit_button("Predict claim", use_container_width=True)

    with right:
        if submitted:
            pred, prob = predict_one(age, sex, bmi, children, smoker, region, charges)
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=prob * 100, number={"suffix": "%", "font": {"color": "#0A1F44"}},
                title={"text": "Claim probability"},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": BLUES[0]},
                       "steps": [{"range": [0, 33], "color": BLUES[5]},
                                 {"range": [33, 66], "color": BLUES[4]},
                                 {"range": [66, 100], "color": BLUES[3]}]}))
            st.plotly_chart(style_fig(fig, 300), use_container_width=True)
            if pred == 1:
                st.markdown(f"<div class='result-yes'><h2>Claim likely</h2>"
                            f"<p>The model estimates a {prob * 100:.1f}% chance this customer will claim.</p></div>",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='result-no'><h2>Claim unlikely</h2>"
                            f"<p>The model estimates only a {prob * 100:.1f}% chance this customer will claim.</p></div>",
                            unsafe_allow_html=True)
        else:
            st.info("Submit the form to see the prediction here.")

with tab2:
    st.write("Upload a CSV with these columns (numeric codes, same as the training data): "
             + ", ".join(f"`{c}`" for c in FEATURES))
    st.caption("sex: 0 = Female, 1 = Male | smoker: 0 = No, 1 = Yes | region: 0 = Northeast, "
               "1 = Northwest, 2 = Southeast, 3 = Southwest")
    template = pd.DataFrame([[35, 1, 28.0, 1, 0, 2, 13000.0]], columns=FEATURES)
    st.download_button("Download template CSV", template.to_csv(index=False), "template.csv", "text/csv")
    up = st.file_uploader("Upload CSV", type="csv")
    if up is not None:
        data = pd.read_csv(up)
        missing = [c for c in FEATURES if c not in data.columns]
        if missing:
            st.error(f"Missing columns: {missing}")
        else:
            pred, prob = predict_df(data)
            out = data.copy()
            out["claim_probability"] = (prob * 100).round(1)
            out["prediction"] = ["Claim" if p == 1 else "No claim" for p in pred]
            st.dataframe(out, use_container_width=True)
            st.download_button("Download results", out.to_csv(index=False), "predictions.csv", "text/csv")
