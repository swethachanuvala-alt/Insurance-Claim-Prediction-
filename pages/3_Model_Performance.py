import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.model_utils import evaluate
from utils.theme import BLUES, hero, kpi, setup_page, style_fig

setup_page("Model Performance", "🏆")
hero("Model Performance", "How the final XGBoost model performs on the held-out 20% test set.")

res = evaluate()
cols = st.columns(5)
for c, (k, v) in zip(cols, res["metrics"].items()):
    kpi(c, k, f"{v * 100:.1f}%" if k != "ROC-AUC" else f"{v:.3f}")
st.write("")

a, b = st.columns(2)
with a:
    cm = res["cm"]
    fig = px.imshow(cm, text_auto=True, color_continuous_scale="Blues",
                    x=["No claim", "Claim"], y=["No claim", "Claim"],
                    labels=dict(x="Predicted", y="Actual"), title=f"Confusion matrix ({res['n_test']} test rows)")
    st.plotly_chart(style_fig(fig), use_container_width=True)
with b:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=res["fpr"], y=res["tpr"], mode="lines", name="XGBoost",
                             line=dict(color=BLUES[2], width=3), fill="tozeroy",
                             fillcolor="rgba(124,196,245,0.35)"))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Random",
                             line=dict(color=BLUES[0], dash="dash")))
    fig.update_layout(title="ROC curve", xaxis_title="False positive rate", yaxis_title="True positive rate")
    st.plotly_chart(style_fig(fig), use_container_width=True)

imp = pd.Series(res["importance"]).sort_values()
fig = px.bar(imp, orientation="h", title="Feature importance (XGBoost)", color=imp.values,
             color_continuous_scale="Blues", labels={"value": "Importance", "index": "Feature"})
fig.update_layout(showlegend=False, coloraxis_showscale=False)
st.plotly_chart(style_fig(fig, 360), use_container_width=True)

st.markdown("### Model comparison (from the notebook)")
comp = pd.DataFrame([
    ["XGBoost", .9739, .9808, .9745, .9776, .9941],
    ["Decision Tree", .9515, .9444, .9745, .9592, .9467],
    ["Random Forest", .9291, .9539, .9236, .9385, .9869],
    ["SVM", .8918, .9571, .8535, .9024, .9379],
    ["KNN", .8843, .9257, .8726, .8984, .9532],
    ["Logistic Regression", .8470, .8919, .8408, .8656, .9037],
], columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"])
st.dataframe(comp.style.format({c: "{:.3f}" for c in comp.columns[1:]}).background_gradient(
    cmap="Blues", subset=comp.columns[1:]), use_container_width=True, hide_index=True)

st.markdown("### After hyper-parameter tuning + 5-fold cross validation")
tuned = pd.DataFrame([
    ["XGBoost", .9701, .9956, .9828],
    ["Decision Tree", .9515, .9467, .9776],
    ["Random Forest", .9478, .9895, .9529],
], columns=["Model", "Test accuracy", "ROC-AUC", "CV accuracy"])
st.dataframe(tuned.style.format({c: "{:.3f}" for c in tuned.columns[1:]}),
             use_container_width=True, hide_index=True)
st.caption("XGBoost had the best cross-validation accuracy, so it was saved as the final model.")
