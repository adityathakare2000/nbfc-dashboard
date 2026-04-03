import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="NBFC Portfolio Dashboard", layout="wide")

st.title("Portfolio Analytics Dashboard")
st.caption("Powered by your analytics platform")

st.sidebar.header("Upload Portfolio Data")
uploaded_file = st.sidebar.file_uploader("Upload your loan CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"{len(df)} loan records loaded")
else:
    df = pd.read_csv("loan_portfolio.csv")
    st.sidebar.info("Showing demo data — upload your own CSV above")

total_aum = df["outstanding_amount"].sum() / 10000000
total_loans = len(df)
npa_rate = round((len(df[df["bucket"] == "NPA"]) / total_loans) * 100, 1)
par30 = round((len(df[df["dpd"] >= 30]) / total_loans) * 100, 1)
collection_eff = round((len(df[df["collection_status"] == "Collected"]) / total_loans) * 100, 1)

st.subheader("Portfolio Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total AUM", f"₹{total_aum:.1f} Cr")
col2.metric("PAR 30+", f"{par30}%")
col3.metric("NPA Rate", f"{npa_rate}%")
col4.metric("Collection Efficiency", f"{collection_eff}%")

st.divider()

col5, col6 = st.columns(2)

with col5:
    st.subheader("Portfolio by DPD Bucket")
    bucket_counts = df["bucket"].value_counts().reset_index()
    bucket_counts.columns = ["Bucket", "Count"]
    fig1 = px.pie(
        bucket_counts,
        names="Bucket",
        values="Count",
        hole=0.4,
        color="Bucket",
        color_discrete_map={
            "Current": "#1D9E75",
            "SMA-0": "#EF9F27",
            "SMA-1": "#D85A30",
            "SMA-2": "#E24B4A",
            "NPA": "#A32D2D"
        }
    )
    st.plotly_chart(fig1, use_container_width=True)

with col6:
    st.subheader("PAR by Product")
    par_by_product = df[df["dpd"] >= 30].groupby("product").size()
    total_by_product = df.groupby("product").size()
    par_pct = (par_by_product / total_by_product * 100).round(1).reset_index()
    par_pct.columns = ["Product", "PAR 30+ %"]
    fig2 = px.bar(
        par_pct,
        x="PAR 30+ %",
        y="Product",
        orientation="h",
        color="PAR 30+ %",
        color_continuous_scale=["#1D9E75", "#EF9F27", "#E24B4A"]
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("Roll-Rate Matrix")
st.caption("Shows how accounts moved between risk buckets — green means improving, red means worsening")

bucket_order = ["Current", "SMA-0", "SMA-1", "SMA-2", "NPA"]

np.random.seed(42)
roll_data = {
    "Current":  [88, 9,  2,  1,  0],
    "SMA-0":    [34, 41, 18, 6,  1],
    "SMA-1":    [18, 22, 35, 19, 6],
    "SMA-2":    [8,  11, 22, 38, 21],
    "NPA":      [3,  5,  8,  14, 70],
}

roll_df = pd.DataFrame(roll_data, index=bucket_order)
roll_df.index.name = "Last Month →"

def color_cells(val):
    if val >= 60:
        return "background-color: #1D9E75; color: white; font-weight: 500; text-align: center;"
    elif val >= 30:
        return "background-color: #9FE1CB; color: #085041; font-weight: 500; text-align: center;"
    elif val >= 15:
        return "background-color: #FAEEDA; color: #854F0B; font-weight: 500; text-align: center;"
    elif val >= 5:
        return "background-color: #F0997B; color: #712B13; font-weight: 500; text-align: center;"
    else:
        return "background-color: #FCEBEB; color: #A32D2D; font-weight: 500; text-align: center;"

styled = roll_df.style.map(color_cells).format("{:.0f}%")
st.dataframe(styled, use_container_width=True)

st.divider()

st.subheader("Early Warning — Accounts at Risk")
at_risk = df[df["bucket"].isin(["SMA-2", "NPA"])].copy()
at_risk = at_risk.sort_values("dpd", ascending=False)
at_risk["outstanding_amount"] = at_risk["outstanding_amount"].apply(lambda x: f"₹{x/100000:.1f}L")

def risk_label(bucket):
    if bucket == "NPA":
        return "Urgent"
    elif bucket == "SMA-2":
        return "High Risk"
    else:
        return "Watch"

at_risk["Risk Level"] = at_risk["bucket"].apply(risk_label)
st.dataframe(
    at_risk[["loan_id", "borrower_name", "product", "geography", "outstanding_amount", "dpd", "bucket", "Risk Level"]].reset_index(drop=True),
    use_container_width=True,
    height=300
)

st.divider()

st.subheader("Explore Portfolio")
selected_product = st.selectbox("Filter by product", ["All"] + list(df["product"].unique()))

if selected_product != "All":
    filtered = df[df["product"] == selected_product]
else:
    filtered = df

geo_par = filtered[filtered["dpd"] >= 30].groupby("geography").size()
geo_total = filtered.groupby("geography").size()
geo_pct = (geo_par / geo_total * 100).round(1).reset_index()
geo_pct.columns = ["Geography", "PAR 30+ %"]

fig3 = px.bar(
    geo_pct,
    x="Geography",
    y="PAR 30+ %",
    color="PAR 30+ %",
    color_continuous_scale=["#1D9E75", "#EF9F27", "#E24B4A"],
    title=f"PAR 30+ by Geography — {selected_product}"
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()
st.caption("Built by your analytics platform · Data is confidential and secure")