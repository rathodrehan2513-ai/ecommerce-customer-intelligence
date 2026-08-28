import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import re
from streamlit_google_auth import Authenticate

# Page configuration
st.set_page_config(
    page_title="E-Commerce Customer Intelligence",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished UI & Login Card
st.markdown("""
<style>
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4B4B, #FF8F6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .result-card {
        padding: 1.5rem;
        border-radius: 12px;
        background: rgba(38, 39, 48, 0.6);
        border-left: 5px solid #00D26A;
        margin-top: 1.2rem;
    }
    
    .google-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 0.55rem;
        border-radius: 8px;
        background-color: #ffffff;
        color: #3c4043;
        font-weight: 500;
        font-size: 0.95rem;
        border: 1px solid #dadce0;
        cursor: pointer;
        transition: background-color 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
    }
    .google-btn:hover {
        background-color: #f8f9fa;
        box-shadow: 0 1px 3px rgba(60,64,67,0.3);
    }
    .google-icon {
        width: 18px;
        height: 18px;
        margin-right: 10px;
    }
    
    .auth-separator {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.2rem 0;
        color: #888;
        font-size: 0.85rem;
    }
    .auth-separator::before,
    .auth-separator::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    }
    .auth-separator:not(:empty)::before {
        margin-right: .5em;
    }
    .auth-separator:not(:empty)::after {
        margin-left: .5em;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- AUTHENTICATION SETUP -----------------
google_auth_configured = "google_auth" in st.secrets
if google_auth_configured:
    authenticator = Authenticate(
        secret_credentials_path={
            "installed": {
                "client_id": st.secrets["google_auth"]["client_id"],
                "client_secret": st.secrets["google_auth"]["client_secret"],
                "redirect_uris": [st.secrets["google_auth"]["redirect_uri"]],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        cookie_name="customer_intelligence_auth_cookie",
        cookie_key=st.secrets["google_auth"]["cookie_secret"],
        cookie_expiry_days=1,
    )
    authenticator.check_authentification()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.session_state["email"] = ""

def is_valid_email(email_str):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email_str.strip()) is not None

def login():
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>🛍️ Customer Intelligence Portal</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Secure access for ML insights and segmentation</p>", unsafe_allow_html=True)
        st.write("")
        
        with st.container(border=True):
            # Google OAuth Button
            if google_auth_configured:
                authenticator.login()
                st.markdown('<div class="auth-separator">OR SIGN IN WITH ANY EMAIL</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="auth-separator">SIGN IN WITH ANY EMAIL</div>', unsafe_allow_html=True)

            # Universal Email Access Form
            with st.form("open_email_login_form"):
                user_email = st.text_input("Work or Personal Email ID", placeholder="e.g. name@company.com or you@gmail.com")
                submit = st.form_submit_button("Continue with Email 🚀", use_container_width=True)
                
                if submit:
                    clean_email = user_email.strip()
                    
                    if not clean_email:
                        st.warning("Please enter an email address.")
                    elif not is_valid_email(clean_email):
                        st.error("Please enter a valid email format (e.g. name@domain.com).")
                    else:
                        email_handle = clean_email.split("@")[0].replace(".", " ").replace("_", " ").title()
                        st.session_state["authenticated"] = True
                        st.session_state["email"] = clean_email
                        st.session_state["username"] = email_handle
                        st.rerun()

def logout():
    if google_auth_configured and st.session_state.get("connected", False):
        authenticator.logout()
    st.session_state["authenticated"] = False
    st.session_state["connected"] = False
    st.session_state["username"] = ""
    st.session_state["email"] = ""
    st.rerun()

# Determine Login State
is_google_logged_in = st.session_state.get("connected", False)
is_manual_logged_in = st.session_state.get("authenticated", False)

# ----------------- MAIN APPLICATION ROUTING -----------------
if not (is_google_logged_in or is_manual_logged_in):
    login()
else:
    # Resolve active user info
    if is_google_logged_in:
        user_info = st.session_state.get("user_info", {})
        display_user = user_info.get("name", "Google User")
        display_email = user_info.get("email", "")
    else:
        display_user = st.session_state.get("username", "Analyst")
        display_email = st.session_state.get("email", "")

    # Sidebar Navigation & User Info
    with st.sidebar:
        st.markdown(f"👤 **Logged in as:** `{display_user}`")
        if display_email:
            st.caption(f"📧 `{display_email}`")
        if st.button("Log Out", use_container_width=True):
            logout()
        st.divider()
        
        st.subheader("Navigation")
        page = st.radio(
            "Go to",
            ["Customer Segment Predictor", "Dashboard", "Customer Explorer"],
            label_visibility="collapsed"
        )

    # Load artifacts (cache for performance)
    @st.cache_resource
    def load_artifacts():
        model = joblib.load("customer_segmentation_model.pkl")[cite: 1]
        scaler = joblib.load("customer_scaler.pkl")[cite: 1]
        segment_names = joblib.load("segment_names.pkl")[cite: 1]
        return model, scaler, segment_names

    model, scaler, segment_names = load_artifacts()

    # ----------------- VIEW 1: CUSTOMER SEGMENT PREDICTOR -----------------
    if page == "Customer Segment Predictor":
        st.markdown('<div class="hero-title">Predict Customer Segment</div>', unsafe_allow_html=True)
        st.caption("Classify live user behavior profiles dynamically using the trained K-Means model.")
        st.divider()

        # Input Layout
        c1, c2 = st.columns(2)
        with c1:
            total_spend = st.number_input("Total Spend ($)", min_value=0.0, value=1000.0, step=50.0)
            items_purchased = st.number_input("Items Purchased", min_value=1, value=10, step=1)
            
        with c2:
            avg_rating = st.slider("Average Rating", min_value=1.0, max_value=5.0, value=4.0, step=0.1)
            recency = st.number_input("Days Since Last Purchase", min_value=0, value=20, step=1)

        predict_btn = st.button("🚀 Predict Customer Segment", type="primary", use_container_width=True)

        if predict_btn:
            # Model inference
            input_data = np.array([[total_spend, items_purchased, avg_rating, recency]])
            scaled_features = scaler.transform(input_data)
            cluster_id = model.predict(scaled_features)[0]
            cluster_label = segment_names.get(cluster_id, f"Cluster {cluster_id}")

            st.write("")
            
            # Interactive Tab Interface
            tab_overview, tab_benchmarks, tab_playbook = st.tabs([
                "🎯 Segment Overview", 
                "📊 Feature Radar & Benchmarks", 
                "💡 Actionable Marketing Playbook"
            ])

            # Tab 1: Overview
            with tab_overview:
                st.markdown(f"""
                <div class="result-card">
                    <span style="color: #aaa; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">Classification Result</span>
                    <h2 style="margin: 0.4rem 0; color: #00D26A;">{cluster_label}</h2>
                    <p style="margin: 0; color: #ddd; font-size: 0.95rem;">Assigned Cluster ID: <b>#{cluster_id}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Spend Profile", f"${total_spend:,.2f}")
                m2.metric("Basket Volume", f"{int(items_purchased)} items")
                m3.metric("Engagement Rating", f"{avg_rating:.1f} / 5.0")
                m4.metric("Activity Recency", f"{int(recency)} days ago")

            # Tab 2: Feature Radar & Benchmarks
            with tab_benchmarks:
                st.markdown("#### Customer Metric Profile")
                categories = ['Spend Intensity', 'Basket Size', 'Satisfaction', 'Recency Score']
                
                spend_score = min(100, (total_spend / 2500.0) * 100)
                basket_score = min(100, (items_purchased / 25.0) * 100)
                rating_score = (avg_rating / 5.0) * 100
                recency_score = max(0, 100 - (recency / 90.0 * 100))

                values = [spend_score, basket_score, rating_score, recency_score]

                fig_radar = px.line_polar(
                    r=values + [values[0]],
                    theta=categories + [categories[0]],
                    line_close=True,
                    template="plotly_dark"
                )
                fig_radar.update_traces(fill='toself', fillcolor='rgba(255, 75, 75, 0.3)', line_color='#FF4B4B')
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    showlegend=False,
                    margin=dict(t=20, b=20, l=40, r=40)
                )
                st.plotly_chart(fig_radar, use_container_width=True)

            # Tab 3: Actionable Marketing Playbook
            with tab_playbook:
                st.markdown(f"#### Recommended Strategies for **{cluster_label}**")
                
                if "High" in cluster_label or "VIP" in cluster_label or total_spend > 1500:
                    st.success("🌟 **Priority VIP Customer**")
                    st.markdown("""
                    * **Retention:** Assign priority customer support and early beta access to product drops.
                    * **Upselling:** Offer bespoke premium bundles and loyalty tier upgrades.
                    * **Engagement:** Send personalized executive check-ins and exclusive discount codes.
                    """)
                elif recency > 45:
                    st.warning("⚠️ **At-Risk / Churn Alert**")
                    st.markdown("""
                    * **Re-engagement Campaign:** Trigger automated *"We miss you"* email workflows with a 15% discount.
                    * **Feedback Loop:** Send a 1-question NPS survey to diagnose churn drivers.
                    * **Remarketing:** Enroll this segment in tailored Facebook/Google retargeting ads.
                    """)
                else:
                    st.info("📈 **Growth & Nurturing Cohort**")
                    st.markdown("""
                    * **Cross-Selling:** Recommend complementary items based on previous purchase history.
                    * **Frequency Boost:** Introduce time-limited free shipping thresholds on orders over $50.
                    * **Social Proof:** Invite them to leave reviews in exchange for rewards points.
                    """)

    # ----------------- VIEW 2: ANALYTICS DASHBOARD -----------------
    elif page == "Dashboard":
        st.markdown('<div class="hero-title">Analytics Dashboard</div>', unsafe_allow_html=True)
        st.caption("Comprehensive overview of customer behavior, spending patterns, and segment distributions.")
        st.divider()

        @st.cache_data
        def load_and_process_data():
            data = pd.read_csv("customer_intelligence_data.csv")[cite: 1]
            feature_cols = ["Total Spend", "Items Purchased", "Average Rating", "Days Since Last Purchase"]
            if all(col in data.columns for col in feature_cols):
                scaled_vals = scaler.transform(data[feature_cols])
                cluster_preds = model.predict(scaled_vals)
                data["Segment"] = [segment_names.get(c, f"Cluster {c}") for c in cluster_preds]
            return data

        try:
            df = load_and_process_data()

            # KPI Summary Metrics
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            with kpi1:
                st.metric("Total Customers", f"{len(df):,}")
            with kpi2:
                st.metric("Avg. Total Spend", f"${df['Total Spend'].mean():,.2f}")
            with kpi3:
                st.metric("Avg. Rating", f"{df['Average Rating'].mean():.2f} / 5.0")
            with kpi4:
                st.metric("Avg. Recency", f"{df['Days Since Last Purchase'].mean():.1f} days")

            st.write("")
            st.divider()

            # Row 1: Segment Breakdown & Scatter Analysis
            col_chart1, col_chart2 = st.columns([1, 1.3])

            with col_chart1:
                st.subheader("👥 Customer Segment Breakdown")
                segment_counts = df["Segment"].value_counts().reset_index()
                segment_counts.columns = ["Segment", "Count"]
                
                fig_pie = px.pie(
                    segment_counts,
                    names="Segment",
                    values="Count",
                    hole=0.45,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_pie.update_layout(
                    margin=dict(t=20, b=20, l=10, r=10),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            with col_chart2:
                st.subheader("💰 Spend vs. Items Purchased")
                fig_scatter = px.scatter(
                    df,
                    x="Items Purchased",
                    y="Total Spend",
                    color="Segment",
                    size="Average Rating",
                    hover_data=["Days Since Last Purchase"],
                    template="plotly_dark",
                    opacity=0.8
                )
                fig_scatter.update_layout(margin=dict(t=20, b=20, l=10, r=10))
                st.plotly_chart(fig_scatter, use_container_width=True)

            st.divider()

            # Row 2: Recency and Rating Distributions
            col_chart3, col_chart4 = st.columns(2)

            with col_chart3:
                st.subheader("⏳ Recency Distribution (Days)")
                fig_hist = px.histogram(
                    df,
                    x="Days Since Last Purchase",
                    nbins=25,
                    marginal="box",
                    color_discrete_sequence=["#FF8F6B"],
                    template="plotly_dark"
                )
                fig_hist.update_layout(margin=dict(t=20, b=20, l=10, r=10), yaxis_title="Customer Count")
                st.plotly_chart(fig_hist, use_container_width=True)

            with col_chart4:
                st.subheader("⭐ Average Rating Distribution")
                fig_rating = px.histogram(
                    df,
                    x="Average Rating",
                    nbins=20,
                    color_discrete_sequence=["#00D26A"],
                    template="plotly_dark"
                )
                fig_rating.update_layout(margin=dict(t=20, b=20, l=10, r=10), yaxis_title="Customer Count")
                st.plotly_chart(fig_rating, use_container_width=True)

        except FileNotFoundError:
            st.error("`customer_intelligence_data.csv` was not found. Please verify the repository path.")

    # ----------------- VIEW 3: CUSTOMER EXPLORER -----------------
    elif page == "Customer Explorer":
        st.markdown('<div class="hero-title">Customer Explorer</div>', unsafe_allow_html=True)
        st.caption("Search, filter, and inspect detailed behavioral profiles and segment classifications.")
        st.divider()

        @st.cache_data
        def load_explorer_data():
            data = pd.read_csv("customer_intelligence_data.csv")[cite: 1]
            feature_cols = ["Total Spend", "Items Purchased", "Average Rating", "Days Since Last Purchase"]
            if all(col in data.columns for col in feature_cols):
                scaled_vals = scaler.transform(data[feature_cols])
                cluster_preds = model.predict(scaled_vals)
                data["Segment"] = [segment_names.get(c, f"Cluster {c}") for c in cluster_preds]
            return data

        try:
            df = load_explorer_data()

            # Filter Controls
            st.markdown("### 🔍 Filters & Search")
            f1, f2, f3 = st.columns([1.5, 2, 2])

            with f1:
                available_segments = ["All"] + sorted(list(df["Segment"].dropna().unique())) if "Segment" in df.columns else ["All"]
                selected_segment = st.selectbox("Customer Segment", available_segments)

            with f2:
                spend_range = st.slider(
                    "Total Spend ($)",
                    min_value=float(df["Total Spend"].min()),
                    max_value=float(df["Total Spend"].max()),
                    value=(float(df["Total Spend"].min()), float(df["Total Spend"].max())),
                    step=25.0
                )

            with f3:
                min_rating, max_rating = st.slider(
                    "Average Rating",
                    min_value=1.0,
                    max_value=5.0,
                    value=(1.0, 5.0),
                    step=0.1
                )

            # Apply filters
            filtered_df = df[
                (df["Total Spend"] >= spend_range[0]) & 
                (df["Total Spend"] <= spend_range[1]) &
                (df["Average Rating"] >= min_rating) &
                (df["Average Rating"] <= max_rating)
            ]

            if selected_segment != "All" and "Segment" in df.columns:
                filtered_df = filtered_df[filtered_df["Segment"] == selected_segment]

            # Results & Export Bar
            r_col1, r_col2 = st.columns([3, 1])
            with r_col1:
                st.markdown(f"**Showing {len(filtered_df):,} of {len(df):,} total customers**")
            with r_col2:
                csv_data = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Filtered CSV",
                    data=csv_data,
                    file_name="filtered_customer_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            # Interactive Data Table
            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=320,
                column_config={
                    "Total Spend": st.column_config.NumberColumn("Total Spend", format="$%.2f"),
                    "Average Rating": st.column_config.NumberColumn("Rating", format="%.2f ⭐"),
                    "Items Purchased": st.column_config.NumberColumn("Items Purchased", format="%d 📦"),
                    "Days Since Last Purchase": st.column_config.NumberColumn("Recency", format="%d days")
                }
            )

            st.divider()

            # Single Customer Deep Dive
            st.subheader("👤 Individual Customer Deep-Dive")
            if not filtered_df.empty:
                selected_idx = st.selectbox(
                    "Select Customer Record (Row Index)",
                    options=filtered_df.index,
                    format_func=lambda x: f"Customer #{x} - {filtered_df.loc[x, 'Segment'] if 'Segment' in filtered_df.columns else ''} (${filtered_df.loc[x, 'Total Spend']:,.2f})"
                )

                selected_customer = filtered_df.loc[selected_idx]

                c_metric1, c_metric2, c_metric3, c_metric4, c_metric5 = st.columns(5)
                with c_metric1:
                    st.metric("Total Spend", f"${selected_customer['Total Spend']:,.2f}")
                with c_metric2:
                    st.metric("Items Purchased", f"{int(selected_customer['Items Purchased'])}")
                with c_metric3:
                    st.metric("Avg Rating", f"{selected_customer['Average Rating']:.2f} ⭐")
                with c_metric4:
                    st.metric("Recency", f"{int(selected_customer['Days Since Last Purchase'])} days")
                with c_metric5:
                    st.metric("Assigned Cohort", f"{selected_customer.get('Segment', 'N/A')}")
            else:
                st.warning("No customer records match the current filter criteria.")

        except FileNotFoundError:
            st.error("`customer_intelligence_data.csv` was not found. Please verify the repository path.")
