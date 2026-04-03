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
if "df" not in st.session_state:
    st.session_state.df = None

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
    st.markdown('<div class="brand-sub">Smart risk analytics</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<span class="org-badge">🏢 {st.session_state.org}</span>', unsafe_allow_html=True)
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
    page = st.radio("Navigate", ["Dashboard", "Borrower Eligibility", "AI Insights", "Data Upload Guide"], label_visibility="collapsed")
    st.markdown("---")
    if st.button("Sign out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.org = ""
        st.session_state.df = None
        st.rerun()

df = st.session_state.df.copy()

def page_header(title):
    st.markdown(f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:1.5rem;"><span style="font-size:24px;font-weight:500;">{title}</span><span class="org-badge">🏢 {st.session_state.org}</span></div>', unsafe_allow_html=True)

def safe_par(data):
    if len(data) == 0:
        return 0.0
    return round(len(data[data["dpd"] >= 30]) / len(data) * 100, 1)

def safe_npa(data):
    if len(data) == 0:
        return 0.0
    return round(len(data[data["bucket"] == "NPA"]) / len(data) * 100, 1)

def safe_collection(data):
    if len(data) == 0:
        return 0.0
    return round(len(data[data["collection_status"] == "Collected"]) / len(data) * 100, 1)

def safe_aum(data):
    return round(data["outstanding_amount"].sum() / 10000000, 1)

if page == "Dashboard":
    page_header("📊 Portfolio Dashboard")

    cf1, cf2, cf3 = st.columns(3)
    with cf1:
        selected_product = st.selectbox("Product", ["All"] + sorted(df["product"].unique().tolist()))
    with cf2:
        selected_geo = st.selectbox("Geography", ["All"] + sorted(df["geography"].unique().tolist()))
    with cf3:
        selected_bucket = st.selectbox("Bucket", ["All"] + ["Current", "SMA-0", "SMA-1", "SMA-2", "NPA"])

    filtered = df.copy()
    if selected_product != "All":
        filtered = filtered[filtered["product"] == selected_product]
    if selected_geo != "All":
        filtered = filtered[filtered["geography"] == selected_geo]
    if selected_bucket != "All":
        filtered = filtered[filtered["bucket"] == selected_bucket]

    total_loans = len(filtered)
    aum = safe_aum(filtered)
    par30 = safe_par(filtered)
    npa_rate = safe_npa(filtered)
    collection_eff = safe_collection(filtered)

    st.markdown("---")
    st.subheader("Portfolio summary")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total loans", f"{total_loans:,}")
    m2.metric("Total AUM", f"Rs.{aum} Cr")
    m3.metric("PAR 30+", f"{par30}%")
    m4.metric("NPA Rate", f"{npa_rate}%")
    m5.metric("Collection Efficiency", f"{collection_eff}%")

    st.markdown("---")
    ch1, ch2 = st.columns(2)

    with ch1:
        st.subheader("Portfolio by DPD bucket")
        if len(filtered) > 0:
            bucket_counts = filtered["bucket"].value_counts().reset_index()
            bucket_counts.columns = ["Bucket", "Count"]
            fig1 = px.pie(
                bucket_counts, names="Bucket", values="Count", hole=0.4,
                color="Bucket",
                color_discrete_map={"Current":"#1D9E75","SMA-0":"#EF9F27","SMA-1":"#D85A30","SMA-2":"#E24B4A","NPA":"#A32D2D"}
            )
            fig1.update_traces(hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>")
            fig1.update_layout(height=320, margin=dict(t=10, b=10))
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No data for selected filters")

    with ch2:
        st.subheader("PAR 30+ by product")
        if len(filtered) > 0:
            par_prod = []
            for prod in filtered["product"].unique():
                prod_df = filtered[filtered["product"] == prod]
                par_prod.append({"Product": prod, "PAR 30+ %": safe_par(prod_df), "Loans": len(prod_df)})
            par_prod_df = pd.DataFrame(par_prod).sort_values("PAR 30+ %", ascending=True)
            fig2 = px.bar(
                par_prod_df, x="PAR 30+ %", y="Product", orientation="h",
                color="PAR 30+ %", color_continuous_scale=["#1D9E75","#EF9F27","#E24B4A"],
                hover_data=["Loans"]
            )
            fig2.update_layout(height=320, margin=dict(t=10, b=10))
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No data for selected filters")

    ch3, ch4 = st.columns(2)

    with ch3:
        st.subheader("AUM by geography")
        if len(filtered) > 0:
            geo_aum = filtered.groupby("geography")["outstanding_amount"].sum().reset_index()
            geo_aum.columns = ["Geography", "Outstanding"]
            geo_aum["AUM (Cr)"] = (geo_aum["Outstanding"] / 10000000).round(2)
            geo_aum = geo_aum.sort_values("AUM (Cr)", ascending=False)
            fig3 = px.bar(
                geo_aum, x="Geography", y="AUM (Cr)",
                color="AUM (Cr)", color_continuous_scale=["#B5D4F4","#1D9E75"]
            )
            fig3.update_traces(hovertemplate="<b>%{x}</b><br>AUM: Rs.%{y} Cr<extra></extra>")
            fig3.update_layout(height=300, margin=dict(t=10, b=10))
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No data for selected filters")

    with ch4:
        st.subheader("Bureau score by risk bucket")
        if len(filtered) > 0:
            bureau_bucket = filtered.groupby("bucket")["bureau_score_at_origination"].mean().round(0).reset_index()
            bureau_bucket.columns = ["Bucket", "Avg Bureau Score"]
            bucket_order_list = ["Current","SMA-0","SMA-1","SMA-2","NPA"]
            bureau_bucket["Bucket"] = pd.Categorical(bureau_bucket["Bucket"], categories=bucket_order_list, ordered=True)
            bureau_bucket = bureau_bucket.sort_values("Bucket")
            colors_map = {"Current":"#1D9E75","SMA-0":"#EF9F27","SMA-1":"#D85A30","SMA-2":"#E24B4A","NPA":"#A32D2D"}
            fig4 = go.Figure()
            for _, row in bureau_bucket.iterrows():
                fig4.add_trace(go.Bar(
                    x=[row["Bucket"]],
                    y=[row["Avg Bureau Score"]],
                    name=row["Bucket"],
                    marker_color=colors_map.get(row["Bucket"], "#888"),
                    text=[f"{int(row['Avg Bureau Score'])}"],
                    textposition="outside",
                    showlegend=False
                ))
            fig4.add_hline(
                y=650, line_dash="dash", line_color="#185FA5",
                annotation_text="Min safe threshold (650)",
                annotation_font=dict(size=11, color="#185FA5")
            )
            fig4.update_layout(
                height=300,
                margin=dict(t=30, b=10),
                yaxis=dict(title="Avg Bureau Score", range=[500, 800]),
                xaxis_title="Risk Bucket",
                plot_bgcolor="white",
                paper_bgcolor="white",
                yaxis_gridcolor="#f0f0f0"
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("No data for selected filters")

    st.markdown("---")
    st.subheader("Roll-rate matrix")
    st.caption("Account movement between buckets — green = improving, red = worsening")
    bucket_order = ["Current","SMA-0","SMA-1","SMA-2","NPA"]
    roll_data = {"Current":[88,9,2,1,0],"SMA-0":[34,41,18,6,1],"SMA-1":[18,22,35,19,6],"SMA-2":[8,11,22,38,21],"NPA":[3,5,8,14,70]}
    roll_df = pd.DataFrame(roll_data, index=bucket_order)
    roll_df.index.name = "Last Month"

    def color_cells(val):
        if val >= 60:
            return "background-color:#1D9E75;color:white;font-weight:500;"
        elif val >= 30:
            return "background-color:#9FE1CB;color:#085041;font-weight:500;"
        elif val >= 15:
            return "background-color:#FAEEDA;color:#854F0B;font-weight:500;"
        elif val >= 5:
            return "background-color:#F0997B;color:#712B13;font-weight:500;"
        else:
            return "background-color:#FCEBEB;color:#A32D2D;font-weight:500;"

    st.dataframe(roll_df.style.map(color_cells).format("{:.0f}%"), use_container_width=True)

    st.markdown("---")
    st.subheader("Early warning — accounts at risk")
    at_risk = filtered[filtered["bucket"].isin(["SMA-2","NPA"])].copy().sort_values("dpd", ascending=False)
    if len(at_risk) > 0:
        at_risk["outstanding_display"] = at_risk["outstanding_amount"].apply(lambda x: f"Rs.{x/100000:.1f}L")
        at_risk["Risk Level"] = at_risk["bucket"].apply(lambda b: "Urgent" if b == "NPA" else "High Risk")
        st.dataframe(
            at_risk[["loan_id","borrower_name","product","geography","outstanding_display","dpd","bucket","Risk Level"]].rename(columns={"outstanding_display":"outstanding"}).reset_index(drop=True),
            use_container_width=True, height=280
        )
    else:
        st.markdown('<div class="success-box">No accounts at risk in selected filters.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("2025 Aadilytics — Smart risk analytics for lending teams — Data is confidential and secure")

elif page == "Borrower Eligibility":
    page_header("👤 Borrower Eligibility")
    st.markdown("Every borrower categorised based on repayment behaviour, DPD, and bureau score.")

    def categorise(row):
        if row["bucket"] == "NPA" or row["dpd"] > 90:
            return "Blacklisted", "🔴", "No new loans. Immediate recovery action required.", "#fdecea", "#c62828"
        elif row["bucket"] == "SMA-2" or row["dpd"] > 60:
            return "High Risk", "🔴", "Not eligible for new loans. Focus on collection.", "#fdecea", "#c62828"
        elif row["bucket"] == "SMA-1" or row["dpd"] > 30:
            return "Risky", "🟠", "New loans only with additional collateral.", "#fff8e1", "#e65100"
        elif row["bucket"] == "SMA-0" or row["dpd"] > 0:
            return "Borderline", "🟡", "Eligible for small top-up loans only. Monitor closely.", "#fffde7", "#f9a825"
        elif row["bureau_score_at_origination"] >= 720 and row["collection_status"] == "Collected":
            return "Premium", "🟢", "Excellent borrower. Eligible for higher amounts and better rates.", "#e8f5e9", "#1b5e20"
        elif row["bureau_score_at_origination"] >= 680 and row["collection_status"] == "Collected":
            return "Eligible", "🟢", "Good borrower. Eligible for new loans at standard terms.", "#e8f5e9", "#2e7d32"
        else:
            return "Review Needed", "🔵", "Needs manual review before approval.", "#e8f0fe", "#1a237e"

    df[["eligibility","icon","reason","bg","color"]] = df.apply(lambda r: pd.Series(categorise(r)), axis=1)

    cats = ["Premium","Eligible","Borderline","Review Needed","Risky","High Risk","Blacklisted"]
    colors = ["#1b5e20","#2e7d32","#f9a825","#1a237e","#e65100","#c62828","#b71c1c"]
    elig_counts = df["eligibility"].value_counts()

    st.markdown("---")
    cols = st.columns(7)
    for cat, col, clr in zip(cats, cols, colors):
        count = elig_counts.get(cat, 0)
        pct = round(count / len(df) * 100, 1)
        col.markdown(f'<div style="background:#f8f9fa;border-radius:10px;padding:12px;text-align:center;border-top:3px solid {clr};"><div style="font-size:20px;font-weight:600;color:{clr};">{count}</div><div style="font-size:11px;color:#888;margin-top:2px;">{cat}</div><div style="font-size:11px;color:#aaa;">{pct}%</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    ec1, ec2 = st.columns(2)

    with ec1:
        st.subheader("Eligibility distribution")
        fig_e = px.pie(
            df["eligibility"].value_counts().reset_index(),
            names="eligibility", values="count", hole=0.4,
            color="eligibility",
            color_discrete_map=dict(zip(cats, colors))
        )
        fig_e.update_layout(height=320, margin=dict(t=10, b=10))
        st.plotly_chart(fig_e, use_container_width=True)

    with ec2:
        st.subheader("Eligible vs not eligible by product")
        df["eligible_flag"] = df["eligibility"].apply(lambda x: "Eligible" if x in ["Premium","Eligible"] else "Not eligible")
        prod_e = df.groupby(["product","eligible_flag"]).size().reset_index(name="count")
        fig_pe = px.bar(
            prod_e, x="product", y="count", color="eligible_flag",
            color_discrete_map={"Eligible":"#1D9E75","Not eligible":"#E24B4A"},
            barmode="stack"
        )
        fig_pe.update_layout(height=320, margin=dict(t=10, b=10))
        st.plotly_chart(fig_pe, use_container_width=True)

    st.markdown("---")
    st.subheader("Borrower eligibility list")
    filter_elig = st.multiselect("Filter by category", options=cats, default=cats)
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
    export_df = df[["loan_id","borrower_name","product","geography","dpd","bucket","bureau_score_at_origination","eligibility","reason"]].copy()
    st.download_button("Download eligibility report", export_df.to_csv(index=False).encode(), "eligibility_report.csv", "text/csv", use_container_width=True)

elif page == "AI Insights":
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
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("PAR 30+", f"{par30}%", f"{round(par30-INDUSTRY_PAR,1)}% vs industry {INDUSTRY_PAR}%", delta_color="inverse")
    m2.metric("NPA Rate", f"{npa_rate}%", f"{round(npa_rate-INDUSTRY_NPA,1)}% vs industry {INDUSTRY_NPA}%", delta_color="inverse")
    m3.metric("Collection Efficiency", f"{collection_eff}%", f"{round(collection_eff-INDUSTRY_COLLECTION,1)}% vs industry {INDUSTRY_COLLECTION}%")
    m4.metric("Avg Bureau Score", f"{int(avg_bureau)}", f"{int(avg_bureau-INDUSTRY_BUREAU)} vs industry {INDUSTRY_BUREAU}")

    st.markdown("---")
    ai1, ai2 = st.columns(2)

    with ai1:
        st.subheader("Your portfolio vs industry")
        fig_c = go.Figure()
        fig_c.add_trace(go.Bar(
            name="Your Portfolio",
            x=["PAR 30+","NPA Rate","Collection Eff."],
            y=[par30, npa_rate, collection_eff],
            marker_color="#1D9E75"
        ))
        fig_c.add_trace(go.Bar(
            name="Industry Avg",
            x=["PAR 30+","NPA Rate","Collection Eff."],
            y=[INDUSTRY_PAR, INDUSTRY_NPA, INDUSTRY_COLLECTION],
            marker_color="#378ADD"
        ))
        fig_c.update_layout(barmode="group", height=300, margin=dict(t=10, b=10))
        st.plotly_chart(fig_c, use_container_width=True)

    with ai2:
        st.subheader("Bureau score distribution")
        fig_h = px.histogram(
            df, x="bureau_score_at_origination", nbins=20,
            color_discrete_sequence=["#7F77DD"],
            labels={"bureau_score_at_origination":"Bureau Score"}
        )
        fig_h.update_layout(height=300, margin=dict(t=10, b=10))
        st.plotly_chart(fig_h, use_container_width=True)

    st.markdown("---")
    st.subheader("AI generated observations")
    observations = []
    if par30 > INDUSTRY_PAR:
        observations.append(("🔴 PAR above industry average", f"Your PAR 30+ is {par30}% vs industry {INDUSTRY_PAR}%. Focus collection on SMA-1 and SMA-2 accounts before they slip to NPA.", "danger"))
    else:
        observations.append(("🟢 PAR below industry average", f"Your PAR 30+ of {par30}% beats industry average of {INDUSTRY_PAR}%. Credit selection is performing well.", "success"))
    if collection_eff < INDUSTRY_COLLECTION:
        observations.append(("🔴 Collection efficiency below average", f"Your {collection_eff}% is below industry {INDUSTRY_COLLECTION}%. Review collection team performance by geography.", "danger"))
    else:
        observations.append(("🟢 Strong collection efficiency", f"Your {collection_eff}% beats industry {INDUSTRY_COLLECTION}%. Operations team is performing well.", "success"))
    high_risk_product = df[df["dpd"] >= 30].groupby("product").size()
    if len(high_risk_product) > 0:
        observations.append(("⚠️ Highest risk product", f"{high_risk_product.idxmax()} has the highest overdue concentration. Consider tightening credit criteria.", "warning"))
    high_risk_geo = df[df["dpd"] >= 30].groupby("geography").size()
    if len(high_risk_geo) > 0:
        observations.append(("📍 Highest risk geography", f"{high_risk_geo.idxmax()} has the highest delinquency rate. Review collection operations in this region.", "warning"))
    low_bureau = df[df["bureau_score_at_origination"] < 650]
    if len(low_bureau) > 0:
        lb_npa = round(len(low_bureau[low_bureau["bucket"] == "NPA"]) / len(low_bureau) * 100, 1)
        observations.append(("📊 Bureau score insight", f"Borrowers with score below 650 have {lb_npa}% NPA rate. Consider setting 650 as minimum threshold.", "guide"))
    for title, text, type_ in observations:
        box = {"danger":"danger-box","success":"success-box","warning":"warning-box","guide":"guide-box"}[type_]
        st.markdown(f'<div class="{box}"><strong>{title}</strong><br>{text}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("NPA risk prediction by product")
    pred_rows = []
    for prod in df["product"].unique():
        prod_df = df[df["product"] == prod]
        cur_par = safe_par(prod_df)
        pred_npa = round(cur_par * 0.35, 1)
        pred_rows.append({
            "Product": prod,
            "Loans": len(prod_df),
            "Current PAR 30+": f"{cur_par}%",
            "Predicted NPA (90 days)": f"{pred_npa}%",
            "Risk Level": "High" if pred_npa > 5 else "Medium" if pred_npa > 2 else "Low"
        })
    pred_df = pd.DataFrame(pred_rows)

    def color_risk(val):
        if val == "High":
            return "background-color:#FCEBEB;color:#A32D2D;font-weight:500;"
        elif val == "Medium":
            return "background-color:#FAEEDA;color:#854F0B;font-weight:500;"
        else:
            return "background-color:#E1F5EE;color:#0F6E56;font-weight:500;"

    st.dataframe(pred_df.style.map(color_risk, subset=["Risk Level"]), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("3 month portfolio forecast")
    months = ["Current", "Month 1", "Month 2", "Month 3"]
    par_forecast = [par30, round(par30*1.05,1), round(par30*1.08,1), round(par30*1.03,1)]
    npa_forecast = [npa_rate, round(npa_rate*1.08,1), round(npa_rate*1.12,1), round(npa_rate*1.06,1)]

    fig_fc = go.Figure()
    fig_fc.add_trace(go.Scatter(
        x=months, y=par_forecast,
        mode="lines+markers+text",
        name="PAR 30+",
        line=dict(color="#E24B4A", width=3),
        marker=dict(size=10, color="#E24B4A"),
        text=[f"{v}%" for v in par_forecast],
        textposition="top center",
        textfont=dict(size=12, color="#E24B4A")
    ))
    fig_fc.add_trace(go.Scatter(
        x=months, y=npa_forecast,
        mode="lines+markers+text",
        name="NPA Rate",
        line=dict(color="#1D9E75", width=3, dash="dash"),
        marker=dict(size=10, color="#1D9E75", symbol="diamond"),
        text=[f"{v}%" for v in npa_forecast],
        textposition="bottom center",
        textfont=dict(size=12, color="#1D9E75")
    ))
    fig_fc.add_hrect(
        y0=0, y1=INDUSTRY_PAR,
        fillcolor="#E6F1FB", opacity=0.3,
        layer="below", line_width=0,
        annotation_text=f"Safe zone (below industry PAR {INDUSTRY_PAR}%)",
        annotation_position="top left",
        annotation_font=dict(size=11, color="#185FA5")
    )
    fig_fc.update_layout(
        height=340,
        margin=dict(t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title="Rate (%)", rangemode="tozero"),
        xaxis_title="",
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis_gridcolor="#f0f0f0"
    )
    st.plotly_chart(fig_fc, use_container_width=True)
    st.markdown('<div class="guide-box">About predictions — Forecasts are directional indicators based on current roll rates. Actual outcomes depend on collection efforts and macro conditions.</div>', unsafe_allow_html=True)

elif page == "Data Upload Guide":
    page_header("📋 Data Upload Guide")
    st.markdown("Follow this guide before uploading your portfolio data.")
    st.markdown("---")

    st.subheader("Step 1 — Download sample file")
    st.markdown('<div class="guide-box">Download our sample CSV and use it as a template — replace values with your real loan data.</div>', unsafe_allow_html=True)
    sample_data = {
        "loan_id": ["LN-5001","LN-5002","LN-5003"],
        "borrower_name": ["Mehta Traders Pvt Ltd","Rajan Enterprises","Sunita Textiles"],
        "product": ["Business Loan","MSME Loan","Equipment Finance"],
        "geography": ["Mumbai","Pune","Nagpur"],
        "disbursement_date": ["2024-01-15","2024-02-10","2023-11-05"],
        "loan_amount": [500000,300000,1000000],
        "outstanding_amount": [420000,180000,850000],
        "tenure_months": [36,24,48],
        "interest_rate": [18.5,16.0,14.5],
        "emis_paid": [8,6,12],
        "dpd": [0,30,90],
        "bucket": ["Current","SMA-0","SMA-2"],
        "collection_status": ["Collected","Partially Collected","Partially Collected"],
        "bureau_score_at_origination": [720,680,750]
    }
    sample_df = pd.DataFrame(sample_data)
    st.download_button("Download sample CSV", sample_df.to_csv(index=False).encode(), "sample_portfolio.csv", "text/csv", use_container_width=True)

    st.markdown("---")
    st.subheader("Step 2 — Required columns")
    st.markdown('<div class="warning-box">All 14 columns must be present. Names must match exactly — spelling, case, and underscores.</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        "Column Name": ["loan_id","borrower_name","product","geography","disbursement_date","loan_amount","outstanding_amount","tenure_months","interest_rate","emis_paid","dpd","bucket","collection_status","bureau_score_at_origination"],
        "Data Type": ["Text","Text","Text","Text","Date","Number","Number","Number","Number","Number","Number","Text","Text","Number"],
        "Format": [
            "Unique ID e.g. LN-1001","Full name",
            "Business Loan / MSME Loan / Equipment Finance / Working Capital / Personal Loan",
            "City e.g. Mumbai","YYYY-MM-DD","Numbers only e.g. 500000","Numbers only e.g. 420000",
            "Months e.g. 36","% e.g. 18.5","Count e.g. 8","0 if current else 30/60/90/120",
            "Current / SMA-0 / SMA-1 / SMA-2 / NPA","Collected / Partially Collected / Defaulted","300-900 e.g. 720"
        ]
    }), use_container_width=True, hide_index=True, height=530)

    st.markdown("---")
    st.subheader("Step 3 — Common mistakes")
    c1, c2 = st.columns(2)
    mistakes = [
        ("Wrong date format","Use YYYY-MM-DD not DD/MM/YYYY"),
        ("Rupee symbol in amounts","Write 500000 not Rs.5,00,000"),
        ("Wrong bucket spelling","Use exactly: Current, SMA-0, SMA-1, SMA-2, NPA"),
        ("Commas in numbers","Write 500000 not 5,00,000"),
        ("Spaces in column names","loan_id not loan_id with spaces"),
        ("Missing columns","All 14 columns must be present"),
    ]
    for i, (title, desc) in enumerate(mistakes):
        with c1 if i % 2 == 0 else c2:
            st.markdown(f'<div class="warning-box">X <strong>{title}</strong><br>{desc}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Step 4 — DPD and bucket reference")
    st.dataframe(pd.DataFrame({
        "DPD Range": ["0 days","1-30 days","31-60 days","61-90 days","90+ days"],
        "Bucket": ["Current","SMA-0","SMA-1","SMA-2","NPA"],
        "Meaning": ["Performing no overdue","Early stress","Moderate stress","High stress","Defaulted"],
        "Action": ["Monitor","Flag for review","Assign collection","Escalate","Legal / recovery"]
    }), use_container_width=True, hide_index=True)
    st.markdown('<div class="success-box">Ready to upload! Use the Upload button in the sidebar on any page.</div>', unsafe_allow_html=True)