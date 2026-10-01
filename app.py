import streamlit as st

from utils.model_utils import load_data
from utils.theme import card, hero, kpi, setup_page

setup_page("Home", "🛡️")
df = load_data()

hero("Insurance Claim Prediction",
     "A gradient-boosted model (XGBoost) that estimates whether a policyholder is likely to make an "
     "insurance claim, based on age, BMI, family size, smoking status, region and charges.")

c1, c2, c3, c4 = st.columns(4)
kpi(c1, "Policyholders", f"{len(df):,}")
kpi(c2, "Claim rate", f"{df['insuranceclaim'].mean() * 100:.1f}%")
kpi(c3, "Avg. charges", f"${df['charges'].mean():,.0f}")
kpi(c4, "Smokers", f"{df['smoker'].mean() * 100:.1f}%")

st.markdown("### Explore the app")
a, b = st.columns(2)
with a:
    card("🔮 Predict Claim", "Enter a customer's details and get an instant claim probability with a gauge.")
    st.page_link("pages/1_Predict_Claim.py", label="Open Predict Claim", icon="🔮")
    card("🏆 Model Performance", "Metrics, confusion matrix, ROC curve and the full model comparison.")
    st.page_link("pages/3_Model_Performance.py", label="Open Model Performance", icon="🏆")
with b:
    card("📊 Data Explorer", "Interactive charts and filters over the 1,338-row insurance dataset.")
    st.page_link("pages/2_Data_Explorer.py", label="Open Data Explorer", icon="📊")
    card("ℹ️ About", "How the model was built, what each feature means and the tech stack.")
    st.page_link("pages/4_About.py", label="Open About", icon="ℹ️")

st.markdown("### Tech stack")
st.markdown("".join(f"<span class='pill'>{t}</span>" for t in
                    ["Python", "Pandas", "Scikit-learn", "XGBoost", "SMOTE", "Plotly", "Streamlit"]),
            unsafe_allow_html=True)
