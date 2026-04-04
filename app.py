import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Aadilytics", layout="wide", page_icon="🔷")

st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .brand { font-size: 22px; font-weight: 700; color: #1a73e8; letter-spacing: -0.5px; }
    .brand-sub { font-size: 12px; color: #888; margin-top: -4px; }
    .org-badge { background: #e8f0fe; color: #1a73e8; padding: 3px 12px; border-radius: 20px; font-size: 12px; font-weight: 500; }
    .guide-box { background: #f0f7ff; border-left: 4px solid #1a73e8; padding: 1rem 1.5rem; border-radius: 6px; margin-bottom: 1rem; }
    .warning-box { background: #fff8e1; border-left: 4px solid #f9a825; padding: 1rem 1.5rem; border-radius: 6px; margin-bottom: 1rem; }
    .success-box { background: #e8f5e9; border-left: 4px solid #2e7d32; padding: 1rem 1.5rem; border-radius: 6px; margin-bottom: 1rem; }
    .danger-box { background: #fdecea; border-left: 4px solid #c62828; padding: 1rem 1.5rem; border-radius: 6px; margin-bottom: 1rem; }
    .info-box { background: #e8f0fe; border-left: 4px solid #1a73e8; padding: 1rem 1.5rem; border-radius: 6px; margin-bottom: 1rem; }
    .metric-row { display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }
    .metric-card { flex: 1; min-width: 120px; background: var(--background-color); border: 1px solid #e0e0e0; border-radius: 12px; padding: 16px; text-align: center; }
    .metric-val { font-size: 22px; font-weight: 700; color: #1a1a2e; }
    .metric-lbl { font-size: 11px; color: #888; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.05em; }
    div[data-testid="stMetricValue"] { font-size: 20px !important; font-weight: 700 !important; color: var(--text-color) !important; }
    div[data-testid="stMetricLabel"] { font-size: 12px !important; color: #888 !important; }
    div[data-testid="stMetricDelta"] { font-size: 11px !important; }
    .stDataFrame { border-radius: 8px; overflow: hidden; }
    section[data-testid="stSidebar"] { background: #0f0f1a !important; }
    section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    section[data-testid="stSidebar"] .stRadio label { color: #e0e0e0 !important; }
    .sidebar-brand { color: #4f9ef7 !important; font-size: 20px; font-weight: 700; }
    .sidebar-sub { color: #888 !important; font-size: 12px; }
    .cid-badge { background: #1a1a3e; color: #7b9ef7; padding: 2px 10px; border-radius: 6px; font-size: 11px; font-family: monospace; font-weight: 500; }
    .loan-card { background: #f8f9ff; border: 1px solid #e8eaed; border-radius: 12px; padding: 16px; margin-bottom: 12px; }
    .tag-green { background: #e8f5e9; color: #2e7d32; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 500; }
    .tag-amber { background: #fff8e1; color: #f9a825; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 500; }
    .tag-red { background: #fdecea; color: #c62828; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 500; }
    .tag-blue { background: #e8f0fe; color: #1a73e8; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

USERS = {
    "demo@nbfc.com":   {"password": "demo123",  "org": "Sunrise NBFC",    "role": "user"},
    "admin@nbfc.com":  {"password": "admin123", "org": "Horizon Finance", "role": "admin"},
    "user@finance.com":{"password": "finance1", "org": "Bharat Lending",  "role": "user"},
}

for key in ["logged_in","org","role","df"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "logged_in" else ("" if key in ["org","role"] else None)

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;margin-bottom:2rem;">
            <div style="font-size:36px;font-weight:800;background:linear-gradient(135deg,#1a73e8,#6c47ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-1px;">🔷 Aadilytics</div>
            <div style="font-size:14px;color:#888;margin-top:6px;">Smart credit risk analytics for lending teams</div>
        </div>
        """, unsafe_allow_html=True)
        with st.container():
            email = st.text_input("Email address", placeholder="you@nbfc.com", label_visibility="visible")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            if st.button("Sign in", use_container_width=True, type="primary"):
                if email in USERS and USERS[email]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.org = USERS[email]["org"]
                    st.session_state.role = USERS[email]["role"]
                    st.rerun()
                else:
                    st.error("Incorrect email or password.")
        st.markdown("---")
        st.caption("Demo login: demo@nbfc.com / demo123")
        st.caption("Admin login: admin@nbfc.com / admin123")
    st.stop()

with st.sidebar:
    st.markdown('<div class="sidebar-brand">🔷 Aadilytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Credit risk analytics</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<span class="org-badge">🏢 {st.session_state.org}</span>', unsafe_allow_html=True)
    if st.session_state.role == "admin":
        st.markdown('<span style="background:#1a1a3e;color:#7b9ef7;padding:2px 8px;border-radius:6px;font-size:11px;margin-left:6px;">ADMIN</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload portfolio CSV", type=["csv"])
    if uploaded_file:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.success(f"{len(st.session_state.df)} records loaded")
    elif st.session_state.df is None:
        st.session_state.df = pd.read_csv("loan_portfolio.csv")
        st.info("Showing demo data")
    st.markdown("---")
    pages = ["📊 Dashboard", "🔍 Borrower Analysis", "✅ Pre-Disbursal Check", "👤 Eligibility", "🤖 AI Insights", "📋 Upload Guide"]
    if st.session_state.role == "admin":
        pages.append("🔧 Admin Panel")
    page = st.radio("Navigate", pages, label_visibility="collapsed")
    st.markdown("---")
    if st.button("Sign out", use_container_width=True):
        for key in ["logged_in","org","role","df"]:
            st.session_state[key] = False if key == "logged_in" else ("" if key in ["org","role"] else None)
        st.rerun()

df = st.session_state.df.copy()
has_cid = "customer_id" in df.columns
has_pan = "pan" in df.columns
has_phone = "phone" in df.columns

def page_header(title):
    st.markdown(f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:1.5rem;"><span style="font-size:24px;font-weight:700;">{title}</span><span class="org-badge">🏢 {st.session_state.org}</span></div>', unsafe_allow_html=True)

def safe_par(data):
    if len(data) == 0: return 0.0
    return round(len(data[data["dpd"] >= 30]) / len(data) * 100, 1)

def safe_npa(data):
    if len(data) == 0: return 0.0
    return round(len(data[data["bucket"] == "NPA"]) / len(data) * 100, 1)

def safe_collection(data):
    if len(data) == 0: return 0.0
    return round(len(data[data["collection_status"] == "Collected"]) / len(data) * 100, 1)

def safe_aum(data):
    return round(data["outstanding_amount"].sum() / 10000000, 1)

def bucket_color(bucket):
    return {"Current":"#1D9E75","SMA-0":"#EF9F27","SMA-1":"#D85A30","SMA-2":"#E24B4A","NPA":"#A32D2D"}.get(bucket,"#888")

def bucket_bg(bucket):
    return {"Current":"#e8f5e9","SMA-0":"#fff8e1","SMA-1":"#fff3e0","SMA-2":"#fdecea","NPA":"#fdecea"}.get(bucket,"#f5f5f5")

def calc_emi(principal, rate_annual, tenure_months):
    if tenure_months == 0 or rate_annual == 0: return 0
    r = rate_annual / 100 / 12
    return round(principal * r * (1+r)**tenure_months / ((1+r)**tenure_months - 1), 0)

BUCKET_ORDER = ["Current","SMA-0","SMA-1","SMA-2","NPA"]
COLOR_MAP = {"Current":"#1D9E75","SMA-0":"#EF9F27","SMA-1":"#D85A30","SMA-2":"#E24B4A","NPA":"#A32D2D"}

if page == "📊 Dashboard":
    page_header("📊 Portfolio Dashboard")
    cf1, cf2, cf3 = st.columns(3)
    with cf1:
        sel_product = st.selectbox("Product", ["All"] + sorted(df["product"].unique().tolist()))
    with cf2:
        sel_geo = st.selectbox("Geography", ["All"] + sorted(df["geography"].unique().tolist()))
    with cf3:
        sel_bucket = st.selectbox("Bucket", ["All"] + BUCKET_ORDER)

    filt = df.copy()
    if sel_product != "All": filt = filt[filt["product"] == sel_product]
    if sel_geo != "All": filt = filt[filt["geography"] == sel_geo]
    if sel_bucket != "All": filt = filt[filt["bucket"] == sel_bucket]

    st.markdown("---")
    unique_customers = filt["customer_id"].nunique() if has_cid else len(filt["borrower_name"].unique())
    m1,m2,m3,m4,m5,m6 = st.columns(6)
    m1.metric("Customers", f"{unique_customers:,}")
    m2.metric("Loan accounts", f"{len(filt):,}")
    m3.metric("Total AUM", f"Rs.{safe_aum(filt)} Cr")
    m4.metric("PAR 30+", f"{safe_par(filt)}%")
    m5.metric("NPA Rate", f"{safe_npa(filt)}%")
    m6.metric("Collection Eff.", f"{safe_collection(filt)}%")

    st.markdown("---")
    ch1, ch2 = st.columns(2)
    with ch1:
        st.subheader("Portfolio by DPD bucket")
        if len(filt) > 0:
            bc = filt["bucket"].value_counts().reset_index()
            bc.columns = ["Bucket","Count"]
            fig1 = px.pie(bc, names="Bucket", values="Count", hole=0.4, color="Bucket", color_discrete_map=COLOR_MAP)
            fig1.update_layout(height=320, margin=dict(t=10,b=10))
            st.plotly_chart(fig1, use_container_width=True)
    with ch2:
        st.subheader("PAR 30+ by product")
        if len(filt) > 0:
            pp = [{"Product":p,"PAR 30+%":safe_par(filt[filt["product"]==p]),"Loans":len(filt[filt["product"]==p])} for p in filt["product"].unique()]
            pp_df = pd.DataFrame(pp).sort_values("PAR 30+%", ascending=True)
            fig2 = px.bar(pp_df, x="PAR 30+%", y="Product", orientation="h", color="PAR 30+%", color_continuous_scale=["#1D9E75","#EF9F27","#E24B4A"])
            fig2.update_layout(height=320, margin=dict(t=10,b=10))
            st.plotly_chart(fig2, use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        st.subheader("AUM by geography")
        if len(filt) > 0:
            ga = filt.groupby("geography")["outstanding_amount"].sum().reset_index()
            ga.columns = ["Geography","Outstanding"]
            ga["AUM (Cr)"] = (ga["Outstanding"]/10000000).round(2)
            ga = ga.sort_values("AUM (Cr)", ascending=False)
            fig3 = px.bar(ga, x="Geography", y="AUM (Cr)", color="AUM (Cr)", color_continuous_scale=["#B5D4F4","#1D9E75"])
            fig3.update_layout(height=300, margin=dict(t=10,b=10))
            st.plotly_chart(fig3, use_container_width=True)
    with ch4:
        st.subheader("Avg bureau score by bucket")
        if len(filt) > 0:
            bb = filt.groupby("bucket")["bureau_score_at_origination"].mean().round(0).reset_index()
            bb.columns = ["Bucket","Avg Score"]
            bb["Bucket"] = pd.Categorical(bb["Bucket"], categories=BUCKET_ORDER, ordered=True)
            bb = bb.sort_values("Bucket")
            fig4 = go.Figure()
            for _, row in bb.iterrows():
                fig4.add_trace(go.Bar(x=[row["Bucket"]], y=[row["Avg Score"]], name=row["Bucket"], marker_color=COLOR_MAP.get(row["Bucket"],"#888"), text=[f"{int(row['Avg Score'])}"], textposition="outside", showlegend=False))
            fig4.add_hline(y=650, line_dash="dash", line_color="#185FA5", annotation_text="Min threshold (650)", annotation_font=dict(size=11,color="#185FA5"))
            fig4.update_layout(height=300, margin=dict(t=30,b=10), yaxis=dict(title="Avg Bureau Score",range=[500,800]), plot_bgcolor="white", paper_bgcolor="white", yaxis_gridcolor="#f0f0f0")
            st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.subheader("Roll-rate matrix")
    st.caption("Account movement between DPD buckets — green = stable/improving, red = worsening")
    roll_data = {"Current":[88,9,2,1,0],"SMA-0":[34,41,18,6,1],"SMA-1":[18,22,35,19,6],"SMA-2":[8,11,22,38,21],"NPA":[3,5,8,14,70]}
    roll_df = pd.DataFrame(roll_data, index=BUCKET_ORDER)
    roll_df.index.name = "Last Month"
    def color_cells(val):
        if val >= 60: return "background-color:#1D9E75;color:white;font-weight:500;"
        elif val >= 30: return "background-color:#9FE1CB;color:#085041;font-weight:500;"
        elif val >= 15: return "background-color:#FAEEDA;color:#854F0B;font-weight:500;"
        elif val >= 5: return "background-color:#F0997B;color:#712B13;font-weight:500;"
        else: return "background-color:#FCEBEB;color:#A32D2D;font-weight:500;"
    st.dataframe(roll_df.style.map(color_cells).format("{:.0f}%"), use_container_width=True)

    st.markdown("---")
    st.subheader("Early warning — accounts at risk")
    at_risk = filt[filt["bucket"].isin(["SMA-2","NPA"])].copy().sort_values("dpd", ascending=False)
    if len(at_risk) > 0:
        at_risk["outstanding_fmt"] = at_risk["outstanding_amount"].apply(lambda x: f"Rs.{x/100000:.1f}L")
        at_risk["Risk"] = at_risk["bucket"].apply(lambda b: "Urgent" if b == "NPA" else "High Risk")
        show_cols = ["loan_id","borrower_name","product","geography","outstanding_fmt","dpd","bucket","Risk"]
        if has_cid: show_cols = ["customer_id","loan_id","borrower_name","product","geography","outstanding_fmt","dpd","bucket","Risk"]
        st.dataframe(at_risk[show_cols].rename(columns={"outstanding_fmt":"outstanding"}).reset_index(drop=True), use_container_width=True, height=280)
    else:
        st.markdown('<div class="success-box">No accounts at risk in selected filters.</div>', unsafe_allow_html=True)
    st.caption("2025 Aadilytics — Smart risk analytics for lending teams")

elif page == "🔍 Borrower Analysis":
    page_header("🔍 Borrower Analysis")
    st.markdown("Search by customer ID, name, PAN, or phone to view all loan accounts.")
    st.markdown("---")

    sc1, sc2, sc3, sc4 = st.columns([2,2,1,1])
    with sc1:
        search_q = st.text_input("Search", placeholder="Customer ID / Name / PAN / Phone")
    with sc2:
        f_product = st.selectbox("Product", ["All"] + sorted(df["product"].unique().tolist()))
    with sc3:
        f_bucket = st.selectbox("Bucket", ["All"] + BUCKET_ORDER)
    with sc4:
        f_geo = st.selectbox("Geography", ["All"] + sorted(df["geography"].unique().tolist()))

    sdf = df.copy()
    if search_q:
        mask = sdf["borrower_name"].str.contains(search_q, case=False, na=False) | sdf["loan_id"].str.contains(search_q, case=False, na=False)
        if has_cid: mask = mask | sdf["customer_id"].str.contains(search_q, case=False, na=False)
        if has_pan: mask = mask | sdf["pan"].str.contains(search_q, case=False, na=False)
        if has_phone: mask = mask | sdf["phone"].astype(str).str.contains(search_q, case=False, na=False)
        sdf = sdf[mask]
    if f_product != "All": sdf = sdf[sdf["product"] == f_product]
    if f_bucket != "All": sdf = sdf[sdf["bucket"] == f_bucket]
    if f_geo != "All": sdf = sdf[sdf["geography"] == f_geo]

    group_col = "customer_id" if has_cid else "borrower_name"
    unique_customers = sdf[group_col].unique()
    st.markdown(f"**{len(sdf):,} loan accounts across {len(unique_customers):,} customers found**")
    st.markdown("---")

    if len(sdf) == 0:
        st.markdown('<div class="warning-box">No results found. Try searching by name, customer ID, PAN, or phone number.</div>', unsafe_allow_html=True)

    elif len(unique_customers) <= 3:
        for cid in unique_customers:
            c_loans = sdf[sdf[group_col] == cid].copy()
            borrower_name = c_loans["borrower_name"].iloc[0]
            num_loans = len(c_loans)
            total_out = c_loans["outstanding_amount"].sum()
            total_loan = c_loans["loan_amount"].sum()
            total_repaid = total_loan - total_out
            max_dpd = int(c_loans["dpd"].max())
            avg_bureau = int(c_loans["bureau_score_at_origination"].mean())
            worst_bucket = c_loans.sort_values("dpd", ascending=False).iloc[0]["bucket"]
            active = len(c_loans[c_loans["bucket"] != "NPA"])
            npa_count = len(c_loans[c_loans["bucket"] == "NPA"])
            wclr = bucket_color(worst_bucket)
            wbg = bucket_bg(worst_bucket)

            pan_display = c_loans["pan"].iloc[0] if has_pan else "N/A"
            phone_display = c_loans["phone"].iloc[0] if has_phone else "N/A"
            cid_display = cid if has_cid else "N/A"

            st.markdown(f"""
            <div style="background:{wbg};border-radius:12px;padding:20px;margin-bottom:12px;border-left:5px solid {wclr};">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
                    <div>
                        <div style="font-size:20px;font-weight:700;color:#1a1a2e;">{borrower_name}</div>
                        <div style="font-size:13px;color:#666;margin-top:6px;display:flex;gap:12px;flex-wrap:wrap;">
                            <span>🪪 <strong>CID:</strong> {cid_display}</span>
                            <span>📋 <strong>PAN:</strong> {pan_display}</span>
                            <span>📱 <strong>Phone:</strong> {phone_display}</span>
                        </div>
                        <div style="font-size:13px;color:#666;margin-top:4px;">{num_loans} loan account{'s' if num_loans > 1 else ''} with {st.session_state.org}</div>
                    </div>
                    <div style="background:{wclr};color:white;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;">Worst: {worst_bucket}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            km1,km2,km3,km4,km5,km6,km7 = st.columns(7)
            km1.metric("Total accounts", num_loans)
            km2.metric("Active", active)
            km3.metric("NPA accounts", npa_count)
            km4.metric("Total outstanding", f"Rs.{total_out/100000:.1f}L")
            km5.metric("Total repaid", f"Rs.{total_repaid/100000:.1f}L")
            km6.metric("Max DPD", f"{max_dpd}d")
            km7.metric("Avg bureau", avg_bureau)

            st.markdown("---")
            st.subheader(f"All loan accounts")

            for idx, (_, loan) in enumerate(c_loans.iterrows()):
                dpd = int(loan["dpd"])
                bucket = loan["bucket"]
                loan_amt = loan["loan_amount"]
                outstanding = loan["outstanding_amount"]
                repaid = loan_amt - outstanding
                repaid_pct = round(repaid/loan_amt*100, 1) if loan_amt > 0 else 0
                tenure = int(loan["tenure_months"])
                emis_paid = int(loan["emis_paid"])
                emis_rem = max(tenure - emis_paid, 0)
                emi_amt = calc_emi(loan_amt, loan["interest_rate"], tenure)
                total_paid_amt = emi_amt * emis_paid
                total_pend_amt = emi_amt * emis_rem
                lclr = bucket_color(bucket)
                lbg = bucket_bg(bucket)

                with st.expander(f"Account {idx+1} — {loan['loan_id']} · {loan['product']} · {bucket} · DPD {dpd}", expanded=(idx==0)):
                    st.markdown(f'<div style="background:{lbg};border-radius:8px;padding:10px 14px;margin-bottom:12px;border-left:4px solid {lclr};"><span style="color:{lclr};font-weight:600;">{bucket}</span><span style="color:#666;margin-left:12px;">{loan["product"]} · {loan["geography"]} · Disbursed {loan["disbursement_date"]}</span></div>', unsafe_allow_html=True)

                    a1,a2,a3,a4,a5,a6 = st.columns(6)
                    a1.metric("Loan amount", f"Rs.{loan_amt/100000:.1f}L")
                    a2.metric("Outstanding", f"Rs.{outstanding/100000:.1f}L")
                    a3.metric("Repaid", f"Rs.{repaid/100000:.1f}L ({repaid_pct}%)")
                    a4.metric("EMI/month", f"Rs.{emi_amt:,.0f}")
                    a5.metric("DPD", f"{dpd} days")
                    a6.metric("Bureau score", int(loan["bureau_score_at_origination"]))

                    st.markdown("<br>", unsafe_allow_html=True)
                    p1, p2 = st.columns(2)
                    with p1:
                        st.markdown("**EMI progress**")
                        fig_emi = go.Figure()
                        fig_emi.add_trace(go.Bar(name="Paid", x=["EMI count","Amount (L)"], y=[emis_paid, round(total_paid_amt/100000,1)], marker_color="#1D9E75", text=[f"{emis_paid}",f"Rs.{total_paid_amt/100000:.1f}L"], textposition="outside"))
                        fig_emi.add_trace(go.Bar(name="Remaining", x=["EMI count","Amount (L)"], y=[emis_rem, round(total_pend_amt/100000,1)], marker_color="#B5D4F4", text=[f"{emis_rem}",f"Rs.{total_pend_amt/100000:.1f}L"], textposition="outside"))
                        fig_emi.update_layout(barmode="group", height=260, margin=dict(t=20,b=10), plot_bgcolor="white", paper_bgcolor="white", yaxis_gridcolor="#f0f0f0", legend=dict(orientation="h",y=1.1))
                        st.plotly_chart(fig_emi, use_container_width=True)
                    with p2:
                        st.markdown("**Repayment breakdown**")
                        fig_rep = go.Figure()
                        fig_rep.add_trace(go.Bar(x=["Repaid","Outstanding"], y=[round(repaid/100000,1), round(outstanding/100000,1)], marker_color=["#1D9E75","#E24B4A"], text=[f"Rs.{repaid/100000:.1f}L ({repaid_pct}%)",f"Rs.{outstanding/100000:.1f}L ({100-repaid_pct}%)"], textposition="outside"))
                        fig_rep.update_layout(height=260, margin=dict(t=20,b=10), yaxis_title="Lakhs", plot_bgcolor="white", paper_bgcolor="white", yaxis_gridcolor="#f0f0f0", showlegend=False)
                        st.plotly_chart(fig_rep, use_container_width=True)

                    d1, d2 = st.columns(2)
                    with d1:
                        st.markdown(f"""
                        <div style="background:#f8f9fa;border-radius:10px;padding:16px;">
                        <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:10px;font-weight:600;">Loan details</div>
                        <table style="width:100%;font-size:13px;">
                        <tr><td style="color:#666;padding:5px 0;">Loan ID</td><td style="font-weight:600;text-align:right;">{loan["loan_id"]}</td></tr>
                        <tr><td style="color:#666;padding:5px 0;">Product</td><td style="font-weight:600;text-align:right;">{loan["product"]}</td></tr>
                        <tr><td style="color:#666;padding:5px 0;">Disbursement</td><td style="font-weight:600;text-align:right;">{loan["disbursement_date"]}</td></tr>
                        <tr><td style="color:#666;padding:5px 0;">Loan amount</td><td style="font-weight:600;text-align:right;">Rs.{loan_amt/100000:.1f}L</td></tr>
                        <tr><td style="color:#666;padding:5px 0;">Interest rate</td><td style="font-weight:600;text-align:right;">{loan["interest_rate"]}%</td></tr>
                        <tr><td style="color:#666;padding:5px 0;">Tenure</td><td style="font-weight:600;text-align:right;">{tenure} months</td></tr>
                        <tr><td style="color:#666;padding:5px 0;">EMI/month</td><td style="font-weight:600;text-align:right;">Rs.{emi_amt:,.0f}</td></tr>
                        </table></div>""", unsafe_allow_html=True)
                    with d2:
                        st.markdown(f"""
                        <div style="background:#f8f9fa;border-radius:10px;padding:16px;">
                        <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:10px;font-weight:600;">Risk details</div>
                        <table style="width:100%;font-size:13px;">
                        <tr><td style="color:#666;padding:5px 0;">Bucket</td><td style="font-weight:600;text-align:right;color:{lclr};">{bucket}</td></tr>
                        <tr><td style="color:#666;padding:5px 0;">Days past due</td><td style="font-weight:600;text-align:right;">{dpd} days</td></tr>
                        <tr><td style="color:#666;padding:5px 0;">Collection status</td><td style="font-weight:600;text-align:right;">{loan["collection_status"]}</td></tr>
                        <tr><td style="color:#666;padding:5px 0;">Bureau score</td><td style="font-weight:600;text-align:right;">{int(loan["bureau_score_at_origination"])}</td></tr>
                        <tr><td style="color:#666;padding:5px 0;">EMIs paid</td><td style="font-weight:600;text-align:right;">{emis_paid} / {tenure}</td></tr>
                        <tr><td style="color:#666;padding:5px 0;">EMIs remaining</td><td style="font-weight:600;text-align:right;">{emis_rem}</td></tr>
                        <tr><td style="color:#666;padding:5px 0;">Geography</td><td style="font-weight:600;text-align:right;">{loan["geography"]}</td></tr>
                        </table></div>""", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    if bucket == "NPA":
                        st.markdown('<div class="danger-box"><strong>Immediate action required.</strong> NPA account. Initiate legal recovery. No new credit.</div>', unsafe_allow_html=True)
                    elif bucket == "SMA-2":
                        st.markdown('<div class="danger-box"><strong>High priority collection.</strong> 61-90 DPD. Assign senior agent. No new loans.</div>', unsafe_allow_html=True)
                    elif bucket == "SMA-1":
                        st.markdown('<div class="warning-box"><strong>Active monitoring.</strong> 31-60 DPD. Follow up within 48 hours.</div>', unsafe_allow_html=True)
                    elif bucket == "SMA-0":
                        st.markdown('<div class="warning-box"><strong>Early warning.</strong> 1-30 DPD. Contact proactively — may self-cure.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="success-box"><strong>Performing account.</strong> No overdue. Standard monitoring.</div>', unsafe_allow_html=True)

            st.markdown("---")
            bs1, bs2 = st.columns(2)
            with bs1:
                bkt_sum = c_loans.groupby("bucket").agg(Accounts=("loan_id","count"), Outstanding=("outstanding_amount","sum")).reset_index()
                bkt_sum["Outstanding"] = bkt_sum["Outstanding"].apply(lambda x: f"Rs.{x/100000:.1f}L")
                st.markdown("**Accounts by bucket**")
                st.dataframe(bkt_sum, use_container_width=True, hide_index=True)
            with bs2:
                prod_sum = c_loans.groupby("product").agg(Accounts=("loan_id","count"), Outstanding=("outstanding_amount","sum")).reset_index()
                prod_sum["Outstanding"] = prod_sum["Outstanding"].apply(lambda x: f"Rs.{x/100000:.1f}L")
                st.markdown("**Accounts by product**")
                st.dataframe(prod_sum, use_container_width=True, hide_index=True)

            st.download_button(f"Download accounts for {borrower_name}", c_loans.to_csv(index=False).encode(), "borrower_accounts.csv", "text/csv", use_container_width=True)

    else:
        st.subheader("Matching customers")
        st.caption("Narrow your search to see individual customer profiles")
        summary = []
        for cid in unique_customers:
            b = sdf[sdf[group_col] == cid]
            worst = b.sort_values("dpd", ascending=False).iloc[0]["bucket"]
            row = {
                "Customer ID": cid if has_cid else "N/A",
                "Borrower name": b["borrower_name"].iloc[0],
                "PAN": b["pan"].iloc[0] if has_pan else "N/A",
                "Phone": str(b["phone"].iloc[0]) if has_phone else "N/A",
                "Accounts": len(b),
                "Total outstanding": f"Rs.{b['outstanding_amount'].sum()/100000:.1f}L",
                "Max DPD": int(b["dpd"].max()),
                "Worst bucket": worst,
                "Products": ", ".join(b["product"].unique())
            }
            summary.append(row)
        sum_df = pd.DataFrame(summary)
        def color_bucket_col(val):
            bgs = {"Current":"background-color:#e8f5e9","SMA-0":"background-color:#fff8e1","SMA-1":"background-color:#fff3e0","SMA-2":"background-color:#fdecea","NPA":"background-color:#fdecea"}
            return bgs.get(val,"")
        st.dataframe(sum_df.style.map(color_bucket_col, subset=["Worst bucket"]), use_container_width=True, hide_index=True, height=400)
        st.markdown("---")
        s1,s2,s3,s4 = st.columns(4)
        s1.metric("Unique customers", len(unique_customers))
        s2.metric("Total accounts", len(sdf))
        s3.metric("Total AUM", f"Rs.{safe_aum(sdf)} Cr")
        s4.metric("PAR 30+", f"{safe_par(sdf)}%")
        st.download_button("Download full list", sdf.to_csv(index=False).encode(), "search_results.csv", "text/csv", use_container_width=True)

elif page == "✅ Pre-Disbursal Check":
    page_header("✅ Pre-Disbursal Credit Check")
    st.markdown("Complete credit assessment for a borrower before disbursing a new loan.")
    st.markdown("---")

    search_input = st.text_input("Search borrower by name, customer ID or PAN", placeholder="e.g. Mehta Traders / CID-10001 / ABCDE1234F")

    if not search_input:
        st.markdown('<div class="info-box">Enter a borrower name or customer ID above to run a pre-disbursal credit check.</div>', unsafe_allow_html=True)
        st.markdown("**What this check covers:**")
        checks = ["Existing loan obligations and total exposure","Current DPD status and bucket classification","Repayment behaviour across all accounts","Bureau score assessment","Eligibility verdict with recommended loan limit","Risk flags and analyst notes"]
        for c in checks:
            st.markdown(f"- {c}")
    else:
        group_col = "customer_id" if has_cid else "borrower_name"
        mask = df["borrower_name"].str.contains(search_input, case=False, na=False) | df["loan_id"].str.contains(search_input, case=False, na=False)
        if has_cid: mask = mask | df["customer_id"].str.contains(search_input, case=False, na=False)
        if has_pan: mask = mask | df["pan"].str.contains(search_input, case=False, na=False)
        results = df[mask]

        if len(results) == 0:
            st.markdown('<div class="warning-box">Borrower not found. They may be a new customer with no existing loans.</div>', unsafe_allow_html=True)
            st.markdown('<div class="success-box"><strong>New customer.</strong> No existing obligations found in system. Proceed with standard credit appraisal using bureau report and income documents.</div>', unsafe_allow_html=True)
        else:
            unique_cids = results[group_col].unique()
            selected_cid = unique_cids[0]
            if len(unique_cids) > 1:
                selected_cid = st.selectbox("Multiple matches found — select customer", unique_cids)
            borrower_loans = results[results[group_col] == selected_cid].copy()
            borrower_name = borrower_loans["borrower_name"].iloc[0]
            cid_val = borrower_loans["customer_id"].iloc[0] if has_cid else "N/A"
            pan_val = borrower_loans["pan"].iloc[0] if has_pan else "N/A"
            phone_val = str(borrower_loans["phone"].iloc[0]) if has_phone else "N/A"

            total_loans = len(borrower_loans)
            total_outstanding = borrower_loans["outstanding_amount"].sum()
            total_disbursed = borrower_loans["loan_amount"].sum()
            total_repaid = total_disbursed - total_outstanding
            repaid_pct = round(total_repaid/total_disbursed*100, 1) if total_disbursed > 0 else 0
            max_dpd = int(borrower_loans["dpd"].max())
            avg_dpd = round(borrower_loans["dpd"].mean(), 1)
            worst_bucket = borrower_loans.sort_values("dpd", ascending=False).iloc[0]["bucket"]
            avg_bureau = int(borrower_loans["bureau_score_at_origination"].mean())
            npa_accounts = len(borrower_loans[borrower_loans["bucket"] == "NPA"])
            overdue_accounts = len(borrower_loans[borrower_loans["dpd"] > 0])
            performing_accounts = len(borrower_loans[borrower_loans["bucket"] == "Current"])
            total_emi_obligation = sum(calc_emi(r["loan_amount"], r["interest_rate"], r["tenure_months"]) for _, r in borrower_loans.iterrows())

            if npa_accounts > 0:
                overall_verdict = "REJECT"
                verdict_color = "#c62828"
                verdict_bg = "#fdecea"
                verdict_reason = f"Borrower has {npa_accounts} NPA account(s). Credit facility cannot be extended."
            elif worst_bucket == "SMA-2":
                overall_verdict = "REJECT"
                verdict_color = "#c62828"
                verdict_bg = "#fdecea"
                verdict_reason = "Borrower has SMA-2 account(s) with 61-90 DPD. High default risk."
            elif worst_bucket == "SMA-1":
                overall_verdict = "HOLD"
                verdict_color = "#e65100"
                verdict_bg = "#fff3e0"
                verdict_reason = "Borrower has SMA-1 account(s). Regularise existing dues before new disbursement."
            elif worst_bucket == "SMA-0":
                overall_verdict = "CONDITIONAL"
                verdict_color = "#f9a825"
                verdict_bg = "#fff8e1"
                verdict_reason = "Minor overdue detected. Proceed only with additional collateral and smaller loan amount."
            elif avg_bureau >= 700 and repaid_pct >= 40:
                overall_verdict = "APPROVE"
                verdict_color = "#2e7d32"
                verdict_bg = "#e8f5e9"
                verdict_reason = "Good repayment history, clean bureau score. Eligible for new loan."
            elif avg_bureau >= 650:
                overall_verdict = "APPROVE WITH CAUTION"
                verdict_color = "#1565c0"
                verdict_bg = "#e8f0fe"
                verdict_reason = "Satisfactory profile. Approve at standard terms with normal monitoring."
            else:
                overall_verdict = "REVIEW"
                verdict_color = "#6a1b9a"
                verdict_bg = "#f3e5f5"
                verdict_reason = "Low bureau score. Manual credit review required before approval."

            recommended_limit = 0
            if overall_verdict in ["APPROVE","APPROVE WITH CAUTION","CONDITIONAL"]:
                base = total_disbursed / total_loans
                if avg_bureau >= 720 and repaid_pct >= 60: recommended_limit = base * 1.5
                elif avg_bureau >= 680 and repaid_pct >= 40: recommended_limit = base * 1.0
                else: recommended_limit = base * 0.5

            st.markdown(f"""
            <div style="background:{verdict_bg};border-radius:12px;padding:24px;margin-bottom:20px;border-left:6px solid {verdict_color};">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
                    <div>
                        <div style="font-size:22px;font-weight:800;color:{verdict_color};">{overall_verdict}</div>
                        <div style="font-size:14px;color:#555;margin-top:4px;">{verdict_reason}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:12px;color:#888;">Recommended limit</div>
                        <div style="font-size:22px;font-weight:700;color:{verdict_color};">{"Rs."+str(round(recommended_limit/100000,1))+"L" if recommended_limit > 0 else "N/A"}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background:#f8f9fa;border-radius:12px;padding:16px;margin-bottom:16px;">
                <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:10px;font-weight:600;">Borrower identity</div>
                <div style="display:flex;gap:32px;flex-wrap:wrap;font-size:13px;">
                    <div><span style="color:#888;">Name</span><br><strong>{borrower_name}</strong></div>
                    <div><span style="color:#888;">Customer ID</span><br><strong>{cid_val}</strong></div>
                    <div><span style="color:#888;">PAN</span><br><strong>{pan_val}</strong></div>
                    <div><span style="color:#888;">Phone</span><br><strong>{phone_val}</strong></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.subheader("Credit assessment summary")
            ca1,ca2,ca3,ca4,ca5,ca6 = st.columns(6)
            ca1.metric("Total loans", total_loans)
            ca2.metric("Total exposure", f"Rs.{total_outstanding/100000:.1f}L")
            ca3.metric("Repaid so far", f"{repaid_pct}%")
            ca4.metric("Max DPD ever", f"{max_dpd}d")
            ca5.metric("Bureau score", avg_bureau)
            ca6.metric("Monthly EMI load", f"Rs.{total_emi_obligation:,.0f}")

            st.markdown("---")
            st.subheader("Detailed checks")

            checks_data = [
                ("Bureau score", f"{avg_bureau}", "Pass" if avg_bureau >= 650 else "Fail", "Min required: 650"),
                ("NPA accounts", f"{npa_accounts}", "Pass" if npa_accounts == 0 else "Fail", "Must be zero"),
                ("Overdue accounts", f"{overdue_accounts} of {total_loans}", "Pass" if overdue_accounts == 0 else "Warning" if overdue_accounts/total_loans < 0.3 else "Fail", "Overdue ratio"),
                ("Repayment rate", f"{repaid_pct}%", "Pass" if repaid_pct >= 30 else "Warning", "Min 30% repaid"),
                ("Worst bucket", worst_bucket, "Pass" if worst_bucket == "Current" else "Warning" if worst_bucket == "SMA-0" else "Fail", "Should be Current"),
                ("Performing accounts", f"{performing_accounts} of {total_loans}", "Pass" if performing_accounts/total_loans >= 0.7 else "Warning", "Min 70% performing"),
                ("Monthly EMI obligation", f"Rs.{total_emi_obligation:,.0f}", "Pass" if total_emi_obligation < 100000 else "Warning", "Existing monthly load"),
                ("Total exposure", f"Rs.{total_outstanding/100000:.1f}L", "Pass" if total_outstanding < 5000000 else "Warning", "Current outstanding"),
            ]

            chk_df = pd.DataFrame(checks_data, columns=["Check","Value","Status","Note"])
            def color_check(val):
                if val == "Pass": return "background-color:#e8f5e9;color:#2e7d32;font-weight:600;"
                elif val == "Warning": return "background-color:#fff8e1;color:#f9a825;font-weight:600;"
                else: return "background-color:#fdecea;color:#c62828;font-weight:600;"
            st.dataframe(chk_df.style.map(color_check, subset=["Status"]), use_container_width=True, hide_index=True)

            st.markdown("---")
            st.subheader("Existing loan accounts")
            disp = borrower_loans.copy()
            disp["outstanding_fmt"] = disp["outstanding_amount"].apply(lambda x: f"Rs.{x/100000:.1f}L")
            disp["loan_amount_fmt"] = disp["loan_amount"].apply(lambda x: f"Rs.{x/100000:.1f}L")
            disp["emi_fmt"] = disp.apply(lambda r: f"Rs.{calc_emi(r['loan_amount'],r['interest_rate'],r['tenure_months']):,.0f}", axis=1)
            show = disp[["loan_id","product","loan_amount_fmt","outstanding_fmt","emi_fmt","emis_paid","tenure_months","dpd","bucket","collection_status"]].rename(columns={"loan_amount_fmt":"loan amount","outstanding_fmt":"outstanding","emi_fmt":"EMI/month","emis_paid":"EMIs paid","tenure_months":"tenure","collection_status":"collection"})
            def color_bkt(val):
                bgs = {"Current":"background-color:#e8f5e9","SMA-0":"background-color:#fff8e1","SMA-1":"background-color:#fff3e0","SMA-2":"background-color:#fdecea","NPA":"background-color:#fdecea"}
                return bgs.get(val,"")
            st.dataframe(show.style.map(color_bkt, subset=["bucket"]).reset_index(drop=True), use_container_width=True, hide_index=True)

            st.markdown("---")
            col_charts1, col_charts2 = st.columns(2)
            with col_charts1:
                st.subheader("Exposure breakdown")
                fig_exp = go.Figure()
                fig_exp.add_trace(go.Bar(x=["Total disbursed","Total repaid","Outstanding"], y=[total_disbursed/100000, total_repaid/100000, total_outstanding/100000], marker_color=["#378ADD","#1D9E75","#E24B4A"], text=[f"Rs.{total_disbursed/100000:.1f}L",f"Rs.{total_repaid/100000:.1f}L",f"Rs.{total_outstanding/100000:.1f}L"], textposition="outside"))
                fig_exp.update_layout(height=280, margin=dict(t=20,b=10), yaxis_title="Lakhs", plot_bgcolor="white", paper_bgcolor="white", yaxis_gridcolor="#f0f0f0", showlegend=False)
                st.plotly_chart(fig_exp, use_container_width=True)
            with col_charts2:
                st.subheader("Accounts by bucket")
                bkt_c = borrower_loans["bucket"].value_counts().reset_index()
                bkt_c.columns = ["Bucket","Count"]
                fig_bkt = px.pie(bkt_c, names="Bucket", values="Count", hole=0.5, color="Bucket", color_discrete_map=COLOR_MAP)
                fig_bkt.update_layout(height=280, margin=dict(t=10,b=10))
                st.plotly_chart(fig_bkt, use_container_width=True)

            st.markdown("---")
            st.subheader("Risk flags")
            flags = []
            if npa_accounts > 0: flags.append(("🔴", f"{npa_accounts} NPA account(s) detected", "danger"))
            if max_dpd > 90: flags.append(("🔴", f"Historical DPD of {max_dpd} days — high default risk", "danger"))
            if max_dpd > 30: flags.append(("🟠", f"Current max DPD is {max_dpd} days", "warning"))
            if avg_bureau < 650: flags.append(("🔴", f"Bureau score {avg_bureau} is below minimum threshold of 650", "danger"))
            if avg_bureau < 700: flags.append(("🟡", f"Bureau score {avg_bureau} is below preferred threshold of 700", "warning"))
            if total_emi_obligation > 100000: flags.append(("🟠", f"Monthly EMI obligation of Rs.{total_emi_obligation:,.0f} is high", "warning"))
            if total_outstanding > 5000000: flags.append(("🟡", f"Total exposure Rs.{total_outstanding/100000:.1f}L — monitor concentration risk", "warning"))
            if overdue_accounts / total_loans > 0.5: flags.append(("🔴", f"{overdue_accounts} of {total_loans} accounts have overdue — poor repayment track record", "danger"))

            if len(flags) == 0:
                st.markdown('<div class="success-box"><strong>No risk flags.</strong> Clean profile — proceed with standard credit appraisal.</div>', unsafe_allow_html=True)
            else:
                for icon, msg, type_ in flags:
                    box = {"danger":"danger-box","warning":"warning-box"}.get(type_,"warning-box")
                    st.markdown(f'<div class="{box}">{icon} {msg}</div>', unsafe_allow_html=True)

elif page == "👤 Eligibility":
    page_header("👤 Borrower Eligibility")
    st.markdown("Every borrower categorised based on repayment behaviour, DPD, and bureau score.")

    def categorise(row):
        if row["bucket"] == "NPA" or row["dpd"] > 90:
            return "Blacklisted","🔴","No new loans. Immediate recovery action required.","#fdecea","#c62828"
        elif row["bucket"] == "SMA-2" or row["dpd"] > 60:
            return "High Risk","🔴","Not eligible for new loans.","#fdecea","#c62828"
        elif row["bucket"] == "SMA-1" or row["dpd"] > 30:
            return "Risky","🟠","New loans only with additional collateral.","#fff8e1","#e65100"
        elif row["bucket"] == "SMA-0" or row["dpd"] > 0:
            return "Borderline","🟡","Top-up loans only. Monitor closely.","#fffde7","#f9a825"
        elif row["bureau_score_at_origination"] >= 720 and row["collection_status"] == "Collected":
            return "Premium","🟢","Eligible for higher amounts and better rates.","#e8f5e9","#1b5e20"
        elif row["bureau_score_at_origination"] >= 680 and row["collection_status"] == "Collected":
            return "Eligible","🟢","Eligible for new loans at standard terms.","#e8f5e9","#2e7d32"
        else:
            return "Review Needed","🔵","Needs manual review.","#e8f0fe","#1a237e"

    df[["eligibility","icon","reason","bg","color"]] = df.apply(lambda r: pd.Series(categorise(r)), axis=1)
    cats = ["Premium","Eligible","Borderline","Review Needed","Risky","High Risk","Blacklisted"]
    colors = ["#1b5e20","#2e7d32","#f9a825","#1a237e","#e65100","#c62828","#b71c1c"]
    elig_counts = df["eligibility"].value_counts()

    st.markdown("---")
    cols = st.columns(7)
    for cat, col, clr in zip(cats, cols, colors):
        count = elig_counts.get(cat, 0)
        pct = round(count/len(df)*100, 1)
        col.markdown(f'<div style="background:#f8f9fa;border-radius:10px;padding:12px;text-align:center;border-top:3px solid {clr};"><div style="font-size:20px;font-weight:700;color:{clr};">{count}</div><div style="font-size:11px;color:#888;margin-top:2px;">{cat}</div><div style="font-size:11px;color:#aaa;">{pct}%</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    ec1, ec2 = st.columns(2)
    with ec1:
        st.subheader("Eligibility distribution")
        fig_e = px.pie(df["eligibility"].value_counts().reset_index(), names="eligibility", values="count", hole=0.4, color="eligibility", color_discrete_map=dict(zip(cats, colors)))
        fig_e.update_layout(height=320, margin=dict(t=10,b=10))
        st.plotly_chart(fig_e, use_container_width=True)
    with ec2:
        st.subheader("Eligible vs not eligible by product")
        df["eligible_flag"] = df["eligibility"].apply(lambda x: "Eligible" if x in ["Premium","Eligible"] else "Not eligible")
        prod_e = df.groupby(["product","eligible_flag"]).size().reset_index(name="count")
        fig_pe = px.bar(prod_e, x="product", y="count", color="eligible_flag", color_discrete_map={"Eligible":"#1D9E75","Not eligible":"#E24B4A"}, barmode="stack")
        fig_pe.update_layout(height=320, margin=dict(t=10,b=10))
        st.plotly_chart(fig_pe, use_container_width=True)

    st.markdown("---")
    filter_elig = st.multiselect("Filter by category", options=cats, default=cats)
    filtered_elig = df[df["eligibility"].isin(filter_elig)]
    for _, row in filtered_elig.head(50).iterrows():
        st.markdown(f"""
        <div style="background:{row['bg']};border-radius:8px;padding:12px 16px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
            <div>
                <span style="font-weight:600;color:#333;">{row['icon']} {row['borrower_name']}</span>
                <span style="font-size:12px;color:#666;margin-left:12px;">{row['product']} · {row['geography']}</span>
                {"<span style='font-size:11px;color:#888;margin-left:8px;font-family:monospace;'>"+row['customer_id']+"</span>" if has_cid else ""}
            </div>
            <div style="text-align:right;">
                <span style="font-size:12px;font-weight:600;color:{row['color']};background:white;padding:2px 10px;border-radius:20px;">{row['eligibility']}</span>
                <div style="font-size:11px;color:#888;margin-top:3px;">{row['reason']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.download_button("Download eligibility report", filtered_elig[["customer_id" if has_cid else "borrower_name","loan_id","borrower_name","product","geography","dpd","bucket","bureau_score_at_origination","eligibility","reason"]].to_csv(index=False).encode(), "eligibility_report.csv", "text/csv", use_container_width=True)

elif page == "🤖 AI Insights":
    page_header("🤖 AI Insights")
    st.caption(f"Analysis based on {len(df):,} loan records from {st.session_state.org}")

    par30 = safe_par(df)
    npa_rate = safe_npa(df)
    collection_eff = safe_collection(df)
    avg_bureau = round(df["bureau_score_at_origination"].mean(), 0)
    INDUSTRY_PAR = 8.2
    INDUSTRY_NPA = 3.1
    INDUSTRY_COLLECTION = 88.5
    INDUSTRY_BUREAU = 695

    st.subheader("Portfolio vs industry benchmark")
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("PAR 30+", f"{par30}%", f"{round(par30-INDUSTRY_PAR,1)}% vs industry {INDUSTRY_PAR}%", delta_color="inverse")
    m2.metric("NPA Rate", f"{npa_rate}%", f"{round(npa_rate-INDUSTRY_NPA,1)}% vs industry {INDUSTRY_NPA}%", delta_color="inverse")
    m3.metric("Collection Efficiency", f"{collection_eff}%", f"{round(collection_eff-INDUSTRY_COLLECTION,1)}% vs industry {INDUSTRY_COLLECTION}%")
    m4.metric("Avg Bureau Score", f"{int(avg_bureau)}", f"{int(avg_bureau-INDUSTRY_BUREAU)} vs industry {INDUSTRY_BUREAU}")

    st.markdown("---")
    ai1, ai2 = st.columns(2)
    with ai1:
        st.subheader("Your portfolio vs industry")
        fig_c = go.Figure()
        fig_c.add_trace(go.Bar(name="Your Portfolio", x=["PAR 30+","NPA Rate","Collection Eff."], y=[par30,npa_rate,collection_eff], marker_color="#1D9E75"))
        fig_c.add_trace(go.Bar(name="Industry Avg", x=["PAR 30+","NPA Rate","Collection Eff."], y=[INDUSTRY_PAR,INDUSTRY_NPA,INDUSTRY_COLLECTION], marker_color="#378ADD"))
        fig_c.update_layout(barmode="group", height=300, margin=dict(t=10,b=10))
        st.plotly_chart(fig_c, use_container_width=True)
    with ai2:
        st.subheader("Bureau score distribution")
        fig_h = px.histogram(df, x="bureau_score_at_origination", nbins=20, color_discrete_sequence=["#7F77DD"], labels={"bureau_score_at_origination":"Bureau Score"})
        fig_h.update_layout(height=300, margin=dict(t=10,b=10))
        st.plotly_chart(fig_h, use_container_width=True)

    st.markdown("---")
    st.subheader("AI generated observations")
    observations = []
    if par30 > INDUSTRY_PAR:
        observations.append(("🔴 PAR above industry average", f"Your PAR 30+ is {par30}% vs industry {INDUSTRY_PAR}%. Focus collection on SMA-1 and SMA-2 accounts.", "danger"))
    else:
        observations.append(("🟢 PAR below industry average", f"Your PAR 30+ of {par30}% beats industry average of {INDUSTRY_PAR}%.", "success"))
    if collection_eff < INDUSTRY_COLLECTION:
        observations.append(("🔴 Collection efficiency below average", f"Your {collection_eff}% is below industry {INDUSTRY_COLLECTION}%.", "danger"))
    else:
        observations.append(("🟢 Strong collection efficiency", f"Your {collection_eff}% beats industry {INDUSTRY_COLLECTION}%.", "success"))
    hrp = df[df["dpd"] >= 30].groupby("product").size()
    if len(hrp) > 0:
        observations.append(("⚠️ Highest risk product", f"{hrp.idxmax()} has highest overdue concentration.", "warning"))
    hrg = df[df["dpd"] >= 30].groupby("geography").size()
    if len(hrg) > 0:
        observations.append(("📍 Highest risk geography", f"{hrg.idxmax()} has highest delinquency rate.", "warning"))
    lb = df[df["bureau_score_at_origination"] < 650]
    if len(lb) > 0:
        lb_npa = round(len(lb[lb["bucket"]=="NPA"])/len(lb)*100, 1)
        observations.append(("📊 Bureau score insight", f"Borrowers below 650 score have {lb_npa}% NPA rate. Consider 650 as minimum.", "guide"))
    for title, text, type_ in observations:
        box = {"danger":"danger-box","success":"success-box","warning":"warning-box","guide":"guide-box"}[type_]
        st.markdown(f'<div class="{box}"><strong>{title}</strong><br>{text}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("NPA risk prediction by product")
    pred_rows = []
    for prod in df["product"].unique():
        prod_df = df[df["product"]==prod]
        cur_par = safe_par(prod_df)
        pred_npa = round(cur_par*0.35, 1)
        pred_rows.append({"Product":prod,"Loans":len(prod_df),"Current PAR 30+":f"{cur_par}%","Predicted NPA (90d)":f"{pred_npa}%","Risk Level":"High" if pred_npa>5 else "Medium" if pred_npa>2 else "Low"})
    pred_df = pd.DataFrame(pred_rows)
    def color_risk(val):
        if val=="High": return "background-color:#FCEBEB;color:#A32D2D;font-weight:600;"
        elif val=="Medium": return "background-color:#FAEEDA;color:#854F0B;font-weight:600;"
        else: return "background-color:#E1F5EE;color:#0F6E56;font-weight:600;"
    st.dataframe(pred_df.style.map(color_risk, subset=["Risk Level"]), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("3 month portfolio forecast")
    months = ["Current","Month 1","Month 2","Month 3"]
    par_fc = [par30, round(par30*1.05,1), round(par30*1.08,1), round(par30*1.03,1)]
    npa_fc = [npa_rate, round(npa_rate*1.08,1), round(npa_rate*1.12,1), round(npa_rate*1.06,1)]
    fig_fc = go.Figure()
    fig_fc.add_trace(go.Scatter(x=months, y=par_fc, mode="lines+markers+text", name="PAR 30+", line=dict(color="#E24B4A",width=3), marker=dict(size=10,color="#E24B4A"), text=[f"{v}%" for v in par_fc], textposition="top center", textfont=dict(size=12,color="#E24B4A")))
    fig_fc.add_trace(go.Scatter(x=months, y=npa_fc, mode="lines+markers+text", name="NPA Rate", line=dict(color="#1D9E75",width=3,dash="dash"), marker=dict(size=10,color="#1D9E75",symbol="diamond"), text=[f"{v}%" for v in npa_fc], textposition="bottom center", textfont=dict(size=12,color="#1D9E75")))
    fig_fc.add_hrect(y0=0, y1=INDUSTRY_PAR, fillcolor="#E6F1FB", opacity=0.3, layer="below", line_width=0, annotation_text=f"Safe zone (below {INDUSTRY_PAR}%)", annotation_position="top left", annotation_font=dict(size=11,color="#185FA5"))
    fig_fc.update_layout(height=340, margin=dict(t=30,b=10), legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1), yaxis=dict(title="Rate (%)",rangemode="tozero"), plot_bgcolor="white", paper_bgcolor="white", yaxis_gridcolor="#f0f0f0")
    st.plotly_chart(fig_fc, use_container_width=True)
    st.markdown('<div class="guide-box">Forecasts are directional indicators based on current roll rates. Actual outcomes depend on collection efforts and macro conditions.</div>', unsafe_allow_html=True)

elif page == "🔧 Admin Panel":
    if st.session_state.role != "admin":
        st.error("Access denied.")
        st.stop()
    page_header("🔧 Admin Panel")
    admin_tab1, admin_tab2, admin_tab3 = st.tabs(["Logic Transparency","User Management","System Info"])

    with admin_tab1:
        st.subheader("All calculation logic used in Aadilytics")
        st.markdown("---")
        st.markdown("#### PAR (Portfolio at Risk)")
        st.markdown('<div class="guide-box"><strong>Formula:</strong> PAR 30+ = (Loans with DPD >= 30) / (Total loans) x 100<br><strong>Source:</strong> dpd column<br><strong>Type:</strong> Count based, not value based</div>', unsafe_allow_html=True)
        st.markdown("#### NPA Rate")
        st.markdown('<div class="guide-box"><strong>Formula:</strong> NPA Rate = (Loans where bucket = NPA) / (Total loans) x 100<br><strong>Classification:</strong> DPD > 90 days per RBI guidelines</div>', unsafe_allow_html=True)
        st.markdown("#### Collection Efficiency")
        st.markdown('<div class="guide-box"><strong>Formula:</strong> (Loans where collection_status = Collected) / (Total loans) x 100<br><strong>Note:</strong> Count based. Value based version planned for v2.</div>', unsafe_allow_html=True)
        st.markdown("#### EMI Calculation")
        st.markdown('<div class="guide-box"><strong>Formula:</strong> EMI = P × r × (1+r)^n / ((1+r)^n - 1)<br>Where P = principal, r = monthly rate (annual/12/100), n = tenure months</div>', unsafe_allow_html=True)
        st.markdown("#### Bucket Classification")
        st.dataframe(pd.DataFrame({"Bucket":["Current","SMA-0","SMA-1","SMA-2","NPA"],"DPD Range":["0","1-30","31-60","61-90","90+"],"RBI Class":["Standard","SMA-0","SMA-1","SMA-2","NPA"],"Action":["Monitor","Early intervention","Collection","Escalate","Legal"]}), use_container_width=True, hide_index=True)
        st.markdown("#### Pre-Disbursal Verdict Logic")
        st.dataframe(pd.DataFrame({"Condition":["NPA accounts > 0","Worst bucket = SMA-2","Worst bucket = SMA-1","Worst bucket = SMA-0","Bureau >= 700 and repaid >= 40%","Bureau >= 650","Otherwise"],"Verdict":["REJECT","REJECT","HOLD","CONDITIONAL","APPROVE","APPROVE WITH CAUTION","REVIEW"]}), use_container_width=True, hide_index=True)

    with admin_tab2:
        st.subheader("Registered users")
        st.markdown('<div class="warning-box">Demo user list. Database-backed auth comes in next version.</div>', unsafe_allow_html=True)
        user_data = [{"Email":e,"Organisation":i["org"],"Role":i["role"],"Status":"Active"} for e,i in USERS.items()]
        st.dataframe(pd.DataFrame(user_data), use_container_width=True, hide_index=True)

    with admin_tab3:
        st.subheader("System information")
        si1,si2,si3 = st.columns(3)
        si1.metric("Records loaded", f"{len(df):,}")
        si2.metric("Unique customers", f"{df['customer_id'].nunique():,}" if has_cid else "N/A")
        si3.metric("Platform version", "v2.0.0")
        st.markdown("---")
        st.subheader("Data quality check")
        qr = [{"Column":c,"Type":str(df[c].dtype),"Nulls":df[c].isnull().sum(),"Null%":f"{round(df[c].isnull().sum()/len(df)*100,1)}%","Status":"OK" if df[c].isnull().sum()==0 else "Warning"} for c in df.columns]
        qdf = pd.DataFrame(qr)
        def col_status(val):
            return "background-color:#e8f5e9;color:#2e7d32;font-weight:600;" if val=="OK" else "background-color:#fff8e1;color:#f9a825;font-weight:600;"
        st.dataframe(qdf.style.map(col_status, subset=["Status"]), use_container_width=True, hide_index=True)

elif page == "📋 Upload Guide":
    page_header("📋 Data Upload Guide")
    st.markdown("Follow this guide before uploading your portfolio data.")
    st.markdown("---")
    st.subheader("Step 1 — Download sample file")
    st.markdown('<div class="guide-box">Download our sample CSV and use it as a template — replace values with your real loan data.</div>', unsafe_allow_html=True)
    sample_data = {
        "loan_id":["LN-5001","LN-5002","LN-5003","LN-5004"],
        "customer_id":["CID-10001","CID-10001","CID-10002","CID-10003"],
        "borrower_name":["Mehta Traders Pvt Ltd","Mehta Traders Pvt Ltd","Rajan Enterprises","Sunita Textiles"],
        "pan":["ABCDE1234F","ABCDE1234F","BCDEG2345H","CDEFH3456I"],
        "phone":["9876543210","9876543210","9765432109","9654321098"],
        "product":["Business Loan","Working Capital","MSME Loan","Equipment Finance"],
        "geography":["Mumbai","Mumbai","Pune","Nagpur"],
        "disbursement_date":["2024-01-15","2023-06-10","2024-02-10","2023-11-05"],
        "loan_amount":[500000,200000,300000,1000000],
        "outstanding_amount":[420000,80000,180000,850000],
        "tenure_months":[36,12,24,48],
        "interest_rate":[18.5,20.0,16.0,14.5],
        "emis_paid":[8,10,6,12],
        "dpd":[0,0,30,90],
        "bucket":["Current","Current","SMA-0","SMA-2"],
        "collection_status":["Collected","Collected","Partially Collected","Partially Collected"],
        "bureau_score_at_origination":[720,720,680,750]
    }
    st.download_button("Download sample CSV", pd.DataFrame(sample_data).to_csv(index=False).encode(), "sample_portfolio.csv", "text/csv", use_container_width=True)
    st.markdown("---")
    st.subheader("Step 2 — Required columns")
    st.markdown('<div class="warning-box">All 17 columns must be present. Names must match exactly — spelling, case, and underscores.</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        "Column":["loan_id","customer_id","borrower_name","pan","phone","product","geography","disbursement_date","loan_amount","outstanding_amount","tenure_months","interest_rate","emis_paid","dpd","bucket","collection_status","bureau_score_at_origination"],
        "Type":["Text","Text","Text","Text","Text","Text","Text","Date","Number","Number","Number","Number","Number","Number","Text","Text","Number"],
        "Format":["Unique e.g. LN-1001","Unique per customer e.g. CID-10001","Full name","PAN card number","10-digit mobile","Business Loan/MSME Loan/Equipment Finance/Working Capital/Personal Loan","City","YYYY-MM-DD","Numbers only e.g. 500000","Numbers only e.g. 420000","Months e.g. 36","% e.g. 18.5","Count e.g. 8","0 if current else 30/60/90","Current/SMA-0/SMA-1/SMA-2/NPA","Collected/Partially Collected/Defaulted","300-900 e.g. 720"]
    }), use_container_width=True, hide_index=True, height=580)
    st.markdown("---")
    st.subheader("Step 3 — Key rules")
    c1,c2 = st.columns(2)
    mistakes = [("Same customer_id for all loans of one borrower","CID-10001 for all Mehta Traders loans"),("YYYY-MM-DD date format","2024-01-15 not 15/01/2024"),("Numbers only — no Rs. symbol","500000 not Rs.5,00,000"),("Exact bucket spelling","Current not current or CURRENT"),("No commas in numbers","500000 not 5,00,000"),("All 17 columns required","Even if some values are blank")]
    for i,(title,desc) in enumerate(mistakes):
        with c1 if i%2==0 else c2:
            st.markdown(f'<div class="warning-box"><strong>{title}</strong><br>{desc}</div>', unsafe_allow_html=True)
    st.markdown('<div class="success-box">Ready to upload! Use the Upload button in the sidebar.</div>', unsafe_allow_html=True)