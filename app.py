import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Aadilytics", layout="wide", page_icon="🔷")

st.markdown("""
<style>
    .brand { font-size: 22px; font-weight: 600; color: #1a73e8; letter-spacing: -0.5px; }
    .brand-sub { font-size: 12px; color: #888; margin-top: -4px; }
    .org-badge { background: #e8f0fe; color: #1a73e8; padding: 3px 12px; border-radius: 20px; font-size: 12px; font-weight: 500; }
    .guide-box { background: #f0f7ff; border-left: 4px solid #1a73e8; padding: 1rem 1.5rem; border-radius: 6px; margin-bottom: 1rem; }
    .warning-box { background: #fff8e1; border-left: 4px solid #f9a825; padding: 1rem 1.5rem; border-radius: 6px; margin-bottom: 1rem; }
    .success-box { background: #e8f5e9; border-left: 4px solid #2e7d32; padding: 1rem 1.5rem; border-radius: 6px; margin-bottom: 1rem; }
    .danger-box { background: #fdecea; border-left: 4px solid #c62828; padding: 1rem 1.5rem; border-radius: 6px; margin-bottom: 1rem; }
    .elig-card { padding: 1rem; border-radius: 10px; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

USERS = {
    "demo@nbfc.com":    {"password": "demo123",  "org": "Sunrise NBFC"},
    "admin@nbfc.com":   {"password": "admin123", "org": "Horizon Finance"},
    "user@finance.com": {"password": "finance1", "org": "Bharat Lending Co"},
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "org" not in st.session_state:
    st.session_state.org = ""
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div class="brand">🔷 Aadilytics</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Smart risk analytics for lending teams</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Sign in to your account")
        email = st.text_input("Email address", placeholder="you@nbfc.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        if st.button("Sign in", use_container_width=True):
            if email in USERS and USERS[email]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.org = USERS[email]["org"]
                st.rerun()
            else:
                st.error("Incorrect email or password.")
        st.markdown("---")
        st.caption("Demo: demo@nbfc.com / demo123")
    st.stop()

with st.sidebar:
    st.markdown('<div class="brand">🔷 Aadilytics</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="brand-sub">Smart risk analytics</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<span class="org-badge">🏢 {st.session_state.org}</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigate", ["Dashboard", "Borrower Eligibility", "AI Insights", "Data Upload Guide"], label_visibility="collapsed")
    st.markdown("---")
    if st.button("Sign out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.org = ""
        st.rerun()

if page == "Data Upload Guide":
    st.markdown(f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:1.5rem;"><span style="font-size:24px;font-weight:500;">📋 Data Upload Guide</span><span class="org-badge">🏢 {st.session_state.org}</span></div>', unsafe_allow_html=True)
    st.markdown("Follow this guide before uploading your portfolio data to avoid errors and get accurate results.")
    st.markdown("---")

    st.subheader("Step 1 — Download the sample file")
    st.markdown('<div class="guide-box">Download our sample CSV file and use it as a template — replace sample values with your real loan data.</div>', unsafe_allow_html=True)
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
    st.download_button("⬇️ Download sample CSV", sample_df.to_csv(index=False).encode(), "sample_portfolio.csv", "text/csv", use_container_width=True)

    st.markdown("---")
    st.subheader("Step 2 — Required columns")
    st.markdown('<div class="warning-box">⚠️ Your file must have ALL 14 columns listed below. Column names must match exactly — spelling, case, and underscores.</div>', unsafe_allow_html=True)
    guide_df = pd.DataFrame({
        "Column Name": ["loan_id","borrower_name","product","geography","disbursement_date","loan_amount","outstanding_amount","tenure_months","interest_rate","emis_paid","dpd","bucket","collection_status","bureau_score_at_origination"],
        "Data Type": ["Text","Text","Text","Text","Date","Number","Number","Number","Number","Number","Number","Text","Text","Number"],
        "Allowed Values / Format": [
            "Unique ID e.g. LN-1001","Full borrower name",
            "Business Loan / MSME Loan / Equipment Finance / Working Capital / Personal Loan",
            "City name e.g. Mumbai","YYYY-MM-DD e.g. 2024-01-15",
            "₹ in numbers only e.g. 500000","₹ in numbers only e.g. 420000",
            "Months e.g. 36","% e.g. 18.5","Count e.g. 8",
            "0 if current, else 30/60/90/120","Current / SMA-0 / SMA-1 / SMA-2 / NPA",
            "Collected / Partially Collected / Defaulted","300–900 e.g. 720"
        ]
    })
    st.dataframe(guide_df, use_container_width=True, hide_index=True, height=530)

    st.markdown("---")
    st.subheader("Step 3 — Common mistakes")
    c1, c2 = st.columns(2)
    mistakes = [
        ("Wrong date format", "Use YYYY-MM-DD not DD/MM/YYYY"),
        ("Rupee symbol in amounts", "Write 500000 not ₹5,00,000"),
        ("Wrong bucket spelling", "Use exactly: Current, SMA-0, SMA-1, SMA-2, NPA"),
        ("Commas in numbers", "Write 500000 not 5,00,000"),
        ("Extra spaces in column names", "loan_id not ' loan_id '"),
        ("Missing columns", "All 14 columns must be present"),
    ]
    for i, (title, desc) in enumerate(mistakes):
        with c1 if i % 2 == 0 else c2:
            st.markdown(f'<div class="warning-box">❌ <strong>{title}</strong><br>{desc}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Step 4 — DPD and bucket reference")
    st.dataframe(pd.DataFrame({
        "DPD Range": ["0 days","1–30 days","31–60 days","61–90 days","90+ days"],
        "Bucket": ["Current","SMA-0","SMA-1","SMA-2","NPA"],
        "Meaning": ["Performing — no overdue","Early stress","Moderate stress","High stress","Defaulted"],
        "Action": ["Monitor","Flag for review","Assign collection","Escalate","Legal / recovery"]
    }), use_container_width=True, hide_index=True)
    st.markdown('<div class="success-box">✅ <strong>Ready to upload!</strong> Go to Dashboard and upload using the sidebar button.</div>', unsafe_allow_html=True)

elif page == "Borrower Eligibility":
    st.markdown(f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:1.5rem;"><span style="font-size:24px;font-weight:500;">👤 Borrower Eligibility</span><span class="org-badge">🏢 {st.session_state.org}</span></div>', unsafe_allow_html=True)
    st.markdown("Every borrower in your portfolio is automatically categorised based on repayment behaviour, DPD history, and bureau score.")

    uploaded_file = st.sidebar.file_uploader("Upload your loan CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success(f"{len(df)} records loaded")
    else:
        df = pd.read_csv("loan_portfolio.csv")
        st.sidebar.info("Showing demo data")

    def categorise(row):
        if row["bucket"] == "NPA" or row["dpd"] > 90:
            return "Blacklisted", "🔴", "No new loans. Immediate recovery action required.", "#fdecea", "#c62828"
        elif row["bucket"] == "SMA-2" or row["dpd"] > 60:
            return "High Risk", "🔴", "Not eligible for new loans. Focus on collection.", "#fdecea", "#c62828"
        elif row["bucket"] == "SMA-1" or row["dpd"] > 30:
            return "Risky", "🟠", "On watch. New loans only with additional collateral.", "#fff8e1", "#e65100"
        elif row["bucket"] == "SMA-0" or row["dpd"] > 0:
            return "Borderline", "🟡", "Eligible for small top-up loans only. Monitor closely.", "#fffde7", "#f9a825"
        elif row["bureau_score_at_origination"] >= 720 and row["collection_status"] == "Collected":
            return "Premium", "🟢", "Excellent borrower. Eligible for higher loan amounts and better rates.", "#e8f5e9", "#1b5e20"
        elif row["bureau_score_at_origination"] >= 680 and row["collection_status"] == "Collected":
            return "Eligible", "🟢", "Good borrower. Eligible for new loans at standard terms.", "#e8f5e9", "#2e7d32"
        else:
            return "Review Needed", "🔵", "Needs manual review before new loan approval.", "#e8f0fe", "#1a237e"

    df[["eligibility", "icon", "reason", "bg", "color"]] = df.apply(
        lambda r: pd.Series(categorise(r)), axis=1
    )

    st.markdown("---")
    st.subheader("Eligibility summary")
    elig_counts = df["eligibility"].value_counts()
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    cats = ["Premium", "Eligible", "Borderline", "Review Needed", "Risky", "High Risk", "Blacklisted"]
    cols = [col1, col2, col3, col4, col5, col6, col7]
    colors = ["#1b5e20", "#2e7d32", "#f9a825", "#1a237e", "#e65100", "#c62828", "#b71c1c"]
    for cat, col, clr in zip(cats, cols, colors):
        count = elig_counts.get(cat, 0)
        pct = round(count / len(df) * 100, 1)
        col.markdown(f'<div style="background:#f8f9fa;border-radius:10px;padding:12px;text-align:center;border-top:3px solid {clr};"><div style="font-size:20px;font-weight:600;color:{clr};">{count}</div><div style="font-size:11px;color:#888;">{cat}</div><div style="font-size:11px;color:#aaa;">{pct}%</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Eligibility distribution")
        fig_elig = px.pie(
            df["eligibility"].value_counts().reset_index(),
            names="eligibility", values="count", hole=0.4,
            color="eligibility",
            color_discrete_map={
                "Premium": "#1b5e20", "Eligible": "#2e7d32",
                "Borderline": "#f9a825", "Review Needed": "#3949ab",
                "Risky": "#e65100", "High Risk": "#c62828", "Blacklisted": "#b71c1c"
            }
        )
        st.plotly_chart(fig_elig, use_container_width=True)

    with c2:
        st.subheader("Eligible vs not eligible by product")
        df["eligible_flag"] = df["eligibility"].apply(lambda x: "Eligible for new loan" if x in ["Premium", "Eligible"] else "Not eligible")
        prod_elig = df.groupby(["product", "eligible_flag"]).size().reset_index(name="count")
        fig_prod = px.bar(prod_elig, x="product", y="count", color="eligible_flag",
            color_discrete_map={"Eligible for new loan": "#1D9E75", "Not eligible": "#E24B4A"},
            barmode="stack")
        fig_prod.update_layout(height=340, margin=dict(t=10, b=10))
        st.plotly_chart(fig_prod, use_container_width=True)

    st.markdown("---")
    st.subheader("Borrower eligibility list")
    filter_elig = st.multiselect("Filter by eligibility category", options=cats, default=cats)
    filtered_elig = df[df["eligibility"].isin(filter_elig)]

    for _, row in filtered_elig.head(50).iterrows():
        st.markdown(f"""
        <div style="background:{row['bg']};border-radius:8px;padding:12px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
            <div>
                <span style="font-weight:500;color:#333;">{row['icon']} {row['borrower_name']}</span>
                <span style="font-size:12px;color:#666;margin-left:12px;">{row['product']} · {row['geography']}</span>
            </div>
            <div style="text-align:right;">
                <span style="font-size:12px;font-weight:500;color:{row['color']};background:white;padding:2px 10px;border-radius:20px;">{row['eligibility']}</span>
                <div style="font-size:11px;color:#888;margin-top:3px;">{row['reason']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Download eligibility report")
    export_df = df[["loan_id", "borrower_name", "product", "geography", "dpd", "bucket", "bureau_score_at_origination", "eligibility", "reason"]].copy()
    st.download_button("⬇️ Download full eligibility report", export_df.to_csv(index=False).encode(), "eligibility_report.csv", "text/csv", use_container_width=True)

elif page == "AI Insights":
    st.markdown(f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:1.5rem;"><span style="font-size:24px;font-weight:500;">🤖 AI Insights</span><span class="org-badge">🏢 {st.session_state.org}</span></div>', unsafe_allow_html=True)

    df = pd.read_csv("loan_portfolio.csv")
    total_loans = len(df)
    npa_rate = round((len(df[df["bucket"] == "NPA"]) / total_loans) * 100, 1)
    par30 = round((len(df[df["dpd"] >= 30]) / total_loans) * 100, 1)
    collection_eff = round((len(df[df["collection_status"] == "Collected"]) / total_loans) * 100, 1)
    avg_bureau = round(df["bureau_score_at_origination"].mean(), 0)

    INDUSTRY_PAR = 8.2
    INDUSTRY_NPA = 3.1
    INDUSTRY_COLLECTION = 88.5
    INDUSTRY_BUREAU = 695

    st.subheader("Your portfolio vs industry benchmark")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("PAR 30+", f"{par30}%", f"{round(par30-INDUSTRY_PAR,1)}% vs industry {INDUSTRY_PAR}%", delta_color="inverse")
    c2.metric("NPA Rate", f"{npa_rate}%", f"{round(npa_rate-INDUSTRY_NPA,1)}% vs industry {INDUSTRY_NPA}%", delta_color="inverse")
    c3.metric("Collection Efficiency", f"{collection_eff}%", f"{round(collection_eff-INDUSTRY_COLLECTION,1)}% vs industry {INDUSTRY_COLLECTION}%")
    c4.metric("Avg Bureau Score", f"{int(avg_bureau)}", f"{round(avg_bureau-INDUSTRY_BUREAU,0)} vs industry {INDUSTRY_BUREAU}")

    st.markdown("---")
    c5, c6 = st.columns(2)
    with c5:
        st.subheader("Portfolio vs industry")
        fig_compare = go.Figure()
        fig_compare.add_trace(go.Bar(name="Your Portfolio", x=["PAR 30+","NPA Rate","Collection Eff."], y=[par30, npa_rate, collection_eff], marker_color="#1D9E75"))
        fig_compare.add_trace(go.Bar(name="Industry Avg", x=["PAR 30+","NPA Rate","Collection Eff."], y=[INDUSTRY_PAR, INDUSTRY_NPA, INDUSTRY_COLLECTION], marker_color="#378ADD"))
        fig_compare.update_layout(barmode="group", height=300, margin=dict(t=10,b=10))
        st.plotly_chart(fig_compare, use_container_width=True)

    with c6:
        st.subheader("Bureau score distribution")
        fig_hist = px.histogram(df, x="bureau_score_at_origination", nbins=20, color_discrete_sequence=["#7F77DD"])
        fig_hist.update_layout(height=300, margin=dict(t=10,b=10))
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")
    st.subheader("AI generated observations")
    observations = []
    if par30 > INDUSTRY_PAR:
        observations.append(("🔴 PAR above industry average", f"Your PAR 30+ is {par30}% vs industry {INDUSTRY_PAR}%. Focus collection on SMA-1 and SMA-2 accounts.", "danger"))
    else:
        observations.append(("🟢 PAR below industry average", f"Your PAR 30+ of {par30}% beats industry average of {INDUSTRY_PAR}%. Credit selection is performing well.", "success"))
    if collection_eff < INDUSTRY_COLLECTION:
        observations.append(("🔴 Collection efficiency below average", f"Your {collection_eff}% is below industry {INDUSTRY_COLLECTION}%. Review collection team performance by geography.", "danger"))
    else:
        observations.append(("🟢 Strong collection efficiency", f"Your {collection_eff}% beats industry {INDUSTRY_COLLECTION}%. Operations team is performing well.", "success"))
    high_risk_product = df[df["dpd"] >= 30].groupby("product").size().idxmax()
    observations.append(("⚠️ Highest risk product", f"{high_risk_product} has the highest overdue concentration. Consider tightening credit criteria for new {high_risk_product} applications.", "warning"))
    high_risk_geo = df[df["dpd"] >= 30].groupby("geography").size().idxmax()
    observations.append(("📍 Highest risk geography", f"{high_risk_geo} has the highest delinquency rate. Review collection operations in this region.", "warning"))
    low_bureau = df[df["bureau_score_at_origination"] < 650]
    if len(low_bureau) > 0:
        lb_npa = round(len(low_bureau[low_bureau["bucket"] == "NPA"]) / len(low_bureau) * 100, 1)
        observations.append(("📊 Bureau score insight", f"Borrowers with score below 650 have {lb_npa}% NPA rate. Consider setting 650 as minimum threshold.", "guide"))

    for title, text, type_ in observations:
        box = {"danger": "danger-box", "success": "success-box", "warning": "warning-box", "guide": "guide-box"}[type_]
        st.markdown(f'<div class="{box}"><strong>{title}</strong><br>{text}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("NPA risk prediction by product")
    products = df["product"].unique()
    pred_rows = []
    for prod in products:
        prod_df = df[df["product"] == prod]
        cur_par = round(len(prod_df[prod_df["dpd"] >= 30]) / len(prod_df) * 100, 1)
        pred_npa = round(cur_par * 0.35, 1)
        pred_rows.append({"Product": prod, "Current PAR 30+": f"{cur_par}%", "Predicted NPA in 90 days": f"{pred_npa}%", "Risk Level": "High" if pred_npa > 5 else "Medium" if pred_npa > 2 else "Low"})
    pred_df = pd.DataFrame(pred_rows)
    def color_risk(val):
        if val == "High": return "background-color:#FCEBEB;color:#A32D2D;font-weight:500;"
        elif val == "Medium": return "background-color:#FAEEDA;color:#854F0B;font-weight:500;"
        else: return "background-color:#E1F5EE;color:#0F6E56;font-weight:500;"
    st.dataframe(pred_df.style.map(color_risk, subset=["Risk Level"]), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("3 month portfolio forecast")
    months = ["Current", "Month 1", "Month 2", "Month 3"]
    fig_fc = go.Figure()
    fig_fc.add_trace(go.Scatter(x=months, y=[par30, round(par30*1.05,1), round(par30*1.08,1), round(par30*1.03,1)], mode="lines+markers", name="PAR 30+ forecast", line=dict(color="#E24B4A", width=2, dash="dot")))
    fig_fc.add_trace(go.Scatter(x=months, y=[npa_rate, round(npa_rate*1.08,1), round(npa_rate*1.12,1), round(npa_rate*1.06,1)], mode="lines+markers", name="NPA forecast", line=dict(color="#D85A30", width=2, dash="dot")))
    fig_fc.add_hline(y=INDUSTRY_PAR, line_dash="dash", line_color="#378ADD", annotation_text="Industry PAR avg")
    fig_fc.update_layout(height=300, margin=dict(t=10,b=10))
    st.plotly_chart(fig_fc, use_container_width=True)

else:
    st.markdown(f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:1.5rem;"><span style="font-size:24px;font-weight:500;">📊 Portfolio Dashboard</span><span class="org-badge">🏢 {st.session_state.org}</span></div>', unsafe_allow_html=True)

    st.sidebar.header("Upload Portfolio Data")
    uploaded_file = st.sidebar.file_uploader("Upload your loan CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success(f"{len(df)} records loaded")
    else:
        df = pd.read_csv("loan_portfolio.csv")
        st.sidebar.info("Showing demo data — upload your CSV above")

    total_aum = df["outstanding_amount"].sum() / 10000000
    total_loans = len(df)
    npa_rate = round((len(df[df["bucket"] == "NPA"]) / total_loans) * 100, 1)
    par30 = round((len(df[df["dpd"] >= 30]) / total_loans) * 100, 1)
    collection_eff = round((len(df[df["collection_status"] == "Collected"]) / total_loans) * 100, 1)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total AUM", f"₹{total_aum:.1f} Cr")
    c2.metric("PAR 30+", f"{par30}%")
    c3.metric("NPA Rate", f"{npa_rate}%")
    c4.metric("Collection Efficiency", f"{collection_eff}%")

    st.markdown("---")

    st.subheader("Interactive portfolio explorer")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        selected_product = st.selectbox("Product", ["All"] + sorted(df["product"].unique().tolist()))
    with col_f2:
        selected_geo = st.selectbox("Geography", ["All"] + sorted(df["geography"].unique().tolist()))
    with col_f3:
        selected_bucket = st.selectbox("Bucket", ["All"] + ["Current", "SMA-0", "SMA-1", "SMA-2", "NPA"])

    filtered = df.copy()
    if selected_product != "All": filtered = filtered[filtered["product"] == selected_product]
    if selected_geo != "All": filtered = filtered[filtered["geography"] == selected_geo]
    if selected_bucket != "All": filtered = filtered[filtered["bucket"] == selected_bucket]

    f1, f2, f3 = st.columns(3)
    f1.metric("Filtered loans", len(filtered))
    f2.metric("Filtered AUM", f"₹{filtered['outstanding_amount'].sum()/10000000:.1f} Cr")
    f3.metric("Filtered PAR 30+", f"{round(len(filtered[filtered['dpd']>=30])/max(len(filtered),1)*100,1)}%")

    st.markdown("---")
    ch1, ch2 = st.columns(2)

    with ch1:
        st.subheader("Portfolio by DPD bucket")
        bucket_counts = filtered["bucket"].value_counts().reset_index()
        bucket_counts.columns = ["Bucket", "Count"]
        fig1 = px.pie(bucket_counts, names="Bucket", values="Count", hole=0.4,
            color="Bucket", color_discrete_map={"Current":"#1D9E75","SMA-0":"#EF9F27","SMA-1":"#D85A30","SMA-2":"#E24B4A","NPA":"#A32D2D"})
        fig1.update_traces(hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>")
        st.plotly_chart(fig1, use_container_width=True)

    with ch2:
        st.subheader("PAR by product")
        par_prod = (filtered[filtered["dpd"]>=30].groupby("product").size() / filtered.groupby("product").size() * 100).round(1).reset_index()
        par_prod.columns = ["Product", "PAR 30+ %"]
        fig2 = px.bar(par_prod, x="PAR 30+ %", y="Product", orientation="h",
            color="PAR 30+ %", color_continuous_scale=["#1D9E75","#EF9F27","#E24B4A"])
        fig2.update_traces(hovertemplate="<b>%{y}</b><br>PAR 30+: %{x}%<extra></extra>")
        fig2.update_layout(height=320, margin=dict(t=10,b=10))
        st.plotly_chart(fig2, use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        st.subheader("Outstanding by geography")
        geo_aum = filtered.groupby("geography")["outstanding_amount"].sum().reset_index()
        geo_aum.columns = ["Geography", "Outstanding"]
        geo_aum["Outstanding (Cr)"] = (geo_aum["Outstanding"] / 10000000).round(2)
        fig3 = px.bar(geo_aum, x="Geography", y="Outstanding (Cr)", color="Outstanding (Cr)",
            color_continuous_scale=["#B5D4F4","#1D9E75"])
        fig3.update_traces(hovertemplate="<b>%{x}</b><br>AUM: ₹%{y} Cr<extra></extra>")
        fig3.update_layout(height=300, margin=dict(t=10,b=10))
        st.plotly_chart(fig3, use_container_width=True)

    with ch4:
        st.subheader("Bureau score vs DPD")
        fig4 = px.scatter(filtered, x="bureau_score_at_origination", y="dpd",
            color="bucket", size="outstanding_amount",
            color_discrete_map={"Current":"#1D9E75","SMA-0":"#EF9F27","SMA-1":"#D85A30","SMA-2":"#E24B4A","NPA":"#A32D2D"},
            hover_data=["borrower_name","product","geography"])
        fig4.update_layout(height=300, margin=dict(t=10,b=10))
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.subheader("Roll-rate matrix")
    st.caption("Account movement between buckets — green = improving, red = worsening")
    bucket_order = ["Current","SMA-0","SMA-1","SMA-2","NPA"]
    roll_data = {"Current":[88,9,2,1,0],"SMA-0":[34,41,18,6,1],"SMA-1":[18,22,35,19,6],"SMA-2":[8,11,22,38,21],"NPA":[3,5,8,14,70]}
    roll_df = pd.DataFrame(roll_data, index=bucket_order)
    roll_df.index.name = "Last Month →"
    def color_cells(val):
        if val >= 60: return "background-color:#1D9E75;color:white;font-weight:500;text-align:center;"
        elif val >= 30: return "background-color:#9FE1CB;color:#085041;font-weight:500;text-align:center;"
        elif val >= 15: return "background-color:#FAEEDA;color:#854F0B;font-weight:500;text-align:center;"
        elif val >= 5: return "background-color:#F0997B;color:#712B13;font-weight:500;text-align:center;"
        else: return "background-color:#FCEBEB;color:#A32D2D;font-weight:500;text-align:center;"
    st.dataframe(roll_df.style.map(color_cells).format("{:.0f}%"), use_container_width=True)

    st.markdown("---")
    st.subheader("Early warning — accounts at risk")
    at_risk = df[df["bucket"].isin(["SMA-2","NPA"])].copy().sort_values("dpd", ascending=False)
    at_risk["outstanding_amount"] = at_risk["outstanding_amount"].apply(lambda x: f"₹{x/100000:.1f}L")
    at_risk["Risk Level"] = at_risk["bucket"].apply(lambda b: "Urgent" if b=="NPA" else "High Risk")
    st.dataframe(at_risk[["loan_id","borrower_name","product","geography","outstanding_amount","dpd","bucket","Risk Level"]].reset_index(drop=True), use_container_width=True, height=280)

    st.markdown("---")
    st.caption("© 2025 Aadilytics · Smart risk analytics for lending teams · Data is confidential and secure")