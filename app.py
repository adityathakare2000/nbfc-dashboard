import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import bcrypt
import os
import json
from datetime import date, datetime
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Aadilytics", layout="wide", page_icon="🔷", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #fafafa;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Main container */
.main .block-container {
    padding: 2rem 2.5rem;
    max-width: 1400px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #f0f0f0 !important;
    width: 240px !important;
}
section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem;
}
section[data-testid="stSidebar"] * {
    color: #1a1a2e !important;
}
section[data-testid="stSidebar"] .stRadio label {
    font-size: 14px !important;
    color: #444 !important;
    padding: 6px 10px;
    border-radius: 8px;
    cursor: pointer;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: #f5f5f5;
}

/* Metrics */
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #f0f0f0;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
div[data-testid="stMetricValue"] {
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #1a1a2e !important;
}
div[data-testid="stMetricLabel"] {
    font-size: 12px !important;
    color: #888 !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
div[data-testid="stMetricDelta"] {
    font-size: 12px !important;
}

/* Buttons */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 0.6rem 1.5rem !important;
    border: 1px solid #e8e8e8 !important;
    transition: all 0.15s ease !important;
}
.stButton > button[kind="primary"] {
    background: #1a1a2e !important;
    color: white !important;
    border: none !important;
}
.stButton > button[kind="primary"]:hover {
    background: #2d2d4e !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(26,26,46,0.2) !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: #f5f5f5 !important;
    border-color: #d0d0d0 !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stDateInput > div > div > input {
    border-radius: 10px !important;
    border: 1px solid #e8e8e8 !important;
    font-size: 14px !important;
    background: #ffffff !important;
}
.stTextInput > div > div > input:focus {
    border-color: #1a1a2e !important;
    box-shadow: 0 0 0 3px rgba(26,26,46,0.08) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #f5f5f5;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #666 !important;
    padding: 8px 20px !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #1a1a2e !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1) !important;
}

/* Dataframe */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden;
    border: 1px solid #f0f0f0 !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #fafafa !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}

/* Divider */
hr { border-color: #f0f0f0 !important; }

/* Cards */
.aa-card {
    background: #ffffff;
    border: 1px solid #f0f0f0;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.aa-section-label {
    font-size: 11px;
    font-weight: 600;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 12px;
}
.aa-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #f5f5f5;
    color: #444;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}
.aa-badge-blue {
    background: #eff6ff;
    color: #1d4ed8;
}
.aa-badge-green {
    background: #f0fdf4;
    color: #16a34a;
}
.aa-badge-red {
    background: #fef2f2;
    color: #dc2626;
}
.aa-badge-amber {
    background: #fffbeb;
    color: #d97706;
}
.aa-badge-purple {
    background: #faf5ff;
    color: #7c3aed;
}

/* Alert boxes */
.aa-alert {
    padding: 14px 18px;
    border-radius: 10px;
    font-size: 14px;
    margin-bottom: 12px;
    line-height: 1.6;
}
.aa-alert-info { background: #eff6ff; border-left: 4px solid #3b82f6; color: #1e3a5f; }
.aa-alert-success { background: #f0fdf4; border-left: 4px solid #22c55e; color: #14532d; }
.aa-alert-warning { background: #fffbeb; border-left: 4px solid #f59e0b; color: #78350f; }
.aa-alert-danger { background: #fef2f2; border-left: 4px solid #ef4444; color: #7f1d1d; }

/* Page header */
.aa-page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #f0f0f0;
}
.aa-page-title {
    font-size: 24px;
    font-weight: 700;
    color: #1a1a2e;
    letter-spacing: -0.3px;
}
.aa-page-sub {
    font-size: 13px;
    color: #888;
    margin-top: 2px;
}

/* Login page */
.aa-login-card {
    background: #ffffff;
    border: 1px solid #f0f0f0;
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}
.aa-logo-text {
    font-size: 28px;
    font-weight: 800;
    color: #1a1a2e;
    letter-spacing: -0.5px;
}
.aa-logo-dot {
    color: #3b82f6;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #fafafa; }
::-webkit-scrollbar-thumb { background: #e0e0e0; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #c0c0c0; }

/* Upload button */
.stFileUploader > div {
    border-radius: 10px !important;
    border: 1.5px dashed #e0e0e0 !important;
    background: #fafafa !important;
}
</style>
""", unsafe_allow_html=True)

for key in ["logged_in","user_id","user_email","nbfc_name","role","df"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "logged_in" else None

def log_activity(user_id, action, detail=""):
    try:
        supabase.table("activity_log").insert({"user_id": user_id, "action": action, "detail": detail}).execute()
    except:
        pass

def save_portfolio(user_id, filename, df):
    try:
        data_json = df.to_json(orient="records")
        existing = supabase.table("portfolio_data").select("id").eq("user_id", user_id).execute()
        if existing.data:
            supabase.table("portfolio_data").update({"filename": filename, "data": data_json, "row_count": len(df), "uploaded_at": datetime.now().isoformat()}).eq("user_id", user_id).execute()
        else:
            supabase.table("portfolio_data").insert({"user_id": user_id, "filename": filename, "data": data_json, "row_count": len(df)}).execute()
        return True
    except Exception as e:
        return False

def load_portfolio(user_id):
    try:
        result = supabase.table("portfolio_data").select("*").eq("user_id", user_id).execute()
        if result.data:
            record = result.data[0]
            return pd.DataFrame(json.loads(record["data"])), record["filename"], record["uploaded_at"]
        return None, None, None
    except:
        return None, None, None

def safe_par(d):
    if len(d) == 0: return 0.0
    return round(len(d[d["dpd"] >= 30]) / len(d) * 100, 1)

def safe_npa(d):
    if len(d) == 0: return 0.0
    return round(len(d[d["bucket"] == "NPA"]) / len(d) * 100, 1)

def safe_collection(d):
    if len(d) == 0: return 0.0
    return round(len(d[d["collection_status"] == "Collected"]) / len(d) * 100, 1)

def safe_aum(d):
    return round(d["outstanding_amount"].sum() / 10000000, 1)

def calc_emi(p, r, n):
    if n == 0 or r == 0: return 0
    r = r / 100 / 12
    return round(p * r * (1+r)**n / ((1+r)**n - 1), 0)

BUCKET_ORDER = ["Current","SMA-0","SMA-1","SMA-2","NPA"]
COLOR_MAP = {"Current":"#10b981","SMA-0":"#f59e0b","SMA-1":"#f97316","SMA-2":"#ef4444","NPA":"#991b1b"}
BG_MAP = {"Current":"#f0fdf4","SMA-0":"#fffbeb","SMA-1":"#fff7ed","SMA-2":"#fef2f2","NPA":"#fef2f2"}

def bclr(b): return COLOR_MAP.get(b,"#888")
def bbg(b): return BG_MAP.get(b,"#f9f9f9")

def page_header(title, subtitle=""):
    nbfc = st.session_state.nbfc_name or ""
    sub = subtitle or f"{nbfc}"
    st.markdown(f"""
    <div class="aa-page-header">
        <div>
            <div class="aa-page-title">{title}</div>
            <div class="aa-page-sub">{sub}</div>
        </div>
        <span class="aa-badge aa-badge-blue">🏢 {nbfc}</span>
    </div>
    """, unsafe_allow_html=True)

def alert(msg, type_="info"):
    st.markdown(f'<div class="aa-alert aa-alert-{type_}">{msg}</div>', unsafe_allow_html=True)

def chart_layout(fig, height=320):
    fig.update_layout(
        height=height,
        margin=dict(t=20,b=10,l=10,r=10),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Inter, sans-serif", size=12, color="#444"),
        yaxis_gridcolor="#f0f0f0",
        xaxis_gridcolor="#f0f0f0",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=12)),
    )
    return fig

if not st.session_state.logged_in:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.1, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center;margin-bottom:2.5rem;">
            <div class="aa-logo-text">Aadily<span class="aa-logo-dot">.</span>tics</div>
            <div style="font-size:14px;color:#888;margin-top:8px;font-weight:400;">Credit risk intelligence for lending teams</div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Sign in", "Create account"])

        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="you@nbfc.com", key="li_email", label_visibility="collapsed")
            st.markdown('<div style="font-size:12px;color:#888;margin:-8px 0 8px 2px;">Email address</div>', unsafe_allow_html=True)
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="li_pass", label_visibility="collapsed")
            st.markdown('<div style="font-size:12px;color:#888;margin:-8px 0 16px 2px;">Password</div>', unsafe_allow_html=True)

            if st.button("Sign in →", use_container_width=True, type="primary", key="li_btn"):
                if not email or not password:
                    alert("Please enter your email and password.", "warning")
                else:
                    try:
                        result = supabase.table("users").select("*").eq("email", email.strip().lower()).execute()
                        if not result.data:
                            alert("No account found with this email.", "danger")
                        else:
                            user = result.data[0]
                            if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
                                alert("Incorrect password. Please try again.", "danger")
                            elif user["status"] == "pending":
                                alert("⏳ Your account is pending approval. The Aadilytics team will review your request and notify you.", "warning")
                            elif user["status"] == "rejected":
                                alert("Your account access has been declined. Contact support for more information.", "danger")
                            elif user["valid_until"] and date.fromisoformat(str(user["valid_until"])) < date.today():
                                alert(f"Your subscription expired on {user['valid_until']}. Please contact Aadilytics to renew your plan.", "danger")
                            else:
                                st.session_state.logged_in = True
                                st.session_state.user_id = user["id"]
                                st.session_state.user_email = user["email"]
                                st.session_state.nbfc_name = user["nbfc_name"]
                                st.session_state.role = user["role"]
                                log_activity(user["id"], "login", email)
                                st.rerun()
                    except Exception as e:
                        alert(f"Login error. Please try again.", "danger")

            st.markdown("""
            <div style="text-align:center;margin-top:1.5rem;font-size:13px;color:#888;">
                Demo: demo@nbfc.com / demo123
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            alert("After creating your account, the Aadilytics team will review and activate your access. You will be notified once approved.", "info")
            su_nbfc = st.text_input("Organisation name", placeholder="e.g. Sunrise NBFC Pvt Ltd", key="su_nbfc")
            su_email = st.text_input("Work email", placeholder="you@nbfc.com", key="su_email")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                su_pass = st.text_input("Password", type="password", placeholder="Min 8 characters", key="su_pass")
            with col_p2:
                su_conf = st.text_input("Confirm password", type="password", placeholder="Re-enter", key="su_conf")

            if st.button("Create account →", use_container_width=True, type="primary", key="su_btn"):
                if not su_nbfc or not su_email or not su_pass or not su_conf:
                    alert("Please fill in all fields.", "warning")
                elif len(su_pass) < 8:
                    alert("Password must be at least 8 characters.", "warning")
                elif su_pass != su_conf:
                    alert("Passwords do not match.", "warning")
                elif "@" not in su_email or "." not in su_email:
                    alert("Please enter a valid email address.", "warning")
                else:
                    try:
                        existing = supabase.table("users").select("id").eq("email", su_email.strip().lower()).execute()
                        if existing.data:
                            alert("An account with this email already exists.", "danger")
                        else:
                            hashed = bcrypt.hashpw(su_pass.encode(), bcrypt.gensalt()).decode()
                            supabase.table("users").insert({
                                "email": su_email.strip().lower(),
                                "password_hash": hashed,
                                "nbfc_name": su_nbfc.strip(),
                                "role": "user",
                                "status": "pending",
                                "valid_until": None
                            }).execute()
                            alert("✅ Account created! Our team will review your request and get in touch with you shortly.", "success")
                    except Exception as e:
                        alert(f"Signup error. Please try again.", "danger")
    st.stop()

with st.sidebar:
    st.markdown(f"""
    <div style="padding:0 0 1rem 0;">
        <div style="font-size:18px;font-weight:800;color:#1a1a2e;letter-spacing:-0.3px;">Aadily<span style="color:#3b82f6;">.</span>tics</div>
        <div style="font-size:11px;color:#999;margin-top:2px;">Credit risk intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#f5f5f5;border-radius:10px;padding:10px 12px;margin-bottom:1rem;">
        <div style="font-size:11px;color:#999;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;">Organisation</div>
        <div style="font-size:13px;font-weight:600;color:#1a1a2e;margin-top:2px;">{st.session_state.nbfc_name}</div>
        <div style="font-size:11px;color:#888;margin-top:1px;">{st.session_state.user_email}</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload portfolio CSV", type=["csv"], label_visibility="collapsed")
    st.markdown('<div style="font-size:11px;color:#999;margin:-8px 0 12px 0;">Upload CSV portfolio file</div>', unsafe_allow_html=True)

    if uploaded_file:
        new_df = pd.read_csv(uploaded_file)
        st.session_state.df = new_df
        if save_portfolio(st.session_state.user_id, uploaded_file.name, new_df):
            st.success(f"{len(new_df):,} records saved")
        else:
            st.warning("Uploaded but not saved to database")
    elif st.session_state.df is None:
        saved_df, saved_filename, saved_at = load_portfolio(st.session_state.user_id)
        if saved_df is not None:
            st.session_state.df = saved_df
            saved_date = saved_at[:10] if saved_at else ""
            st.markdown(f'<div style="font-size:11px;color:#10b981;margin-bottom:8px;">✓ {saved_filename} · {saved_date}</div>', unsafe_allow_html=True)
        else:
            if st.session_state.role == "admin":
                try:
                    st.session_state.df = pd.read_csv("loan_portfolio.csv")
                except:
                    st.session_state.df = pd.DataFrame()
            else:
                st.session_state.df = pd.DataFrame()

    st.markdown('<div style="height:1px;background:#f0f0f0;margin:12px 0;"></div>', unsafe_allow_html=True)

    pages = ["📊 Dashboard","🔍 Borrower Analysis","✅ Pre-Disbursal","👤 Eligibility","🤖 AI Insights","📋 Upload Guide"]
    if st.session_state.role == "admin":
        pages.append("🔧 Admin")

    page = st.radio("", pages, label_visibility="collapsed")

    st.markdown('<div style="height:1px;background:#f0f0f0;margin:12px 0;"></div>', unsafe_allow_html=True)
    if st.button("Sign out", use_container_width=True, key="signout"):
        log_activity(st.session_state.user_id, "logout", "")
        for key in ["logged_in","user_id","user_email","nbfc_name","role","df"]:
            st.session_state[key] = False if key == "logged_in" else None
        st.rerun()

df = st.session_state.df if st.session_state.df is not None else pd.DataFrame()
has_data = len(df) > 0
has_cid = "customer_id" in df.columns if has_data else False
has_pan = "pan" in df.columns if has_data else False
has_phone = "phone" in df.columns if has_data else False

if not has_data and page not in ["🔧 Admin","📋 Upload Guide"]:
    page_header(page, "No data loaded")
    alert("<strong>No portfolio data found.</strong> Please upload your CSV file using the sidebar to view analytics.", "warning")
    alert("Go to <strong>📋 Upload Guide</strong> for the required file format and a sample CSV to download.", "info")
    st.stop()

if page == "📊 Dashboard":
    page_header("Portfolio Dashboard", f"{len(df):,} loan records · {df['customer_id'].nunique() if has_cid else df['borrower_name'].nunique():,} customers")

    f1, f2, f3 = st.columns(3)
    with f1: sel_product = st.selectbox("Product", ["All"] + sorted(df["product"].unique().tolist()), label_visibility="visible")
    with f2: sel_geo = st.selectbox("Geography", ["All"] + sorted(df["geography"].unique().tolist()))
    with f3: sel_bucket = st.selectbox("Bucket", ["All"] + BUCKET_ORDER)

    filt = df.copy()
    if sel_product != "All": filt = filt[filt["product"] == sel_product]
    if sel_geo != "All": filt = filt[filt["geography"] == sel_geo]
    if sel_bucket != "All": filt = filt[filt["bucket"] == sel_bucket]

    uniq_cust = filt["customer_id"].nunique() if has_cid else filt["borrower_name"].nunique()

    st.markdown("<br>", unsafe_allow_html=True)
    m1,m2,m3,m4,m5,m6 = st.columns(6)
    m1.metric("Customers", f"{uniq_cust:,}")
    m2.metric("Loan accounts", f"{len(filt):,}")
    m3.metric("Total AUM", f"₹{safe_aum(filt)} Cr")
    m4.metric("PAR 30+", f"{safe_par(filt)}%")
    m5.metric("NPA Rate", f"{safe_npa(filt)}%")
    m6.metric("Collection Eff.", f"{safe_collection(filt)}%")

    st.markdown("<br>", unsafe_allow_html=True)
    ch1, ch2 = st.columns(2)
    with ch1:
        st.markdown('<div class="aa-section-label">Portfolio by DPD bucket</div>', unsafe_allow_html=True)
        bc = filt["bucket"].value_counts().reset_index()
        bc.columns = ["Bucket","Count"]
        fig1 = px.pie(bc, names="Bucket", values="Count", hole=0.55, color="Bucket", color_discrete_map=COLOR_MAP)
        fig1.update_traces(textposition="outside", textinfo="percent+label", textfont_size=12)
        fig1.update_layout(**chart_layout(fig1, 300).layout.to_plotly_json())
        st.plotly_chart(fig1, use_container_width=True)
    with ch2:
        st.markdown('<div class="aa-section-label">PAR 30+ by product</div>', unsafe_allow_html=True)
        pp = [{"Product":p,"PAR 30+%":safe_par(filt[filt["product"]==p])} for p in filt["product"].unique()]
        pp_df = pd.DataFrame(pp).sort_values("PAR 30+%", ascending=True)
        fig2 = px.bar(pp_df, x="PAR 30+%", y="Product", orientation="h", color="PAR 30+%", color_continuous_scale=["#10b981","#f59e0b","#ef4444"], text="PAR 30+%")
        fig2.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig2.update_layout(**chart_layout(fig2, 300).layout.to_plotly_json())
        st.plotly_chart(fig2, use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        st.markdown('<div class="aa-section-label">AUM by geography (₹ Cr)</div>', unsafe_allow_html=True)
        ga = filt.groupby("geography")["outstanding_amount"].sum().reset_index()
        ga.columns = ["Geography","Outstanding"]
        ga["AUM"] = (ga["Outstanding"]/10000000).round(2)
        ga = ga.sort_values("AUM", ascending=True)
        fig3 = px.bar(ga, x="AUM", y="Geography", orientation="h", color="AUM", color_continuous_scale=["#bfdbfe","#1d4ed8"], text="AUM")
        fig3.update_traces(texttemplate="₹%{text}Cr", textposition="outside")
        fig3.update_layout(**chart_layout(fig3, 300).layout.to_plotly_json())
        st.plotly_chart(fig3, use_container_width=True)
    with ch4:
        st.markdown('<div class="aa-section-label">Avg bureau score by risk bucket</div>', unsafe_allow_html=True)
        bb = filt.groupby("bucket")["bureau_score_at_origination"].mean().round(0).reset_index()
        bb.columns = ["Bucket","Score"]
        bb["Bucket"] = pd.Categorical(bb["Bucket"], categories=BUCKET_ORDER, ordered=True)
        bb = bb.sort_values("Bucket")
        fig4 = go.Figure()
        for _, row in bb.iterrows():
            fig4.add_trace(go.Bar(x=[row["Bucket"]], y=[row["Score"]], name=row["Bucket"], marker_color=COLOR_MAP.get(row["Bucket"],"#888"), text=[f"{int(row['Score'])}"], textposition="outside", showlegend=False))
        fig4.add_hline(y=650, line_dash="dash", line_color="#3b82f6", annotation_text="Min: 650", annotation_font=dict(size=11, color="#3b82f6"))
        fig4.update_layout(**chart_layout(fig4, 300).layout.to_plotly_json())
        fig4.update_layout(yaxis=dict(range=[500,820], title="Avg Bureau Score"), plot_bgcolor="#ffffff", paper_bgcolor="#ffffff")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="aa-section-label">Roll-rate matrix — dynamic from your portfolio</div>', unsafe_allow_html=True)
    st.caption("Shows % of accounts that moved between DPD buckets. Calculated from your uploaded data.")

    if "disbursement_date" in filt.columns:
        filt["disbursement_date"] = pd.to_datetime(filt["disbursement_date"], errors="coerce")
        filt["months_since"] = ((pd.Timestamp.now() - filt["disbursement_date"]).dt.days / 30).fillna(0).astype(int)

        def assign_prev_bucket(row):
            prev_dpd = max(0, row["dpd"] - 30)
            if prev_dpd == 0: return "Current"
            elif prev_dpd <= 30: return "SMA-0"
            elif prev_dpd <= 60: return "SMA-1"
            elif prev_dpd <= 90: return "SMA-2"
            else: return "NPA"

        filt["prev_bucket"] = filt.apply(assign_prev_bucket, axis=1)
        roll_counts = filt.groupby(["prev_bucket","bucket"]).size().reset_index(name="count")
        roll_totals = filt.groupby("prev_bucket").size().reset_index(name="total")
        roll_merged = roll_counts.merge(roll_totals, on="prev_bucket")
        roll_merged["pct"] = (roll_merged["count"] / roll_merged["total"] * 100).round(1)

        roll_matrix = pd.DataFrame(index=BUCKET_ORDER, columns=BUCKET_ORDER, data=0.0)
        for _, row in roll_merged.iterrows():
            if row["prev_bucket"] in BUCKET_ORDER and row["bucket"] in BUCKET_ORDER:
                roll_matrix.loc[row["prev_bucket"], row["bucket"]] = row["pct"]

        roll_matrix.index.name = "From → To"
    else:
        roll_matrix = pd.DataFrame({"Current":[88,9,2,1,0],"SMA-0":[34,41,18,6,1],"SMA-1":[18,22,35,19,6],"SMA-2":[8,11,22,38,21],"NPA":[3,5,8,14,70]}, index=BUCKET_ORDER)
        roll_matrix.index.name = "From → To"

    def color_roll(val):
        try:
            v = float(val)
        except:
            return ""
        if v >= 60: return "background-color:#dcfce7;color:#14532d;font-weight:600;"
        elif v >= 30: return "background-color:#bbf7d0;color:#166534;font-weight:600;"
        elif v >= 15: return "background-color:#fef9c3;color:#713f12;font-weight:600;"
        elif v >= 5: return "background-color:#fed7aa;color:#9a3412;font-weight:600;"
        else: return "background-color:#fee2e2;color:#7f1d1d;font-weight:600;"

    st.dataframe(roll_matrix.style.map(color_roll).format("{:.1f}%"), use_container_width=True)
    st.caption("Rows = last month bucket · Columns = this month bucket · Estimated from DPD movement in your portfolio")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="aa-section-label">Early warning — accounts requiring attention</div>', unsafe_allow_html=True)
    at_risk = filt[filt["bucket"].isin(["SMA-2","NPA"])].copy().sort_values("dpd", ascending=False)
    if len(at_risk) > 0:
        at_risk["outstanding_fmt"] = at_risk["outstanding_amount"].apply(lambda x: f"₹{x/100000:.1f}L")
        at_risk["Risk"] = at_risk["bucket"].apply(lambda b: "🔴 Urgent" if b == "NPA" else "🟠 High Risk")
        show_cols = ["loan_id","borrower_name","product","geography","outstanding_fmt","dpd","bucket","Risk"]
        if has_cid: show_cols = ["customer_id"] + show_cols
        def color_risk_col(val):
            if "Urgent" in str(val): return "background-color:#fef2f2;color:#991b1b;font-weight:600;"
            elif "High" in str(val): return "background-color:#fff7ed;color:#9a3412;font-weight:600;"
            return ""
        def color_bkt_col(val):
            return {"Current":"background-color:#f0fdf4","SMA-0":"background-color:#fffbeb","SMA-1":"background-color:#fff7ed","SMA-2":"background-color:#fef2f2","NPA":"background-color:#fef2f2"}.get(val,"")
        display_risk = at_risk[show_cols].rename(columns={"outstanding_fmt":"outstanding"}).reset_index(drop=True)
        st.dataframe(display_risk.style.map(color_risk_col, subset=["Risk"]).map(color_bkt_col, subset=["bucket"]), use_container_width=True, height=280)
    else:
        alert("✅ No accounts at risk in the selected filters.", "success")

elif page == "🔍 Borrower Analysis":
    page_header("Borrower Analysis", "Search by name, customer ID, PAN or phone")

    sc1, sc2, sc3, sc4 = st.columns([2,2,1,1])
    with sc1: search_q = st.text_input("Search", placeholder="Name / CID / PAN / Phone", label_visibility="collapsed")
    with sc2: f_product = st.selectbox("Product", ["All"] + sorted(df["product"].unique().tolist()))
    with sc3: f_bucket = st.selectbox("Bucket", ["All"] + BUCKET_ORDER)
    with sc4: f_geo = st.selectbox("Geography", ["All"] + sorted(df["geography"].unique().tolist()))

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
    unique_custs = sdf[group_col].unique()
    st.markdown(f'<div style="font-size:13px;color:#888;margin-bottom:1rem;">{len(sdf):,} loan accounts · {len(unique_custs):,} customers</div>', unsafe_allow_html=True)

    if len(sdf) == 0:
        alert("No results found. Try searching by name, customer ID, PAN, or phone.", "warning")
    elif len(unique_custs) <= 3:
        for cid in unique_custs:
            c_loans = sdf[sdf[group_col] == cid].copy()
            bname = c_loans["borrower_name"].iloc[0]
            num_loans = len(c_loans)
            total_out = c_loans["outstanding_amount"].sum()
            total_loan = c_loans["loan_amount"].sum()
            total_repaid = total_loan - total_out
            max_dpd = int(c_loans["dpd"].max())
            avg_bureau = int(c_loans["bureau_score_at_origination"].mean())
            worst_bucket = c_loans.sort_values("dpd", ascending=False).iloc[0]["bucket"]
            active = len(c_loans[c_loans["bucket"] != "NPA"])
            npa_count = len(c_loans[c_loans["bucket"] == "NPA"])
            wclr = bclr(worst_bucket)
            wbg = bbg(worst_bucket)
            pan_val = c_loans["pan"].iloc[0] if has_pan else "N/A"
            phone_val = str(c_loans["phone"].iloc[0]) if has_phone else "N/A"

            st.markdown(f"""
            <div style="background:{wbg};border-radius:16px;padding:20px 24px;margin-bottom:16px;border-left:4px solid {wclr};">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
                    <div>
                        <div style="font-size:18px;font-weight:700;color:#1a1a2e;">{bname}</div>
                        <div style="font-size:13px;color:#666;margin-top:6px;display:flex;gap:16px;flex-wrap:wrap;">
                            <span>🪪 {cid}</span><span>📋 {pan_val}</span><span>📱 {phone_val}</span>
                        </div>
                        <div style="font-size:12px;color:#888;margin-top:4px;">{num_loans} account{'s' if num_loans>1 else ''} with {st.session_state.nbfc_name}</div>
                    </div>
                    <div style="background:{wclr};color:white;padding:5px 14px;border-radius:20px;font-size:12px;font-weight:600;">Worst: {worst_bucket}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            km1,km2,km3,km4,km5,km6,km7 = st.columns(7)
            km1.metric("Accounts", num_loans)
            km2.metric("Active", active)
            km3.metric("NPA", npa_count)
            km4.metric("Outstanding", f"₹{total_out/100000:.1f}L")
            km5.metric("Repaid", f"₹{total_repaid/100000:.1f}L")
            km6.metric("Max DPD", f"{max_dpd}d")
            km7.metric("Bureau", avg_bureau)
            st.markdown("<br>", unsafe_allow_html=True)

            for idx, (_, loan) in enumerate(c_loans.iterrows()):
                dpd = int(loan["dpd"])
                bucket = loan["bucket"]
                loan_amt = loan["loan_amount"]
                outstanding = loan["outstanding_amount"]
                repaid = loan_amt - outstanding
                repaid_pct = round(repaid/loan_amt*100,1) if loan_amt > 0 else 0
                tenure = int(loan["tenure_months"])
                emis_paid = int(loan["emis_paid"])
                emis_rem = max(tenure-emis_paid, 0)
                emi_amt = calc_emi(loan_amt, loan["interest_rate"], tenure)
                lclr = bclr(bucket)
                lbg = bbg(bucket)

                with st.expander(f"  {loan['loan_id']} · {loan['product']} · {bucket} · DPD {dpd}", expanded=(idx==0)):
                    st.markdown(f'<div style="background:{lbg};border-radius:8px;padding:10px 14px;margin-bottom:12px;border-left:3px solid {lclr};font-size:13px;"><span style="color:{lclr};font-weight:600;">{bucket}</span><span style="color:#666;margin-left:12px;">{loan["product"]} · {loan["geography"]} · {loan["disbursement_date"]}</span></div>', unsafe_allow_html=True)

                    a1,a2,a3,a4,a5,a6 = st.columns(6)
                    a1.metric("Loan", f"₹{loan_amt/100000:.1f}L")
                    a2.metric("Outstanding", f"₹{outstanding/100000:.1f}L")
                    a3.metric("Repaid", f"₹{repaid/100000:.1f}L ({repaid_pct}%)")
                    a4.metric("EMI/mo", f"₹{emi_amt:,.0f}")
                    a5.metric("DPD", f"{dpd}d")
                    a6.metric("Bureau", int(loan["bureau_score_at_origination"]))

                    p1, p2 = st.columns(2)
                    with p1:
                        fig_emi = go.Figure()
                        fig_emi.add_trace(go.Bar(name="Paid", x=["Count","Amount (₹L)"], y=[emis_paid, round(emi_amt*emis_paid/100000,1)], marker_color="#10b981", text=[emis_paid, f"₹{emi_amt*emis_paid/100000:.1f}L"], textposition="outside"))
                        fig_emi.add_trace(go.Bar(name="Remaining", x=["Count","Amount (₹L)"], y=[emis_rem, round(emi_amt*emis_rem/100000,1)], marker_color="#bfdbfe", text=[emis_rem, f"₹{emi_amt*emis_rem/100000:.1f}L"], textposition="outside"))
                        fig_emi.update_layout(barmode="group", height=240, margin=dict(t=20,b=10), plot_bgcolor="white", paper_bgcolor="white", legend=dict(orientation="h",y=1.1), title=dict(text="EMI progress",font=dict(size=13)))
                        st.plotly_chart(fig_emi, use_container_width=True)
                    with p2:
                        fig_rep = go.Figure(go.Bar(x=["Repaid","Outstanding"], y=[round(repaid/100000,1), round(outstanding/100000,1)], marker_color=["#10b981","#ef4444"], text=[f"₹{repaid/100000:.1f}L ({repaid_pct}%)", f"₹{outstanding/100000:.1f}L"], textposition="outside"))
                        fig_rep.update_layout(height=240, margin=dict(t=20,b=10), yaxis_title="₹ Lakhs", plot_bgcolor="white", paper_bgcolor="white", showlegend=False, title=dict(text="Repayment breakdown",font=dict(size=13)))
                        st.plotly_chart(fig_rep, use_container_width=True)

                    d1, d2 = st.columns(2)
                    with d1:
                        st.markdown(f"""<div class="aa-card" style="margin-bottom:0;">
                        <div class="aa-section-label">Loan details</div>
                        <table style="width:100%;font-size:13px;border-collapse:collapse;">
                        <tr><td style="color:#888;padding:6px 0;border-bottom:1px solid #f5f5f5;">Loan ID</td><td style="font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #f5f5f5;">{loan['loan_id']}</td></tr>
                        <tr><td style="color:#888;padding:6px 0;border-bottom:1px solid #f5f5f5;">Product</td><td style="font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #f5f5f5;">{loan['product']}</td></tr>
                        <tr><td style="color:#888;padding:6px 0;border-bottom:1px solid #f5f5f5;">Disbursed</td><td style="font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #f5f5f5;">{loan['disbursement_date']}</td></tr>
                        <tr><td style="color:#888;padding:6px 0;border-bottom:1px solid #f5f5f5;">Rate</td><td style="font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #f5f5f5;">{loan['interest_rate']}% p.a.</td></tr>
                        <tr><td style="color:#888;padding:6px 0;border-bottom:1px solid #f5f5f5;">Tenure</td><td style="font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #f5f5f5;">{tenure} months</td></tr>
                        <tr><td style="color:#888;padding:6px 0;">EMI/month</td><td style="font-weight:600;text-align:right;padding:6px 0;">₹{emi_amt:,.0f}</td></tr>
                        </table></div>""", unsafe_allow_html=True)
                    with d2:
                        st.markdown(f"""<div class="aa-card" style="margin-bottom:0;">
                        <div class="aa-section-label">Risk details</div>
                        <table style="width:100%;font-size:13px;border-collapse:collapse;">
                        <tr><td style="color:#888;padding:6px 0;border-bottom:1px solid #f5f5f5;">Bucket</td><td style="font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #f5f5f5;color:{lclr};">{bucket}</td></tr>
                        <tr><td style="color:#888;padding:6px 0;border-bottom:1px solid #f5f5f5;">DPD</td><td style="font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #f5f5f5;">{dpd} days</td></tr>
                        <tr><td style="color:#888;padding:6px 0;border-bottom:1px solid #f5f5f5;">Collection</td><td style="font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #f5f5f5;">{loan['collection_status']}</td></tr>
                        <tr><td style="color:#888;padding:6px 0;border-bottom:1px solid #f5f5f5;">Bureau score</td><td style="font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #f5f5f5;">{int(loan['bureau_score_at_origination'])}</td></tr>
                        <tr><td style="color:#888;padding:6px 0;border-bottom:1px solid #f5f5f5;">EMIs paid</td><td style="font-weight:600;text-align:right;padding:6px 0;border-bottom:1px solid #f5f5f5;">{emis_paid} / {tenure}</td></tr>
                        <tr><td style="color:#888;padding:6px 0;">Geography</td><td style="font-weight:600;text-align:right;padding:6px 0;">{loan['geography']}</td></tr>
                        </table></div>""", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    if bucket == "NPA": alert("<strong>Immediate action required.</strong> NPA account. Initiate legal recovery. Do not extend new credit.", "danger")
                    elif bucket == "SMA-2": alert("<strong>High priority collection.</strong> 61-90 DPD. Assign senior agent immediately.", "danger")
                    elif bucket == "SMA-1": alert("<strong>Active monitoring needed.</strong> 31-60 DPD. Follow up within 48 hours.", "warning")
                    elif bucket == "SMA-0": alert("<strong>Early warning.</strong> 1-30 DPD. Contact proactively — may self-cure.", "warning")
                    else: alert("<strong>Performing account.</strong> No overdue. Continue standard monitoring.", "success")

            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(f"Export {bname} accounts", c_loans.to_csv(index=False).encode(), "borrower_accounts.csv", "text/csv", use_container_width=True)

    else:
        summary = []
        for cid in unique_custs:
            b = sdf[sdf[group_col] == cid]
            worst = b.sort_values("dpd", ascending=False).iloc[0]["bucket"]
            summary.append({"CID": cid if has_cid else "N/A","Name": b["borrower_name"].iloc[0],"PAN": b["pan"].iloc[0] if has_pan else "N/A","Accounts": len(b),"Outstanding": f"₹{b['outstanding_amount'].sum()/100000:.1f}L","Max DPD": int(b["dpd"].max()),"Bucket": worst})
        sum_df = pd.DataFrame(summary)
        def cbkt(val):
            return {"Current":"background-color:#f0fdf4","SMA-0":"background-color:#fffbeb","SMA-1":"background-color:#fff7ed","SMA-2":"background-color:#fef2f2","NPA":"background-color:#fef2f2"}.get(val,"")
        st.dataframe(sum_df.style.map(cbkt, subset=["Bucket"]), use_container_width=True, hide_index=True, height=400)
        s1,s2,s3,s4 = st.columns(4)
        s1.metric("Customers", len(unique_custs))
        s2.metric("Accounts", len(sdf))
        s3.metric("AUM", f"₹{safe_aum(sdf)} Cr")
        s4.metric("PAR 30+", f"{safe_par(sdf)}%")
        st.download_button("Export list", sdf.to_csv(index=False).encode(), "search_results.csv", "text/csv")

elif page == "✅ Pre-Disbursal":
    page_header("Pre-Disbursal Credit Check", "Full credit assessment before loan disbursement")
    search_input = st.text_input("Search borrower", placeholder="Name / Customer ID / PAN", label_visibility="collapsed")
    st.markdown('<div style="font-size:12px;color:#888;margin:-8px 0 16px 2px;">Enter name, customer ID, or PAN to run credit check</div>', unsafe_allow_html=True)

    if not search_input:
        st.markdown("<br>", unsafe_allow_html=True)
        checks_info = ["✓ Existing loan obligations and total exposure","✓ Current DPD status across all accounts","✓ Repayment behaviour and track record","✓ Bureau score assessment","✓ Eligibility verdict with recommended loan limit","✓ Automated risk flags for analyst review"]
        col1, col2 = st.columns(2)
        for i, c in enumerate(checks_info):
            with col1 if i%2==0 else col2:
                st.markdown(f'<div style="background:#f9fafb;border-radius:10px;padding:12px 16px;margin-bottom:8px;font-size:13px;color:#444;border:1px solid #f0f0f0;">{c}</div>', unsafe_allow_html=True)
    else:
        group_col = "customer_id" if has_cid else "borrower_name"
        mask = df["borrower_name"].str.contains(search_input, case=False, na=False) | df["loan_id"].str.contains(search_input, case=False, na=False)
        if has_cid: mask = mask | df["customer_id"].str.contains(search_input, case=False, na=False)
        if has_pan: mask = mask | df["pan"].str.contains(search_input, case=False, na=False)
        results = df[mask]

        if len(results) == 0:
            alert("Borrower not found in system — this may be a new customer.", "warning")
            alert("<strong>New customer.</strong> No existing obligations found. Proceed with standard credit appraisal using bureau report and income documents.", "success")
        else:
            unique_cids = results[group_col].unique()
            selected_cid = unique_cids[0]
            if len(unique_cids) > 1:
                selected_cid = st.selectbox("Multiple matches found", unique_cids)

            bl = results[results[group_col] == selected_cid].copy()
            bname = bl["borrower_name"].iloc[0]
            cid_val = bl["customer_id"].iloc[0] if has_cid else "N/A"
            pan_val = bl["pan"].iloc[0] if has_pan else "N/A"
            phone_val = str(bl["phone"].iloc[0]) if has_phone else "N/A"

            total_loans = len(bl)
            total_out = bl["outstanding_amount"].sum()
            total_dis = bl["loan_amount"].sum()
            total_rep = total_dis - total_out
            rep_pct = round(total_rep/total_dis*100,1) if total_dis > 0 else 0
            max_dpd = int(bl["dpd"].max())
            worst_bucket = bl.sort_values("dpd", ascending=False).iloc[0]["bucket"]
            avg_bureau = int(bl["bureau_score_at_origination"].mean())
            npa_acc = len(bl[bl["bucket"]=="NPA"])
            overdue_acc = len(bl[bl["dpd"]>0])
            perf_acc = len(bl[bl["bucket"]=="Current"])
            total_emi = sum(calc_emi(r["loan_amount"],r["interest_rate"],r["tenure_months"]) for _,r in bl.iterrows())

            if npa_acc > 0: verdict,vclr,vbg,vreason = "REJECT","#dc2626","#fef2f2",f"{npa_acc} NPA account(s). Cannot extend credit."
            elif worst_bucket == "SMA-2": verdict,vclr,vbg,vreason = "REJECT","#dc2626","#fef2f2","SMA-2 account detected. High default risk."
            elif worst_bucket == "SMA-1": verdict,vclr,vbg,vreason = "HOLD","#ea580c","#fff7ed","SMA-1 detected. Regularise dues first."
            elif worst_bucket == "SMA-0": verdict,vclr,vbg,vreason = "CONDITIONAL","#d97706","#fffbeb","Minor overdue. Proceed with collateral only."
            elif avg_bureau >= 700 and rep_pct >= 40: verdict,vclr,vbg,vreason = "APPROVE","#16a34a","#f0fdf4","Good repayment history and bureau score."
            elif avg_bureau >= 650: verdict,vclr,vbg,vreason = "APPROVE WITH CAUTION","#1d4ed8","#eff6ff","Satisfactory profile. Standard terms."
            else: verdict,vclr,vbg,vreason = "REVIEW","#7c3aed","#faf5ff","Low bureau score. Manual review required."

            rec_limit = 0
            if verdict in ["APPROVE","APPROVE WITH CAUTION","CONDITIONAL"]:
                base = total_dis / total_loans
                if avg_bureau >= 720 and rep_pct >= 60: rec_limit = base * 1.5
                elif avg_bureau >= 680 and rep_pct >= 40: rec_limit = base * 1.0
                else: rec_limit = base * 0.5

            st.markdown(f"""
            <div style="background:{vbg};border-radius:16px;padding:24px 28px;margin-bottom:24px;border-left:5px solid {vclr};">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
                    <div>
                        <div style="font-size:28px;font-weight:800;color:{vclr};letter-spacing:-0.5px;">{verdict}</div>
                        <div style="font-size:14px;color:#555;margin-top:6px;">{vreason}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.05em;font-weight:600;">Recommended limit</div>
                        <div style="font-size:26px;font-weight:800;color:{vclr};">{"₹"+str(round(rec_limit/100000,1))+"L" if rec_limit > 0 else "N/A"}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="aa-card" style="margin-bottom:16px;">
                <div class="aa-section-label">Borrower identity</div>
                <div style="display:flex;gap:32px;flex-wrap:wrap;font-size:13px;">
                    <div><div style="color:#888;font-size:11px;font-weight:600;text-transform:uppercase;">Name</div><div style="font-weight:700;margin-top:2px;">{bname}</div></div>
                    <div><div style="color:#888;font-size:11px;font-weight:600;text-transform:uppercase;">Customer ID</div><div style="font-weight:700;margin-top:2px;font-family:monospace;">{cid_val}</div></div>
                    <div><div style="color:#888;font-size:11px;font-weight:600;text-transform:uppercase;">PAN</div><div style="font-weight:700;margin-top:2px;font-family:monospace;">{pan_val}</div></div>
                    <div><div style="color:#888;font-size:11px;font-weight:600;text-transform:uppercase;">Phone</div><div style="font-weight:700;margin-top:2px;">{phone_val}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            ca1,ca2,ca3,ca4,ca5,ca6 = st.columns(6)
            ca1.metric("Total loans", total_loans)
            ca2.metric("Total exposure", f"₹{total_out/100000:.1f}L")
            ca3.metric("Repaid", f"{rep_pct}%")
            ca4.metric("Max DPD", f"{max_dpd}d")
            ca5.metric("Bureau score", avg_bureau)
            ca6.metric("Monthly EMI load", f"₹{total_emi:,.0f}")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="aa-section-label">Credit checklist</div>', unsafe_allow_html=True)
            checks = [
                ("Bureau score",f"{avg_bureau}","Pass" if avg_bureau>=650 else "Fail","Min required 650"),
                ("NPA accounts",f"{npa_acc}","Pass" if npa_acc==0 else "Fail","Must be zero"),
                ("Overdue accounts",f"{overdue_acc}/{total_loans}","Pass" if overdue_acc==0 else "Warning" if overdue_acc/total_loans<0.3 else "Fail","Overdue ratio"),
                ("Repayment rate",f"{rep_pct}%","Pass" if rep_pct>=30 else "Warning","Min 30% repaid"),
                ("Worst bucket",worst_bucket,"Pass" if worst_bucket=="Current" else "Warning" if worst_bucket=="SMA-0" else "Fail","Should be Current"),
                ("Performing accounts",f"{perf_acc}/{total_loans}","Pass" if perf_acc/total_loans>=0.7 else "Warning","Min 70% performing"),
                ("Monthly EMI load",f"₹{total_emi:,.0f}","Pass" if total_emi<100000 else "Warning","Existing obligation"),
                ("Total exposure",f"₹{total_out/100000:.1f}L","Pass" if total_out<5000000 else "Warning","Concentration risk"),
            ]
            chk_df = pd.DataFrame(checks, columns=["Check","Value","Status","Note"])
            def color_chk(val):
                if val=="Pass": return "background-color:#f0fdf4;color:#16a34a;font-weight:700;"
                elif val=="Warning": return "background-color:#fffbeb;color:#d97706;font-weight:700;"
                else: return "background-color:#fef2f2;color:#dc2626;font-weight:700;"
            st.dataframe(chk_df.style.map(color_chk, subset=["Status"]), use_container_width=True, hide_index=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="aa-section-label">Existing loan accounts</div>', unsafe_allow_html=True)
            disp = bl.copy()
            disp["outstanding_fmt"] = disp["outstanding_amount"].apply(lambda x: f"₹{x/100000:.1f}L")
            disp["loan_fmt"] = disp["loan_amount"].apply(lambda x: f"₹{x/100000:.1f}L")
            disp["emi_fmt"] = disp.apply(lambda r: f"₹{calc_emi(r['loan_amount'],r['interest_rate'],r['tenure_months']):,.0f}", axis=1)
            show = disp[["loan_id","product","loan_fmt","outstanding_fmt","emi_fmt","emis_paid","tenure_months","dpd","bucket","collection_status"]].rename(columns={"loan_fmt":"loan","outstanding_fmt":"outstanding","emi_fmt":"EMI/mo","emis_paid":"EMIs paid","tenure_months":"tenure","collection_status":"collection"}).reset_index(drop=True)
            def cbkt2(val):
                return {"Current":"background-color:#f0fdf4","SMA-0":"background-color:#fffbeb","SMA-1":"background-color:#fff7ed","SMA-2":"background-color:#fef2f2","NPA":"background-color:#fef2f2"}.get(val,"")
            st.dataframe(show.style.map(cbkt2, subset=["bucket"]), use_container_width=True, hide_index=True)

            st.markdown("<br>", unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)
            with cc1:
                fig_exp = go.Figure(go.Bar(x=["Disbursed","Repaid","Outstanding"], y=[total_dis/100000,total_rep/100000,total_out/100000], marker_color=["#3b82f6","#10b981","#ef4444"], text=[f"₹{total_dis/100000:.1f}L",f"₹{total_rep/100000:.1f}L",f"₹{total_out/100000:.1f}L"], textposition="outside"))
                fig_exp.update_layout(height=260, margin=dict(t=30,b=10), yaxis_title="₹ Lakhs", plot_bgcolor="white", paper_bgcolor="white", showlegend=False, title=dict(text="Exposure breakdown",font=dict(size=13,color="#444")))
                st.plotly_chart(fig_exp, use_container_width=True)
            with cc2:
                bkt_c = bl["bucket"].value_counts().reset_index()
                bkt_c.columns = ["Bucket","Count"]
                fig_bkt = px.pie(bkt_c, names="Bucket", values="Count", hole=0.5, color="Bucket", color_discrete_map=COLOR_MAP)
                fig_bkt.update_layout(height=260, margin=dict(t=30,b=10), title=dict(text="Accounts by bucket",font=dict(size=13,color="#444")))
                st.plotly_chart(fig_bkt, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="aa-section-label">Risk flags</div>', unsafe_allow_html=True)
            flags = []
            if npa_acc > 0: flags.append(("danger",f"🔴 {npa_acc} NPA account(s) detected"))
            if max_dpd > 90: flags.append(("danger",f"🔴 Max DPD {max_dpd} days — high default risk"))
            if max_dpd > 30 and max_dpd <= 90: flags.append(("warning",f"🟠 Current max DPD is {max_dpd} days"))
            if avg_bureau < 650: flags.append(("danger",f"🔴 Bureau score {avg_bureau} below minimum 650"))
            if avg_bureau < 700 and avg_bureau >= 650: flags.append(("warning",f"🟡 Bureau score {avg_bureau} below preferred threshold 700"))
            if total_emi > 100000: flags.append(("warning",f"🟠 Monthly EMI load ₹{total_emi:,.0f} is high"))
            if total_out > 5000000: flags.append(("warning",f"🟡 Total exposure ₹{total_out/100000:.1f}L — monitor concentration"))
            if overdue_acc/total_loans > 0.5: flags.append(("danger",f"🔴 {overdue_acc}/{total_loans} accounts overdue — poor repayment track"))
            if len(flags) == 0:
                alert("✅ No risk flags. Clean profile — proceed with standard appraisal.", "success")
            else:
                for type_, msg in flags:
                    alert(msg, type_)

elif page == "👤 Eligibility":
    page_header("Borrower Eligibility", "Loan eligibility categorisation across your portfolio")

    def categorise(row):
        if row["bucket"] == "NPA" or row["dpd"] > 90: return "Blacklisted","🔴","No new loans.","#fef2f2","#dc2626"
        elif row["bucket"] == "SMA-2" or row["dpd"] > 60: return "High Risk","🔴","Not eligible.","#fef2f2","#dc2626"
        elif row["bucket"] == "SMA-1" or row["dpd"] > 30: return "Risky","🟠","Collateral required.","#fff7ed","#ea580c"
        elif row["bucket"] == "SMA-0" or row["dpd"] > 0: return "Borderline","🟡","Top-up only.","#fffbeb","#d97706"
        elif row["bureau_score_at_origination"] >= 720 and row["collection_status"] == "Collected": return "Premium","🟢","Higher amounts, better rates.","#f0fdf4","#15803d"
        elif row["bureau_score_at_origination"] >= 680 and row["collection_status"] == "Collected": return "Eligible","🟢","Standard terms.","#f0fdf4","#16a34a"
        else: return "Review Needed","🔵","Manual review.","#eff6ff","#1d4ed8"

    df[["eligibility","icon","reason","bg","color"]] = df.apply(lambda r: pd.Series(categorise(r)), axis=1)
    cats = ["Premium","Eligible","Borderline","Review Needed","Risky","High Risk","Blacklisted"]
    colors = ["#15803d","#16a34a","#d97706","#1d4ed8","#ea580c","#dc2626","#991b1b"]
    elig_counts = df["eligibility"].value_counts()

    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(7)
    for cat, col, clr in zip(cats, cols, colors):
        count = elig_counts.get(cat, 0)
        pct = round(count/len(df)*100,1)
        col.markdown(f'<div style="background:#ffffff;border-radius:12px;padding:14px;text-align:center;border:1px solid #f0f0f0;box-shadow:0 1px 3px rgba(0,0,0,0.04);border-top:3px solid {clr};"><div style="font-size:22px;font-weight:700;color:{clr};">{count}</div><div style="font-size:11px;color:#888;margin-top:3px;font-weight:500;">{cat}</div><div style="font-size:11px;color:#bbb;margin-top:1px;">{pct}%</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    ec1, ec2 = st.columns(2)
    with ec1:
        st.markdown('<div class="aa-section-label">Eligibility distribution</div>', unsafe_allow_html=True)
        fig_e = px.pie(df["eligibility"].value_counts().reset_index(), names="eligibility", values="count", hole=0.5, color="eligibility", color_discrete_map=dict(zip(cats, colors)))
        fig_e.update_traces(textposition="outside", textinfo="percent+label")
        fig_e.update_layout(**chart_layout(fig_e, 320).layout.to_plotly_json())
        st.plotly_chart(fig_e, use_container_width=True)
    with ec2:
        st.markdown('<div class="aa-section-label">Eligible vs not eligible by product</div>', unsafe_allow_html=True)
        df["eligible_flag"] = df["eligibility"].apply(lambda x: "Eligible" if x in ["Premium","Eligible"] else "Not eligible")
        prod_e = df.groupby(["product","eligible_flag"]).size().reset_index(name="count")
        fig_pe = px.bar(prod_e, x="product", y="count", color="eligible_flag", color_discrete_map={"Eligible":"#10b981","Not eligible":"#ef4444"}, barmode="stack")
        fig_pe.update_layout(**chart_layout(fig_pe, 320).layout.to_plotly_json())
        st.plotly_chart(fig_pe, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    filter_elig = st.multiselect("Filter by category", options=cats, default=cats)
    filtered_elig = df[df["eligibility"].isin(filter_elig)]
    for _, row in filtered_elig.head(50).iterrows():
        cid_span = f'<span style="font-size:11px;color:#999;margin-left:10px;font-family:monospace;">{row["customer_id"]}</span>' if has_cid else ""
        st.markdown(f"""
        <div style="background:{row['bg']};border-radius:10px;padding:12px 18px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;border:1px solid rgba(0,0,0,0.04);">
            <div><span style="font-weight:600;color:#1a1a2e;font-size:14px;">{row['icon']} {row['borrower_name']}</span><span style="font-size:12px;color:#888;margin-left:12px;">{row['product']} · {row['geography']}</span>{cid_span}</div>
            <div style="text-align:right;"><span style="font-size:12px;font-weight:600;color:{row['color']};background:white;padding:3px 12px;border-radius:20px;border:1px solid {row['color']}20;">{row['eligibility']}</span><div style="font-size:11px;color:#888;margin-top:3px;">{row['reason']}</div></div>
        </div>
        """, unsafe_allow_html=True)
    export_cols = ["loan_id","borrower_name","product","geography","dpd","bucket","bureau_score_at_origination","eligibility","reason"]
    if has_cid: export_cols = ["customer_id"] + export_cols
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button("Export eligibility report", filtered_elig[export_cols].to_csv(index=False).encode(), "eligibility_report.csv", "text/csv", use_container_width=True)

elif page == "🤖 AI Insights":
    page_header("AI Insights", f"Portfolio intelligence for {st.session_state.nbfc_name}")

    par30 = safe_par(df)
    npa_rate = safe_npa(df)
    col_eff = safe_collection(df)
    avg_bureau = round(df["bureau_score_at_origination"].mean(), 0)
    IND_PAR,IND_NPA,IND_COL,IND_BUR = 8.2, 3.1, 88.5, 695

    m1,m2,m3,m4 = st.columns(4)
    m1.metric("PAR 30+", f"{par30}%", f"{round(par30-IND_PAR,1)}% vs industry", delta_color="inverse")
    m2.metric("NPA Rate", f"{npa_rate}%", f"{round(npa_rate-IND_NPA,1)}% vs industry", delta_color="inverse")
    m3.metric("Collection Eff.", f"{col_eff}%", f"{round(col_eff-IND_COL,1)}% vs industry")
    m4.metric("Avg Bureau", f"{int(avg_bureau)}", f"{int(avg_bureau-IND_BUR)} vs industry")

    st.markdown("<br>", unsafe_allow_html=True)
    ai1, ai2 = st.columns(2)
    with ai1:
        st.markdown('<div class="aa-section-label">Your portfolio vs industry</div>', unsafe_allow_html=True)
        fig_c = go.Figure()
        fig_c.add_trace(go.Bar(name="Your Portfolio", x=["PAR 30+","NPA Rate","Collection Eff."], y=[par30,npa_rate,col_eff], marker_color="#1d4ed8", text=[f"{par30}%",f"{npa_rate}%",f"{col_eff}%"], textposition="outside"))
        fig_c.add_trace(go.Bar(name="Industry Avg", x=["PAR 30+","NPA Rate","Collection Eff."], y=[IND_PAR,IND_NPA,IND_COL], marker_color="#e2e8f0", text=[f"{IND_PAR}%",f"{IND_NPA}%",f"{IND_COL}%"], textposition="outside"))
        fig_c.update_layout(**chart_layout(fig_c, 300).layout.to_plotly_json())
        st.plotly_chart(fig_c, use_container_width=True)
    with ai2:
        st.markdown('<div class="aa-section-label">Bureau score distribution</div>', unsafe_allow_html=True)
        fig_h = px.histogram(df, x="bureau_score_at_origination", nbins=20, color_discrete_sequence=["#6366f1"])
        fig_h.add_vline(x=650, line_dash="dash", line_color="#ef4444", annotation_text="Min 650", annotation_font=dict(size=11,color="#ef4444"))
        fig_h.add_vline(x=700, line_dash="dash", line_color="#f59e0b", annotation_text="Preferred 700", annotation_font=dict(size=11,color="#f59e0b"))
        fig_h.update_layout(**chart_layout(fig_h, 300).layout.to_plotly_json())
        st.plotly_chart(fig_h, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="aa-section-label">AI generated observations</div>', unsafe_allow_html=True)
    obs = []
    if par30 > IND_PAR: obs.append(("danger",f"🔴 PAR above industry — your {par30}% vs industry {IND_PAR}%. Focus collection on SMA-1 and SMA-2 accounts."))
    else: obs.append(("success",f"🟢 PAR below industry — your {par30}% beats industry average of {IND_PAR}%."))
    if col_eff < IND_COL: obs.append(("danger",f"🔴 Collection efficiency below industry — {col_eff}% vs {IND_COL}%."))
    else: obs.append(("success",f"🟢 Strong collection efficiency — {col_eff}% beats industry {IND_COL}%."))
    hrp = df[df["dpd"]>=30].groupby("product").size()
    if len(hrp) > 0: obs.append(("warning",f"⚠️ Highest risk product — {hrp.idxmax()} has the most overdue accounts. Review credit criteria."))
    hrg = df[df["dpd"]>=30].groupby("geography").size()
    if len(hrg) > 0: obs.append(("warning",f"📍 Highest risk geography — {hrg.idxmax()} has the highest delinquency rate."))
    lb = df[df["bureau_score_at_origination"]<650]
    if len(lb) > 0:
        lb_npa = round(len(lb[lb["bucket"]=="NPA"])/len(lb)*100,1)
        obs.append(("warning",f"📊 Bureau insight — borrowers below 650 score have {lb_npa}% NPA rate in your portfolio."))
    for type_, msg in obs:
        alert(msg, type_)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="aa-section-label">NPA prediction by product</div>', unsafe_allow_html=True)
    pred_rows = []
    for prod in df["product"].unique():
        pf = df[df["product"]==prod]
        cp = safe_par(pf)
        pn = round(cp*0.35,1)
        pred_rows.append({"Product":prod,"Loans":len(pf),"PAR 30+":f"{cp}%","Predicted NPA (90d)":f"{pn}%","Risk":"High" if pn>5 else "Medium" if pn>2 else "Low"})
    pred_df = pd.DataFrame(pred_rows)
    def crisk(val):
        if val=="High": return "background-color:#fef2f2;color:#dc2626;font-weight:700;"
        elif val=="Medium": return "background-color:#fffbeb;color:#d97706;font-weight:700;"
        else: return "background-color:#f0fdf4;color:#16a34a;font-weight:700;"
    st.dataframe(pred_df.style.map(crisk, subset=["Risk"]), use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="aa-section-label">3 month portfolio forecast</div>', unsafe_allow_html=True)
    months = ["Current","Month 1","Month 2","Month 3"]
    par_fc = [par30, round(par30*1.05,1), round(par30*1.08,1), round(par30*1.03,1)]
    npa_fc = [npa_rate, round(npa_rate*1.08,1), round(npa_rate*1.12,1), round(npa_rate*1.06,1)]
    fig_fc = go.Figure()
    fig_fc.add_trace(go.Scatter(x=months, y=par_fc, mode="lines+markers+text", name="PAR 30+", line=dict(color="#ef4444",width=3), marker=dict(size=10,color="#ef4444"), text=[f"{v}%" for v in par_fc], textposition="top center", textfont=dict(size=12,color="#ef4444")))
    fig_fc.add_trace(go.Scatter(x=months, y=npa_fc, mode="lines+markers+text", name="NPA Rate", line=dict(color="#3b82f6",width=3,dash="dash"), marker=dict(size=10,color="#3b82f6",symbol="diamond"), text=[f"{v}%" for v in npa_fc], textposition="bottom center", textfont=dict(size=12,color="#3b82f6")))
    fig_fc.add_hrect(y0=0, y1=IND_PAR, fillcolor="#eff6ff", opacity=0.5, layer="below", line_width=0, annotation_text=f"Industry safe zone (< {IND_PAR}%)", annotation_position="top left", annotation_font=dict(size=11,color="#1d4ed8"))
    fig_fc.update_layout(**chart_layout(fig_fc, 340).layout.to_plotly_json())
    fig_fc.update_layout(yaxis=dict(title="Rate (%)",rangemode="tozero"))
    st.plotly_chart(fig_fc, use_container_width=True)
    alert("Forecasts are directional indicators based on current roll rates. Actual outcomes depend on collection efforts and market conditions.", "info")

elif page == "🔧 Admin":
    if st.session_state.role != "admin":
        alert("Access denied. This page is for admins only.", "danger")
        st.stop()
    page_header("Admin Panel", "Manage users, approvals, and system health")

    admin_tab1, admin_tab2, admin_tab3 = st.tabs(["User Management","Activity Log","System Info"])

    with admin_tab1:
        st.markdown('<div class="aa-section-label">Registered users</div>', unsafe_allow_html=True)
        try:
            all_users = supabase.table("users").select("*").order("created_at", desc=True).execute()
            if all_users.data:
                pending = [u for u in all_users.data if u["status"] == "pending"]
                if pending:
                    alert(f"<strong>{len(pending)} account(s) pending your approval.</strong>", "warning")

                for user in all_users.data:
                    status_icons = {"pending":"🟡","approved":"🟢","rejected":"🔴"}
                    icon = status_icons.get(user["status"],"⚪")
                    with st.expander(f"{icon} {user['nbfc_name']} · {user['email']} · {user['status'].upper()}", expanded=(user["status"]=="pending")):
                        u1,u2,u3,u4 = st.columns(4)
                        u1.metric("NBFC", user["nbfc_name"])
                        u2.metric("Role", user["role"])
                        u3.metric("Status", user["status"])
                        u4.metric("Valid until", str(user["valid_until"]) if user["valid_until"] else "—")
                        st.caption(f"Signed up: {user['created_at'][:19].replace('T',' ')}")

                        if user["status"] == "pending":
                            st.markdown("---")
                            ac1, ac2, ac3, ac4 = st.columns(4)
                            with ac1: valid_d = st.date_input("Validity", date(2025,12,31), key=f"vd_{user['id']}")
                            with ac2: role_s = st.selectbox("Role", ["user","admin"], key=f"rs_{user['id']}")
                            with ac3:
                                st.markdown("<br>", unsafe_allow_html=True)
                                if st.button("✓ Approve", key=f"ap_{user['id']}", type="primary", use_container_width=True):
                                    supabase.table("users").update({"status":"approved","role":role_s,"valid_until":valid_d.isoformat()}).eq("id",user["id"]).execute()
                                    log_activity(st.session_state.user_id,"approve_user",f"Approved {user['email']}")
                                    st.rerun()
                            with ac4:
                                st.markdown("<br>", unsafe_allow_html=True)
                                if st.button("✗ Reject", key=f"rj_{user['id']}", use_container_width=True):
                                    supabase.table("users").update({"status":"rejected"}).eq("id",user["id"]).execute()
                                    st.rerun()

                        elif user["status"] == "approved":
                            st.markdown("---")
                            ec1, ec2, ec3 = st.columns(3)
                            with ec1: new_v = st.date_input("Extend validity", date.fromisoformat(str(user["valid_until"])) if user["valid_until"] else date.today(), key=f"ev_{user['id']}")
                            with ec2:
                                st.markdown("<br>", unsafe_allow_html=True)
                                if st.button("Update", key=f"upd_{user['id']}", use_container_width=True):
                                    supabase.table("users").update({"valid_until":new_v.isoformat()}).eq("id",user["id"]).execute()
                                    log_activity(st.session_state.user_id,"extend_validity",f"{user['email']} to {new_v}")
                                    st.rerun()
                            with ec3:
                                st.markdown("<br>", unsafe_allow_html=True)
                                if st.button("Revoke", key=f"rv_{user['id']}", use_container_width=True):
                                    supabase.table("users").update({"status":"rejected"}).eq("id",user["id"]).execute()
                                    st.rerun()
        except Exception as e:
            alert(f"Error loading users: {e}", "danger")

    with admin_tab2:
        st.markdown('<div class="aa-section-label">Recent activity</div>', unsafe_allow_html=True)
        try:
            logs = supabase.table("activity_log").select("*, users(email, nbfc_name)").order("created_at", desc=True).limit(100).execute()
            if logs.data:
                log_rows = []
                for log in logs.data:
                    ui = log.get("users") or {}
                    log_rows.append({"Time":log["created_at"][:19].replace("T"," "),"NBFC":ui.get("nbfc_name","System"),"Email":ui.get("email","—"),"Action":log["action"],"Detail":log["detail"] or ""})
                st.dataframe(pd.DataFrame(log_rows), use_container_width=True, hide_index=True, height=450)
            else:
                alert("No activity logs yet.", "info")
        except Exception as e:
            alert(f"Error: {e}", "danger")

    with admin_tab3:
        st.markdown('<div class="aa-section-label">System overview</div>', unsafe_allow_html=True)
        try:
            total_u = supabase.table("users").select("id", count="exact").execute()
            appr_u = supabase.table("users").select("id", count="exact").eq("status","approved").execute()
            pend_u = supabase.table("users").select("id", count="exact").eq("status","pending").execute()
            uploads = supabase.table("portfolio_data").select("id", count="exact").execute()
            si1,si2,si3,si4 = st.columns(4)
            si1.metric("Total users", total_u.count)
            si2.metric("Approved", appr_u.count)
            si3.metric("Pending", pend_u.count)
            si4.metric("Data uploads", uploads.count)
        except Exception as e:
            alert(f"Error: {e}", "danger")

        if has_data:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="aa-section-label">Data quality check</div>', unsafe_allow_html=True)
            qr = [{"Column":c,"Type":str(df[c].dtype),"Nulls":df[c].isnull().sum(),"Null%":f"{round(df[c].isnull().sum()/len(df)*100,1)}%","Status":"OK" if df[c].isnull().sum()==0 else "Warning"} for c in df.columns]
            qdf = pd.DataFrame(qr)
            def cstat(val):
                return "background-color:#f0fdf4;color:#16a34a;font-weight:600;" if val=="OK" else "background-color:#fffbeb;color:#d97706;font-weight:600;"
            st.dataframe(qdf.style.map(cstat, subset=["Status"]), use_container_width=True, hide_index=True)

elif page == "📋 Upload Guide":
    page_header("Upload Guide", "How to prepare and upload your portfolio data")

    st.markdown("<br>", unsafe_allow_html=True)
    alert("Your data is saved securely to your account. Once uploaded, it loads automatically on every login — no re-uploading needed.", "success")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="aa-section-label">Step 1 — Download sample file</div>', unsafe_allow_html=True)
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
    st.download_button("⬇ Download sample CSV", pd.DataFrame(sample_data).to_csv(index=False).encode(), "sample_portfolio.csv", "text/csv", use_container_width=True, type="primary")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="aa-section-label">Step 2 — Required columns (17 total)</div>', unsafe_allow_html=True)
    alert("All 17 columns must be present with exact names — spelling, case, and underscores must match.", "warning")
    st.dataframe(pd.DataFrame({
        "Column":["loan_id","customer_id","borrower_name","pan","phone","product","geography","disbursement_date","loan_amount","outstanding_amount","tenure_months","interest_rate","emis_paid","dpd","bucket","collection_status","bureau_score_at_origination"],
        "Type":["Text","Text","Text","Text","Text","Text","Text","Date","Number","Number","Number","Number","Number","Number","Text","Text","Number"],
        "Format / Allowed values":["Unique e.g. LN-1001","Same for all loans of one customer e.g. CID-10001","Full name","PAN number","10-digit mobile","Business Loan / MSME Loan / Equipment Finance / Working Capital / Personal Loan","City name","YYYY-MM-DD","Numbers only e.g. 500000","Numbers only e.g. 420000","Months e.g. 36","% e.g. 18.5","Count e.g. 8","0 if current, else 30/60/90","Current / SMA-0 / SMA-1 / SMA-2 / NPA","Collected / Partially Collected / Defaulted","300–900 e.g. 720"]
    }), use_container_width=True, hide_index=True, height=580)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="aa-section-label">Step 3 — Common mistakes to avoid</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    mistakes = [("Wrong date format","Use YYYY-MM-DD · not DD/MM/YYYY"),("₹ symbol in amounts","Write 500000 · not ₹5,00,000"),("Wrong bucket spelling","Exact: Current / SMA-0 / SMA-1 / SMA-2 / NPA"),("Commas in numbers","Write 500000 · not 5,00,000"),("Spaces in column names","loan_id · not ' loan_id '"),("Different CID for same customer","Same customer_id for all loans of one borrower")]
    for i,(t,d) in enumerate(mistakes):
        with c1 if i%2==0 else c2:
            st.markdown(f'<div style="background:#fffbeb;border-radius:10px;padding:12px 16px;margin-bottom:8px;border:1px solid #fde68a;font-size:13px;"><strong style="color:#92400e;">⚠ {t}</strong><br><span style="color:#78350f;">{d}</span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="aa-section-label">DPD to bucket mapping</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        "DPD":["0","1–30","31–60","61–90","90+"],
        "Bucket":["Current","SMA-0","SMA-1","SMA-2","NPA"],
        "Meaning":["Performing — no overdue","Early stress","Moderate stress","High stress","Defaulted"],
        "Action":["Monitor normally","Flag for review","Assign collection agent","Escalate immediately","Legal / recovery"]
    }), use_container_width=True, hide_index=True)