import plotly.express as px
import streamlit as st

from utils.model_utils import REGION, SEX, SMOKER, load_data
from utils.theme import BLUES, hero, kpi, setup_page, style_fig

setup_page("Data Explorer", "📊")
hero("Data Explorer", "Slice and visualise the insurance dataset used to train the model.")

df = load_data().copy()
df["Sex"] = df["sex"].map(SEX)
df["Smoker"] = df["smoker"].map(SMOKER)
df["Region"] = df["region"].map(REGION)
df["Claim"] = df["insuranceclaim"].map({0: "No claim", 1: "Claim"})

with st.expander("Filters", expanded=True):
    f1, f2, f3 = st.columns(3)
    ages = f1.slider("Age range", int(df.age.min()), int(df.age.max()), (int(df.age.min()), int(df.age.max())))
    smk = f2.multiselect("Smoker", ["No", "Yes"], default=["No", "Yes"])
    reg = f3.multiselect("Region", sorted(REGION.values()), default=sorted(REGION.values()))

d = df[df.age.between(*ages) & df.Smoker.isin(smk) & df.Region.isin(reg)]
if d.empty:
    st.warning("No rows match these filters.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
kpi(c1, "Rows", f"{len(d):,}")
kpi(c2, "Claim rate", f"{d.insuranceclaim.mean() * 100:.1f}%")
kpi(c3, "Avg. BMI", f"{d.bmi.mean():.1f}")
kpi(c4, "Avg. charges", f"${d.charges.mean():,.0f}")
st.write("")

cmap = {"Claim": BLUES[2], "No claim": BLUES[4]}
t1, t2, t3, t4 = st.tabs(["Distributions", "Relationships", "Correlation", "Raw data"])

with t1:
    col = st.selectbox("Feature", ["age", "bmi", "charges", "children"])
    fig = px.histogram(d, x=col, color="Claim", barmode="overlay", nbins=30, opacity=0.8,
                       color_discrete_map=cmap, title=f"Distribution of {col} by claim status")
    st.plotly_chart(style_fig(fig), use_container_width=True)
    a, b = st.columns(2)
    g = d.groupby("Smoker").insuranceclaim.mean().mul(100).reset_index()
    a.plotly_chart(style_fig(px.bar(g, x="Smoker", y="insuranceclaim", color="Smoker",
                   color_discrete_sequence=BLUES[1:4], title="Claim rate by smoker (%)")), use_container_width=True)
    g = d.groupby("Region").insuranceclaim.mean().mul(100).reset_index()
    b.plotly_chart(style_fig(px.bar(g, x="Region", y="insuranceclaim", color="Region",
                   color_discrete_sequence=BLUES[1:5], title="Claim rate by region (%)")), use_container_width=True)

with t2:
    fig = px.scatter(d, x="age", y="charges", color="Claim", size="bmi", opacity=0.7,
                     color_discrete_map=cmap, title="Age vs charges (bubble size = BMI)")
    st.plotly_chart(style_fig(fig, 460), use_container_width=True)

with t3:
    corr = d[["age", "sex", "bmi", "children", "smoker", "region", "charges", "insuranceclaim"]].corr().round(2)
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="Blues", title="Correlation matrix")
    st.plotly_chart(style_fig(fig, 520), use_container_width=True)

with t4:
    st.dataframe(d.drop(columns=["Sex", "Smoker", "Region", "Claim"]), use_container_width=True)
    st.download_button("Download filtered data", d.to_csv(index=False), "filtered_insurance.csv", "text/csv")
