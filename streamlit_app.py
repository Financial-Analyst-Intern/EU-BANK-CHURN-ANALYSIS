"""
Customer Segmentation & Churn Analytics - European Banking
Streamlit dashboard | Run:  streamlit run streamlit_app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="EU Bank Churn Analytics", layout="wide")
st.title("\U0001F3E6 Customer Segmentation & Churn Analytics — European Banking")

@st.cache_data
def load_data():
    df = pd.read_csv("european_bank_processed.csv")
    return df

df = load_data()
TOTAL, CHURNED = len(df), int(df["Exited"].sum())
OVERALL = CHURNED / TOTAL


st.sidebar.header("Segment Filters")
geo = st.sidebar.multiselect("Geography", df["Geography"].unique(), default=list(df["Geography"].unique()))
gender = st.sidebar.multiselect("Gender", df["Gender"].unique(), default=list(df["Gender"].unique()))
age = st.sidebar.slider("Age", int(df.Age.min()), int(df.Age.max()), (int(df.Age.min()), int(df.Age.max())))
bal = st.sidebar.slider("Balance (€)", 0, int(df.Balance.max()), (0, int(df.Balance.max())))
act = st.sidebar.radio("Activity", ["All", "Active only", "Inactive only"])

f = df[df.Geography.isin(geo) & df.Gender.isin(gender) & df.Age.between(*age) & df.Balance.between(*bal)]
if act == "Active only":      f = f[f.IsActiveMember == 1]
elif act == "Inactive only":  f = f[f.IsActiveMember == 0]


c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Customers (filtered)", f"{len(f):,}")
c2.metric("Churn Rate", f"{f.Exited.mean():.1%}", delta=f"{f.Exited.mean()-OVERALL:+.1%} vs overall")
c3.metric("Churned Customers", f"{int(f.Exited.sum()):,}")
c4.metric("Balance Lost (churned)", f"€{f.loc[f.Exited==1,'Balance'].sum():,.0f}")
c5.metric("Overall Churn Rate", f"{OVERALL:.1%}")

tab1, tab2, tab3, tab4 = st.tabs(["Overall Summary", "Geography", "Age & Tenure", "High-Value Explorer"])

def churn_bar(f, col, title, color="#d62728"):
    g = f.groupby(col, observed=True)["Exited"].agg(["count", "mean"]).reset_index()
    g["churn_%"] = g["mean"] * 100
    fig = px.bar(g, x=col, y="churn_%", color_discrete_sequence=[color],
                 labels={"churn_%": "Churn %", col: col},
                 hover_data={"count": True, "churn_%": ":.1f"}, title=title)
    fig.add_hline(y=OVERALL*100, line_dash="dash", annotation_text="overall")
    return fig

with tab1:
    st.subheader("Churn by Number of Products & Activity")
    col1, col2 = st.columns(2)
    col1.plotly_chart(churn_bar(f, "NumOfProducts", "Churn % by Number of Products"), use_container_width=True)
    col2.plotly_chart(churn_bar(f, "IsActiveMember", "Churn % by Activity Status"), use_container_width=True)
    st.plotly_chart(churn_bar(f, "CreditBand", "Churn % by Credit Score Band"), use_container_width=True)

with tab2:
    st.subheader("Geography-wise Churn")
    st.plotly_chart(churn_bar(f, "Geography", "Churn % by Geography"), use_container_width=True)
    piv = pd.crosstab(f["AgeGroup"], f["Geography"], f["Exited"], aggfunc="mean") * 100
    fig = px.imshow(piv, text_auto=".1f", color_continuous_scale="Reds", title="Churn % — Age Group × Geography")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Age & Tenure Comparison")
    col1, col2 = st.columns(2)
    col1.plotly_chart(churn_bar(f, "AgeGroup", "Churn % by Age Group"), use_container_width=True)
    col2.plotly_chart(churn_bar(f, "TenureGroup", "Churn % by Tenure Group"), use_container_width=True)

with tab4:
    st.subheader("High-Value Customer Churn Explorer")
    f2 = f.copy()
    f2["ValueTier"] = np.where((f2.Balance >= 100000) | (f2.EstimatedSalary >= 100000), "High-Value", "Standard")
    st.plotly_chart(churn_bar(f2, "ValueTier", "Churn % by Value Tier", "#9467bd"), use_container_width=True)
    hv = f2[(f2.ValueTier == "High-Value") & (f2.Exited == 1)]
    st.write(f"**{len(hv):,} high-value customers churned**, taking **€{hv.Balance.sum():,.0f}** in balances with them.")
    st.dataframe(hv[["CustomerId","Geography","Gender","Age","Balance","EstimatedSalary","NumOfProducts","IsActiveMember"]])
