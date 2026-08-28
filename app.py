import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px

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
    /* Gradient accent glow for headers */
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4B4B, #FF8F6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    /* Segment result card */
    .result-card {
        padding: 1.5rem;
        border-radius: 12px;
        background: rgba(38, 39, 48, 0.6);
        border-left: 5px solid #00D26A;
        margin-top: 1.2rem;
    }
    
    /* Login card container */
    [data-testid="stForm"] {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# ----------------- AUTHENTICATION -----------------
USER_CREDENTIALS = {
    "RehanRathod2513": "ikra@786",
    "abdullah": "ikra@786"
}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""

def login():
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>🛍️ Customer Intelligence Portal</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888;'>Secure access for ML insights and segmentation</p>", unsafe_allow_html=True)
        st.write("")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="e.g. admin")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submit = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit:
                if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")

def logout():
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.rerun()

# ----------------- MAIN APPLICATION -----------------
if not st.session_state["authenticated"]:
    login()
else:
    # Sidebar Navigation & User Info
    with st.sidebar:
        st.markdown(f"👤 **Logged in as:** `{st.session_state['username']}`")
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
        model = joblib.load("customer_segmentation_model.pkl")
        scaler = joblib.load("customer_scaler.pkl")
        segment_names = joblib.load("segment_names.pkl")
        return model, scaler, segment_names

    model, scaler, segment_names = load_artifacts()

    # View 1: Customer Segment Predictor
    if page == "Customer Segment Predictor":
        st.markdown('<div class="hero-title">Predict Customer Segment</div>', unsafe_allow_html=True)
        st.caption("Classify live user behavior profiles dynamically using the trained K-Means model.")
        st.divider()

        # Inputs in responsive columns
        c1, c2 = st.columns(2)
        with c1:
            total_spend = st.number_input("Total Spend ($)", min_value=0.0, value=1000.0, step=50.0)
            items_purchased = st.number_input("Items Purchased", min_value=1, value=10, step=1)
            
        with c2:
            avg_rating = st.slider("Average Rating", min_value=1.0, max_value=5.0, value=4.0, step=0.1)
            recency = st.number_input("Days Since Last Purchase", min_value=0, value=20, step=1)

        if st.button("Predict Segment", type="primary", use_container_width=True):
            # Scale & Predict
            input_data = np.array([[total_spend, items_purchased, avg_rating, recency]])
            scaled_features = scaler.transform(input_data)
            cluster_id = model.predict(scaled_features)[0]
            cluster_label = segment_names.get(cluster_id, f"Cluster {cluster_id}")

            # Highlighted result card
            st.markdown(f"""
            <div class="result-card">
                <span style="color: #888; font-size: 0.9rem;">Prediction Output</span>
                <h3 style="margin: 0.3rem 0; color: #00D26A;">🎯 {cluster_label}</h3>
                <p style="margin: 0; color: #ccc; font-size: 0.85rem;">Cluster ID: #{cluster_id} | High affinity to repeat engagement campaigns.</p>
            </div>
            """, unsafe_allow_html=True)

    elif page == "Dashboard":
        st.markdown('<div class="hero-title">Analytics Dashboard</div>', unsafe_allow_html=True)
        st.caption("Comprehensive overview of customer behavior, spending patterns, and segment distributions.")
        st.divider()

        @st.cache_data
        def load_and_process_data():
            data = pd.read_csv("customer_intelligence_data.csv")
            
            # Predict segments if not already present in the raw CSV
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
    elif page == "Customer Explorer":
        st.markdown('<div class="hero-title">Customer Explorer</div>', unsafe_allow_html=True)
        st.info("Search, filter, and inspect individual customer records.")
