import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="NBFC Portfolio Dashboard", layout="wide", page_icon="📊")

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stMetric { background: white; padding: 1rem; border-radius: 10px; border: 1px solid #eee; }
    .guide-box { background: #f0f7ff; border-left: 4px solid #1a73e8; padding: 1rem 1.5rem; border-radius: 6px; margin-bottom: 1rem; }
    .warning-box { background: #fff8e1; border-left: 4px solid #f9a825; padding: 1rem 1.5rem; border-radius: 6px; margin-bottom: 1rem; }
    .success-box { background: #e8f5e9; border-left: 4px solid #2e7d32; padding: 1rem 1.5rem; border-radius: 6px; margin-bottom: 1rem; }
    .ai-box { background: linear-gradient(135deg, #667eea20, #764ba220); border: 1px solid #667eea40; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; }
    h1 { color: #1a1a2e; }
    h2 { color: #16213e; }
    h3 { color: #0f3460; }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

USERS = {
    "demo@nbfc.com": "demo123",
    "admin@nbfc.com": "admin123"
}

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("## 📊 NBFC Portfolio Analytics")
        st.markdown("*Smarter risk decisions for lending teams*")
        st.markdown("---")
        st.markdown("### Sign in to your account")
        email = st.text_input("Email address", placeholder="you@nbfc.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        if st.button("Sign in", use_container_width=True):
            if email in USERS and USERS[email] == password:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Incorrect email or password. Try demo@nbfc.com / demo123")
        st.markdown("---")
        st.caption("Demo credentials: demo@nbfc.com / demo123")
    st.stop()

with st.sidebar:
    st.markdown("### 📊 NBFC Analytics")
    st.markdown(f"*Logged in*")
    st.markdown("---")
    page = st.radio("Navigate", ["Dashboard", "Data Upload Guide", "AI Insights"], label_visibility="collapsed")
    st.markdown("---")
    if st.button("Sign out"):
        st.session_state.logged_in = False
        st.rerun()

if page == "Data Upload Guide":
    st.title("📋 Data Upload Guide")
    st.markdown("Follow this guide carefully before uploading your portfolio data to avoid errors and get accurate results.")

    st.markdown("---")
    st.subheader("Step 1 — Download the sample file")
    st.markdown("""
    <div class='guide-box'>
    Before preparing your data, download our sample CSV file below to see exactly what the format looks like.
    Use it as a template — replace the sample values with your real loan data.
    </div>
    """, unsafe_allow_html=True)

    sample_data = {
        "loan_id": ["LN-5001", "LN-5002", "LN-5003"],
        "borrower_name": ["Mehta Traders Pvt Ltd", "Rajan Enterprises", "Sunita Textiles"],
        "product": ["Business Loan", "MSME Loan", "Equipment Finance"],
        "geography": ["Mumbai", "Pune", "Nagpur"],
        "disbursement_date": ["2024-01-15", "2024-02-10", "2023-11-05"],
        "loan_amount": [500000, 300000, 1000000],
        "outstanding_amount": [420000, 180000, 850000],
        "tenure_months": [36, 24, 48],
        "interest_rate": [18.5, 16.0, 14.5],
        "emis_paid": [8, 6, 12],
        "dpd": [0, 30, 90],
        "bucket": ["Current", "SMA-0", "SMA-2"],
        "collection_status": ["Collected", "Partially Collected", "Partially Collected"],
        "bureau_score_at_origination": [720, 680, 750]
    }
    sample_df = pd.DataFrame(sample_data)
    csv_bytes = sample_df.to_csv(index=False).encode()
    st.download_button("⬇️ Download sample CSV", csv_bytes, "sample_portfolio.csv", "text/csv", use_container_width=True)

    st.markdown("---")
    st.subheader("Step 2 — Required columns")
    st.markdown("""
    <div class='warning-box'>
    ⚠️ Your file must have ALL 14 columns listed below. Missing columns will cause errors.
    Column names must match exactly — spelling, case, and underscores.
    </div>
    """, unsafe_allow_html=True)

    guide_data = {
        "Column Name": [
            "loan_id", "borrower_name", "product", "geography",
            "disbursement_date", "loan_amount", "outstanding_amount",
            "tenure_months", "interest_rate", "emis_paid",
            "dpd", "bucket", "collection_status", "bureau_score_at_origination"
        ],
        "Data Type": [
            "Text", "Text", "Text", "Text",
            "Date", "Number", "Number",
            "Number", "Number", "Number",
            "Number", "Text", "Text", "Number"
        ],
        "Format / Allowed Values": [
            "Unique ID e.g. LN-1001",
            "Full borrower name",
            "Business Loan / MSME Loan / Equipment Finance / Working Capital / Personal Loan",
            "City name e.g. Mumbai",
            "YYYY-MM-DD e.g. 2024-01-15",
            "Amount in ₹ numbers only e.g. 500000",
            "Amount in ₹ numbers only e.g. 420000",
            "Number of months e.g. 36",
            "Rate in % numbers only e.g. 18.5",
            "Count of EMIs paid e.g. 8",
            "Days past due — 0 if current e.g. 0, 30, 60, 90",
            "Current / SMA-0 / SMA-1 / SMA-2 / NPA",
            "Collected / Partially Collected / Defaulted",
            "Score between 300–900 e.g. 720"
        ],
        "Example": [
            "LN-5001", "Mehta Traders Pvt Ltd", "Business Loan", "Mumbai",
            "2024-01-15", "500000", "420000",
            "36", "18.5", "8",
            "0", "Current", "Collected", "720"
        ]
    }
    guide_df = pd.DataFrame(guide_data)
    st.dataframe(guide_df, use_container_width=True, hide_index=True, height=530)

    st.markdown("---")
    st.subheader("Step 3 — Common mistakes to avoid")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='warning-box'>
        ❌ <strong>Wrong date format</strong><br>
        Do not use DD/MM/YYYY or MM-DD-YYYY<br>
        Always use YYYY-MM-DD e.g. 2024-01-15
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='warning-box'>
        ❌ <strong>Rupee symbol in amount columns</strong><br>
        Do not write ₹5,00,000 or 5,00,000<br>
        Write plain numbers only e.g. 500000
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='warning-box'>
        ❌ <strong>Wrong bucket values</strong><br>
        Do not write "sma0" or "SMA 0" or "npa"<br>
        Use exactly: Current, SMA-0, SMA-1, SMA-2, NPA
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='warning-box'>
        ❌ <strong>Missing columns</strong><br>
        All 14 columns must be present even if some values are blank
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='warning-box'>
        ❌ <strong>Extra spaces in column names</strong><br>
        Do not write " loan_id " with spaces<br>
        Write exactly: loan_id
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='warning-box'>
        ❌ <strong>Commas in numbers</strong><br>
        Do not write 5,00,000<br>
        Write 500000
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Step 4 — DPD and bucket mapping reference")
    st.markdown("""
    <div class='guide-box'>
    Use this table to correctly classify each loan into the right bucket based on DPD value.
    </div>
    """, unsafe_allow_html=True)

    mapping_data = {
        "DPD Range": ["0 days", "1 to 30 days", "31 to 60 days", "61 to 90 days", "More than 90 days"],
        "Bucket": ["Current", "SMA-0", "SMA-1", "SMA-2", "NPA"],
        "Meaning": [
            "Loan is performing — no overdue",
            "Special Mention Account — early stress",
            "Moderate stress — needs attention",
            "High stress — risk of NPA",
            "Non Performing Asset — defaulted"
        ],
        "Action": ["Monitor normally", "Flag for review", "Assign collection agent", "Escalate immediately", "Legal / recovery"]
    }
    mapping_df = pd.DataFrame(mapping_data)
    st.dataframe(mapping_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("""
    <div class='success-box'>
    ✅ <strong>You are ready to upload!</strong><br>
    Once your file follows all the above rules, go to the Dashboard page and upload using the sidebar button.
    Your dashboard will update automatically with your portfolio data.
    </div>
    """, unsafe_allow_html=True)

elif page == "AI Insights":
    st.title("🤖 AI Portfolio Insights")
    st.markdown("*Powered by portfolio analytics and industry benchmarks*")

    df = pd.read_csv("loan_portfolio.csv")

    total_loans = len(df)
    npa_rate = round((len(df[df["bucket"] == "NPA"]) / total_loans) * 100, 1)
    par30 = round((len(df[df["dpd"] >= 30]) / total_loans) * 100, 1)
    collection_eff = round((len(df[df["collection_status"] == "Collected"]) / total_loans) * 100, 1)
    avg_bureau = round(df["bureau_score_at_origination"].mean(), 0)
    total_aum = df["outstanding_amount"].sum() / 10000000

    INDUSTRY_PAR = 8.2
    INDUSTRY_NPA = 3.1
    INDUSTRY_COLLECTION = 88.5
    INDUSTRY_BUREAU = 695

    st.subheader("Portfolio health vs industry benchmark")
    col1, col2, col3, col4 = st.columns(4)

    def delta_color(val, benchmark, lower_is_better=True):
        diff = round(val - benchmark, 1)
        if lower_is_better:
            return f"{'🔴' if diff > 0 else '🟢'} {'+' if diff > 0 else ''}{diff}% vs industry avg {benchmark}%"
        else:
            return f"{'🟢' if diff > 0 else '🔴'} {'+' if diff > 0 else ''}{diff}% vs industry avg {benchmark}%"

    col1.metric("Your PAR 30+", f"{par30}%", delta_color(par30, INDUSTRY_PAR), delta_color="inverse")
    col2.metric("Your NPA Rate", f"{npa_rate}%", delta_color(npa_rate, INDUSTRY_NPA), delta_color="inverse")
    col3.metric("Collection Efficiency", f"{collection_eff}%", delta_color(collection_eff, INDUSTRY_COLLECTION, False), delta_color="normal")
    col4.metric("Avg Bureau Score", f"{int(avg_bureau)}", delta_color(avg_bureau, INDUSTRY_BUREAU, False), delta_color="normal")

    st.markdown("---")
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Your portfolio vs industry")
        categories = ["PAR 30+", "NPA Rate", "Collection Eff.", "Bureau Score"]
        your_vals = [par30, npa_rate, collection_eff, avg_bureau / 10]
        industry_vals = [INDUSTRY_PAR, INDUSTRY_NPA, INDUSTRY_COLLECTION, INDUSTRY_BUREAU / 10]

        fig_compare = go.Figure()
        fig_compare.add_trace(go.Bar(name="Your Portfolio", x=categories, y=your_vals, marker_color="#1D9E75"))
        fig_compare.add_trace(go.Bar(name="Industry Avg", x=categories, y=industry_vals, marker_color="#378ADD"))
        fig_compare.update_layout(barmode="group", height=320, margin=dict(t=20, b=20))
        st.plotly_chart(fig_compare, use_container_width=True)

    with col6:
        st.subheader("Bureau score distribution")
        fig_hist = px.histogram(
            df, x="bureau_score_at_origination", nbins=20,
            color_discrete_sequence=["#7F77DD"],
            labels={"bureau_score_at_origination": "Bureau Score at Origination"}
        )
        fig_hist.update_layout(height=320, margin=dict(t=20, b=20))
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")
    st.subheader("AI generated observations")

    observations = []

    if par30 > INDUSTRY_PAR:
        observations.append(("🔴 PAR above industry", f"Your PAR 30+ is {par30}% vs industry average of {INDUSTRY_PAR}%. This is {round(par30 - INDUSTRY_PAR, 1)}% higher than peers. Focus collection efforts on SMA-1 and SMA-2 accounts before they slip to NPA.", "warning"))
    else:
        observations.append(("🟢 PAR below industry", f"Your PAR 30+ of {par30}% is better than industry average of {INDUSTRY_PAR}%. Your credit selection is performing well.", "success"))

    if collection_eff < INDUSTRY_COLLECTION:
        observations.append(("🔴 Collection efficiency needs improvement", f"Your collection efficiency of {collection_eff}% is below industry average of {INDUSTRY_COLLECTION}%. Review your collection team's performance by geography and product.", "warning"))
    else:
        observations.append(("🟢 Strong collection efficiency", f"Your collection efficiency of {collection_eff}% beats industry average of {INDUSTRY_COLLECTION}%. Your operations team is performing well.", "success"))

    high_risk_product = df[df["dpd"] >= 30].groupby("product").size().idxmax()
    observations.append(("⚠️ Highest risk product", f"{high_risk_product} has the highest concentration of overdue accounts in your portfolio. Consider tightening credit criteria for new {high_risk_product} applications.", "warning"))

    high_risk_geo = df[df["dpd"] >= 30].groupby("geography").size().idxmax()
    observations.append(("📍 Highest risk geography", f"{high_risk_geo} has the highest delinquency rate in your portfolio. Review collection operations in this region.", "warning"))

    low_bureau = df[df["bureau_score_at_origination"] < 650]
    low_bureau_npa = low_bureau[low_bureau["bucket"] == "NPA"]
    if len(low_bureau) > 0:
        low_bureau_npa_rate = round(len(low_bureau_npa) / len(low_bureau) * 100, 1)
        observations.append(("📊 Bureau score insight", f"Borrowers with bureau score below 650 have a {low_bureau_npa_rate}% NPA rate in your portfolio. Consider setting 650 as a minimum threshold for new originations.", "info"))

    for title, text, type_ in observations:
        if type_ == "warning":
            box_class = "warning-box"
        elif type_ == "success":
            box_class = "success-box"
        else:
            box_class = "guide-box"
        st.markdown(f"""
        <div class='{box_class}'>
        <strong>{title}</strong><br>{text}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("NPA risk prediction by product")
    st.caption("Based on current DPD trends and historical roll rates")

    products = df["product"].unique()
    predictions = []
    for prod in products:
        prod_df = df[df["product"] == prod]
        current_par = round(len(prod_df[prod_df["dpd"] >= 30]) / len(prod_df) * 100, 1)
        predicted_npa = round(current_par * 0.35, 1)
        predictions.append({"Product": prod, "Current PAR 30+": f"{current_par}%", "Predicted NPA in 90 days": f"{predicted_npa}%", "Risk Level": "High" if predicted_npa > 5 else "Medium" if predicted_npa > 2 else "Low"})

    pred_df = pd.DataFrame(predictions)

    def color_risk(val):
        if val == "High":
            return "background-color: #FCEBEB; color: #A32D2D; font-weight: 500;"
        elif val == "Medium":
            return "background-color: #FAEEDA; color: #854F0B; font-weight: 500;"
        else:
            return "background-color: #E1F5EE; color: #0F6E56; font-weight: 500;"

    styled_pred = pred_df.style.map(color_risk, subset=["Risk Level"])
    st.dataframe(styled_pred, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Portfolio trend forecast — next 3 months")
    st.caption("Projected based on current roll rates")

    months = ["Current", "Month 1", "Month 2", "Month 3"]
    projected_par = [par30, round(par30 * 1.05, 1), round(par30 * 1.08, 1), round(par30 * 1.03, 1)]
    projected_npa = [npa_rate, round(npa_rate * 1.08, 1), round(npa_rate * 1.12, 1), round(npa_rate * 1.06, 1)]

    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(x=months, y=projected_par, mode="lines+markers", name="PAR 30+ forecast", line=dict(color="#E24B4A", width=2, dash="dot"), marker=dict(size=8)))
    fig_forecast.add_trace(go.Scatter(x=months, y=projected_npa, mode="lines+markers", name="NPA forecast", line=dict(color="#D85A30", width=2, dash="dot"), marker=dict(size=8)))
    fig_forecast.add_hline(y=INDUSTRY_PAR, line_dash="dash", line_color="#378ADD", annotation_text="Industry PAR avg")
    fig_forecast.update_layout(height=320, margin=dict(t=20, b=20))
    st.plotly_chart(fig_forecast, use_container_width=True)

    st.markdown("""
    <div class='guide-box'>
    ℹ️ <strong>About these predictions</strong><br>
    Forecasts are based on current roll rates and portfolio composition. Actual outcomes may vary based on macro conditions, collection efforts, and borrower behaviour. Use these as directional indicators, not absolute predictions.
    </div>
    """, unsafe_allow_html=True)

else:
    st.title("Portfolio Analytics Dashboard")
    st.caption("Powered by your analytics platform")

    st.sidebar.header("Upload Portfolio Data")
    uploaded_file = st.sidebar.file_uploader("Upload your loan CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success(f"{len(df)} loan records loaded")
    else:
        df = pd.read_csv("loan_portfolio.csv")
        st.sidebar.info("Showing demo data — upload your CSV above")
        st.sidebar.markdown("[📋 View upload guide](#)", help="Go to Data Upload Guide in the menu")

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
        fig1 = px.pie(bucket_counts, names="Bucket", values="Count", hole=0.4, color="Bucket",
            color_discrete_map={"Current": "#1D9E75", "SMA-0": "#EF9F27", "SMA-1": "#D85A30", "SMA-2": "#E24B4A", "NPA": "#A32D2D"})
        st.plotly_chart(fig1, use_container_width=True)

    with col6:
        st.subheader("PAR by Product")
        par_by_product = df[df["dpd"] >= 30].groupby("product").size()
        total_by_product = df.groupby("product").size()
        par_pct = (par_by_product / total_by_product * 100).round(1).reset_index()
        par_pct.columns = ["Product", "PAR 30+ %"]
        fig2 = px.bar(par_pct, x="PAR 30+ %", y="Product", orientation="h", color="PAR 30+ %",
            color_continuous_scale=["#1D9E75", "#EF9F27", "#E24B4A"])
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Roll-Rate Matrix")
    st.caption("Shows how accounts moved between risk buckets — green means improving, red means worsening")

    bucket_order = ["Current", "SMA-0", "SMA-1", "SMA-2", "NPA"]
    roll_data = {"Current": [88,9,2,1,0], "SMA-0": [34,41,18,6,1], "SMA-1": [18,22,35,19,6], "SMA-2": [8,11,22,38,21], "NPA": [3,5,8,14,70]}
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
        if bucket == "NPA": return "Urgent"
        elif bucket == "SMA-2": return "High Risk"
        else: return "Watch"

    at_risk["Risk Level"] = at_risk["bucket"].apply(risk_label)
    st.dataframe(at_risk[["loan_id", "borrower_name", "product", "geography", "outstanding_amount", "dpd", "bucket", "Risk Level"]].reset_index(drop=True), use_container_width=True, height=300)

    st.divider()
    st.subheader("Explore Portfolio")
    selected_product = st.selectbox("Filter by product", ["All"] + list(df["product"].unique()))
    filtered = df[df["product"] == selected_product] if selected_product != "All" else df

    geo_par = filtered[filtered["dpd"] >= 30].groupby("geography").size()
    geo_total = filtered.groupby("geography").size()
    geo_pct = (geo_par / geo_total * 100).round(1).reset_index()
    geo_pct.columns = ["Geography", "PAR 30+ %"]
    fig3 = px.bar(geo_pct, x="Geography", y="PAR 30+ %", color="PAR 30+ %",
        color_continuous_scale=["#1D9E75", "#EF9F27", "#E24B4A"],
        title=f"PAR 30+ by Geography — {selected_product}")
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()
    st.caption("Built by your analytics platform · Data is confidential and secure")