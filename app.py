import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="NEURAL METRICS // Customer Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling: Cyberpunk Glassmorphism, Animated Glowing Gradients & Neon HUD
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');

    .stApp {
        background: radial-gradient(circle at 10% 20%, #0d1117 0%, #05070a 90%);
        color: #e6edf3;
        font-family: 'Rajdhani', sans-serif;
    }

    h1, h2, h3, .hero-title {
        font-family: 'Orbitron', monospace !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #00ff87 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hud-card {
        background: rgba(13, 17, 23, 0.7);
        border: 1px solid rgba(0, 242, 254, 0.2);
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.08), inset 0 0 15px rgba(0, 242, 254, 0.03);
        border-radius: 12px;
        padding: 1.2rem;
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
        transition: border 0.3s ease, box-shadow 0.3s ease;
    }
    .hud-card:hover {
        border: 1px solid rgba(0, 255, 135, 0.5);
        box-shadow: 0 0 20px rgba(0, 255, 135, 0.2);
    }

    .hud-metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #8b949e;
    }
    .hud-metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: #00f2fe;
        margin-top: 0.2rem;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
    }

    .cyber-separator {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.5rem 0;
        color: #00f2fe;
        font-family: 'Orbitron', monospace;
        font-size: 0.75rem;
        letter-spacing: 2px;
    }
    .cyber-separator::before, .cyber-separator::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid rgba(0, 242, 254, 0.25);
    }
    .cyber-separator:not(:empty)::before { margin-right: 1em; }
    .cyber-separator:not(:empty)::after { margin-left: 1em; }

    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', monospace;
        color: #00ff87 !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- AUTHENTICATION -----------------
if "user_credentials" not in st.session_state:
    st.session_state["user_credentials"] = {
        "RehanRathod2513": "ikra@786",
        "abdullah": "ikra@786"
    }

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""

def login():
    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>⚡ NEURAL METRICS</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #00f2fe; letter-spacing: 1px;'>// QUANTUM CUSTOMER CLASSIFICATION SUITE</p>", unsafe_allow_html=True)
        
        with st.container(border=True):
            if st.button("🌐 Connect via SSO Matrix", use_container_width=True):
                st.session_state["authenticated"] = True
                st.session_state["username"] = "Matrix_Agent"
                st.rerun()

            st.markdown('<div class="cyber-separator">SECURE PROTOCOL ACCESS</div>', unsafe_allow_html=True)

            tab_signin, tab_signup = st.tabs(["🔑 DECRYPT / LOGIN", "📝 REGISTER NODE"])

            with tab_signin:
                with st.form("login_form"):
                    username = st.text_input("Identity Handle", placeholder="e.g. admin")
                    password = st.text_input("Access Cipher", type="password", placeholder="••••••••")
                    submit = st.form_submit_button("AUTHENTICATE SYSTEM", use_container_width=True)
                    
                    if submit:
                        credentials = st.session_state["user_credentials"]
                        if username in credentials and credentials[username] == password:
                            st.session_state["authenticated"] = True
                            st.session_state["username"] = username
                            st.rerun()
                        else:
                            st.error("ACCESS DENIED: Invalid Cipher Signature")

            with tab_signup:
                with st.form("signup_form"):
                    new_user = st.text_input("Assign Identity Handle", placeholder="e.g. agent_01")
                    new_pass = st.text_input("Set Access Cipher", type="password", placeholder="••••••••")
                    confirm_pass = st.text_input("Confirm Access Cipher", type="password", placeholder="••••••••")
                    signup_submit = st.form_submit_button("REGISTER CREDENTIALS", use_container_width=True)

                    if signup_submit:
                        clean_user = new_user.strip()
                        credentials = st.session_state["user_credentials"]
                        
                        if not clean_user or not new_pass:
                            st.warning("All data vectors required.")
                        elif clean_user in credentials:
                            st.error("Handle collision: Identity already in registry.")
                        elif new_pass != confirm_pass:
                            st.error("Cipher checksum mismatch.")
                        elif len(new_pass) < 6:
                            st.warning("Cipher complexity must exceed 5 bytes.")
                        else:
                            st.session_state["user_credentials"][clean_user] = new_pass
                            st.success("Identity node registered. Proceed to Decrypt.")

def logout():
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
    st.rerun()

# ----------------- MAIN APPLICATION -----------------
if not st.session_state["authenticated"]:
    login()
else:
    with st.sidebar:
        st.markdown(f"🟢 **OPERATOR:** `{st.session_state['username']}`")
        st.markdown("<p style='font-size:0.75rem; color:#00ff87;'>NODE STATUS: SYNCHRONIZED</p>", unsafe_allow_html=True)
        if st.button("TERMINATE SESSION", use_container_width=True):
            logout()
        st.divider()
        
        st.markdown("<p style='letter-spacing:2px; font-size:0.8rem; color:#8b949e;'>CORE MODULES</p>", unsafe_allow_html=True)
        page = st.radio(
            "Navigation",
            ["⚡ Neural Segment Predictor", "📊 Quantum Dashboard", "🔍 Cyber Customer Explorer"],
            label_visibility="collapsed"
        )

    @st.cache_resource
    def load_artifacts():
        model = joblib.load("customer_segmentation_model.pkl")
        scaler = joblib.load("customer_scaler.pkl")
        segment_names = joblib.load("segment_names.pkl")
        return model, scaler, segment_names

    model, scaler, segment_names = load_artifacts()

    # ----------------- VIEW 1: PREDICTOR -----------------
    if page == "⚡ Neural Segment Predictor":
        st.markdown('<h1>// NEURAL SEGMENT CLASSIFIER</h1>', unsafe_allow_html=True)
        st.caption("Live behavioral clustering, scenario simulation, and multi-node batch inference.")
        st.divider()

        mode_tab1, mode_tab2 = st.tabs(["🎯 SINGLE NODE SIMULATOR", "📂 BATCH CSV CLUSTER INGESTION"])

        with mode_tab1:
            st.markdown("##### ⚡ Quick Persona Presets")
            p_col1, p_col2, p_col3, p_col4 = st.columns(4)
            
            if "preset_spend" not in st.session_state:
                st.session_state["preset_spend"] = 1250.0
                st.session_state["preset_items"] = 12
                st.session_state["preset_rating"] = 4.2
                st.session_state["preset_recency"] = 14

            if p_col1.button("👑 Whale / High VIP", use_container_width=True):
                st.session_state["preset_spend"] = 2800.0
                st.session_state["preset_items"] = 28
                st.session_state["preset_rating"] = 4.9
                st.session_state["preset_recency"] = 4
                st.rerun()

            if p_col2.button("⚠️ Dormant Churn Risk", use_container_width=True):
                st.session_state["preset_spend"] = 350.0
                st.session_state["preset_items"] = 3
                st.session_state["preset_rating"] = 2.1
                st.session_state["preset_recency"] = 85
                st.rerun()

            if p_col3.button("🛍️ Frequent Low-Ticket", use_container_width=True):
                st.session_state["preset_spend"] = 650.0
                st.session_state["preset_items"] = 18
                st.session_state["preset_rating"] = 4.1
                st.session_state["preset_recency"] = 7
                st.rerun()

            if p_col4.button("🌱 New Onboarded Node", use_container_width=True):
                st.session_state["preset_spend"] = 150.0
                st.session_state["preset_items"] = 2
                st.session_state["preset_rating"] = 3.5
                st.session_state["preset_recency"] = 1
                st.rerun()

            st.write("")

            c1, c2 = st.columns(2)
            with c1:
                total_spend = st.number_input(
                    "Total Lifetime Value ($)", 
                    min_value=0.0, 
                    max_value=10000.0,
                    value=float(st.session_state["preset_spend"]), 
                    step=50.0
                )
                items_purchased = st.number_input(
                    "Purchased Volume Units", 
                    min_value=1, 
                    max_value=100,
                    value=int(st.session_state["preset_items"]), 
                    step=1
                )
            with c2:
                avg_rating = st.slider(
                    "Sentiment Rating Index", 
                    min_value=1.0, 
                    max_value=5.0, 
                    value=float(st.session_state["preset_rating"]), 
                    step=0.1
                )
                recency = st.number_input(
                    "Temporal Recency (Days Inactive)", 
                    min_value=0, 
                    max_value=365,
                    value=int(st.session_state["preset_recency"]), 
                    step=1
                )

            predict_btn = st.button("EXECUTE NEURAL INFERENCE", type="primary", use_container_width=True)

            if predict_btn or "last_prediction" in st.session_state:
                st.session_state["last_prediction"] = True
                
                input_data = np.array([[total_spend, items_purchased, avg_rating, recency]])
                scaled_features = scaler.transform(input_data)
                cluster_id = model.predict(scaled_features)[0]
                cluster_label = segment_names.get(cluster_id, f"Cluster #{cluster_id}")
                
                centroids = model.cluster_centers_
                distances = np.linalg.norm(centroids - scaled_features, axis=1)
                closest_confidence = max(0, 100 - (distances[cluster_id] * 25))

                st.write("")
                st.markdown(f"""
                <div class="hud-card" style="border-left: 4px solid #00ff87;">
                    <div class="hud-metric-label">IDENTIFIED BEHAVIORAL MATRIX</div>
                    <div class="hud-metric-value" style="color: #00ff87;">{cluster_label}</div>
                    <p style="color: #8b949e; margin-top: 0.5rem; font-size: 0.9rem;">
                        Cluster Vector ID: <span style="color:#00f2fe;">0x0{cluster_id}</span> | 
                        Cluster Affinity: <span style="color:#00ff87;">{closest_confidence:.1f}%</span> | 
                        Spatial Distortion: <span style="color:#ff007f;">{distances[cluster_id]:.3f}</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)

                tab_radar, tab_simulation, tab_proximity, tab_strategy = st.tabs([
                    "📡 RADAR PROFILE", 
                    "🧪 WHAT-IF SANDBOX", 
                    "🌌 CENTROID DISTANCES", 
                    "💾 DIRECTIVE ACTION PLAN"
                ])

                with tab_radar:
                    categories = ['Spend Density', 'Basket Volume', 'Sentiment Index', 'Engagement Velocity']
                    spend_score = min(100, (total_spend / 2500.0) * 100)
                    basket_score = min(100, (items_purchased / 25.0) * 100)
                    rating_score = (avg_rating / 5.0) * 100
                    recency_score = max(0, 100 - (recency / 90.0 * 100))
                    values = [spend_score, basket_score, rating_score, recency_score]

                    fig_radar = go.Figure()
                    fig_radar.add_trace(go.Scatterpolar(
                        r=values + [values[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        fillcolor='rgba(0, 242, 254, 0.25)',
                        line=dict(color='#00f2fe', width=2),
                        name='Current Node'
                    ))
                    fig_radar.update_layout(
                        polar=dict(
                            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)"),
                            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", linecolor="rgba(0, 242, 254, 0.5)")
                        ),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        showlegend=False,
                        font=dict(color="#00f2fe", family="Rajdhani")
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)

                with tab_simulation:
                    st.markdown("##### 🧪 Real-Time What-If Upsell / Retention Simulator")
                    sim_col1, sim_col2 = st.columns(2)
                    with sim_col1:
                        add_spend = st.slider("Simulate Additional Spend ($)", 0.0, 2000.0, 250.0, step=25.0)
                        add_items = st.slider("Simulate Additional Items", 0, 15, 2, step=1)
                    with sim_col2:
                        reduce_recency = st.slider("Simulated Re-engagement (Days Subtracted)", 0, int(recency), min(5, int(recency)), step=1)

                    simulated_spend = total_spend + add_spend
                    simulated_items = items_purchased + add_items
                    simulated_recency = max(0, recency - reduce_recency)
                    
                    sim_input = np.array([[simulated_spend, simulated_items, avg_rating, simulated_recency]])
                    sim_scaled = scaler.transform(sim_input)
                    sim_cluster_id = model.predict(sim_scaled)[0]
                    sim_label = segment_names.get(sim_cluster_id, f"Cluster #{sim_cluster_id}")

                    st.markdown(f"""
                    <div style="background: rgba(0, 242, 254, 0.05); border: 1px dashed #00f2fe; border-radius: 8px; padding: 1rem; margin-top: 0.5rem;">
                        <span style="color:#8b949e; font-size:0.85rem;">PREDICTED SHIFT AFTER UPGRADE:</span>
                        <h3 style="color:#00ff87; margin:0.2rem 0;">{sim_label}</h3>
                        <p style="color:#ccc; font-size:0.9rem; margin:0;">
                            Simulated Lifetime Value: <b>${simulated_spend:,.2f}</b> | Basket: <b>{simulated_items} units</b> | Recency: <b>{simulated_recency} days</b>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                with tab_proximity:
                    st.markdown("##### 🌌 Distance to All Cluster Centers")
                    dist_df = pd.DataFrame({
                        "Cluster": [segment_names.get(i, f"Cluster {i}") for i in range(len(centroids))],
                        "Normalized Distance": distances
                    }).sort_values("Normalized Distance")

                    fig_dist = px.bar(
                        dist_df,
                        x="Normalized Distance",
                        y="Cluster",
                        orientation="h",
                        color="Normalized Distance",
                        color_continuous_scale=[[0, "#00ff87"], [1, "#ff007f"]],
                        template="plotly_dark"
                    )
                    fig_dist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10))
                    st.plotly_chart(fig_dist, use_container_width=True)

                with tab_strategy:
                    if "High" in cluster_label or "VIP" in cluster_label or total_spend > 1500:
                        st.success("🌟 PRIORITY HIGH-CAPITAL NODE")
                        st.markdown("""
                        * **Direct Protocol:** Provision exclusive concierge support channel.
                        * **Upsell Vector:** Dispatch automated alpha access to upcoming catalog releases.
                        * **Retention Guard:** Alert account executive if inactivity exceeds 20 days.
                        """)
                    elif recency > 45:
                        st.error("⚠️ HIGH-LATENCY AT-RISK NODE")
                        st.markdown("""
                        * **Re-engagement Trigger:** Deploy targeted reactivation incentives with 20% discount.
                        * **Telemetry Diagnostic:** Dispatch 1-click sentiment diagnostic workflow.
                        * **Multi-Channel Sync:** Trigger SMS reminders.
                        """)
                    else:
                        st.info("📈 EXPANSION & GROWTH VECTOR")
                        st.markdown("""
                        * **Cross-Sell Stream:** Surface algorithmic product associations based on prior carts.
                        * **Cadence Optimization:** Implement recurring loyalty rewards.
                        * **Review Incentive:** Offer loyalty points in exchange for verified feedback.
                        """)

        with mode_tab2:
            st.markdown("##### 📂 Upload Batch Customer CSV for Neural Classification")
            uploaded_file = st.file_uploader("Upload CSV matching required features (Total Spend, Items Purchased, Average Rating, Days Since Last Purchase)", type=["csv"])
            
            if uploaded_file is not None:
                batch_df = pd.read_csv(uploaded_file)
                req_cols = ["Total Spend", "Items Purchased", "Average Rating", "Days Since Last Purchase"]
                
                if all(c in batch_df.columns for c in req_cols):
                    b_scaled = scaler.transform(batch_df[req_cols])
                    b_preds = model.predict(b_scaled)
                    batch_df["Predicted_Cluster_ID"] = b_preds
                    batch_df["Predicted_Segment"] = [segment_names.get(c, f"Cluster {c}") for c in b_preds]

                    st.success(f"Successfully processed {len(batch_df):,} customer records!")
                    st.dataframe(batch_df.head(10), use_container_width=True)

                    csv_out = batch_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 DOWNLOAD ENRICHED CLASSIFICATIONS CSV",
                        data=csv_out,
                        file_name="neural_batch_classified.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.error(f"Missing required columns! File must include: `{req_cols}`")

    # ----------------- VIEW 2: QUANTUM DASHBOARD -----------------
    elif page == "📊 Quantum Dashboard":
        st.markdown('<h1>// QUANTUM TELEMETRY DASHBOARD</h1>', unsafe_allow_html=True)
        st.caption("Live spatial clustering, macro telemetry, correlation heatmaps, and segment benchmark comparisons.")
        st.divider()

        @st.cache_data
        def load_and_process_data():
            data = pd.read_csv("customer_intelligence_data.csv")
            feature_cols = ["Total Spend", "Items Purchased", "Average Rating", "Days Since Last Purchase"]
            if all(col in data.columns for col in feature_cols):
                scaled_vals = scaler.transform(data[feature_cols])
                cluster_preds = model.predict(scaled_vals)
                data["Segment"] = [segment_names.get(c, f"Cluster {c}") for c in cluster_preds]
            return data

        try:
            df = load_and_process_data()

            m1, m2, m3, m4, m5, m6 = st.columns(6)
            with m1:
                st.markdown(f"""<div class="hud-card"><div class="hud-metric-label">TOTAL NODES</div><div class="hud-metric-value">{len(df):,}</div></div>""", unsafe_allow_html=True)
            with m2:
                total_rev = df['Total Spend'].sum()
                st.markdown(f"""<div class="hud-card"><div class="hud-metric-label">TOTAL VOLUME</div><div class="hud-metric-value">${total_rev/1e6:.2f}M</div></div>""", unsafe_allow_html=True)
            with m3:
                st.markdown(f"""<div class="hud-card"><div class="hud-metric-label">MEAN YIELD</div><div class="hud-metric-value">${df['Total Spend'].mean():,.0f}</div></div>""", unsafe_allow_html=True)
            with m4:
                avg_val_item = (df['Total Spend'] / df['Items Purchased'].replace(0, 1)).mean()
                st.markdown(f"""<div class="hud-card"><div class="hud-metric-label">AVG UNIT VAL</div><div class="hud-metric-value">${avg_val_item:.1f}</div></div>""", unsafe_allow_html=True)
            with m5:
                st.markdown(f"""<div class="hud-card"><div class="hud-metric-label">SENTIMENT</div><div class="hud-metric-value">{df['Average Rating'].mean():.2f} ★</div></div>""", unsafe_allow_html=True)
            with m6:
                churn_risk_pct = (len(df[df['Days Since Last Purchase'] > 45]) / len(df)) * 100
                st.markdown(f"""<div class="hud-card"><div class="hud-metric-label">LATENCY RISK</div><div class="hud-metric-value" style="color:#ff007f;">{churn_risk_pct:.1f}%</div></div>""", unsafe_allow_html=True)

            st.write("")

            st.subheader("🌐 3D Spatial Vector Clustering")
            fig_3d = px.scatter_3d(
                df,
                x='Total Spend',
                y='Items Purchased',
                z='Days Since Last Purchase',
                color='Segment',
                size='Average Rating',
                color_discrete_sequence=['#00f2fe', '#00ff87', '#ff007f', '#ffe600', '#7928ca'],
                template="plotly_dark",
                opacity=0.85
            )
            fig_3d.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=10, b=10, l=10, r=10),
                scene=dict(
                    xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
                    yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
                    zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)")
                )
            )
            st.plotly_chart(fig_3d, use_container_width=True)

            st.divider()

            c_left, c_right = st.columns(2)
            with c_left:
                st.subheader("🧬 Cohort Revenue vs Node Count")
                cohort_summary = df.groupby("Segment").agg(
                    Total_Spend=("Total Spend", "sum"),
                    Node_Count=("Total Spend", "count")
                ).reset_index()

                fig_dual = go.Figure()
                fig_dual.add_trace(go.Bar(
                    x=cohort_summary["Segment"],
                    y=cohort_summary["Total_Spend"],
                    name="Gross Revenue ($)",
                    marker_color="#00f2fe",
                    opacity=0.85
                ))
                fig_dual.add_trace(go.Scatter(
                    x=cohort_summary["Segment"],
                    y=cohort_summary["Node_Count"],
                    name="Node Count",
                    yaxis="y2",
                    mode="lines+markers",
                    line=dict(color="#00ff87", width=3),
                    marker=dict(size=8, symbol="diamond")
                ))
                fig_dual.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    yaxis=dict(title="Gross Revenue ($)", gridcolor="rgba(255,255,255,0.1)"),
                    yaxis2=dict(title="Node Count", overlaying="y", side="right"),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(t=20, b=20, l=10, r=10),
                    template="plotly_dark"
                )
                st.plotly_chart(fig_dual, use_container_width=True)

            with c_right:
                st.subheader("⚡ Multi-Cluster Feature Correlation")
                numeric_cols = ["Total Spend", "Items Purchased", "Average Rating", "Days Since Last Purchase"]
                corr_matrix = df[numeric_cols].corr()
                fig_corr = px.imshow(
                    corr_matrix,
                    text_auto=".2f",
                    aspect="auto",
                    color_continuous_scale=[[0, "#05070a"], [0.5, "#00f2fe"], [1, "#00ff87"]],
                    template="plotly_dark"
                )
                fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20, l=10, r=10))
                st.plotly_chart(fig_corr, use_container_width=True)

            st.divider()

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                st.subheader("💎 Spend vs Recency Density Contours")
                fig_density_contour = px.density_contour(
                    df,
                    x="Days Since Last Purchase",
                    y="Total Spend",
                    color="Segment",
                    marginal_x="histogram",
                    marginal_y="box",
                    color_discrete_sequence=['#00f2fe', '#00ff87', '#ff007f', '#ffe600', '#7928ca'],
                    template="plotly_dark"
                )
                fig_density_contour.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20, l=10, r=10))
                st.plotly_chart(fig_density_contour, use_container_width=True)

            with col_b2:
                st.subheader("🎯 Cross-Segment Mean Radar Profiles")
                cluster_means = df.groupby("Segment")[numeric_cols].mean()
                norm_means = (cluster_means - cluster_means.min()) / (cluster_means.max() - cluster_means.min() + 1e-6) * 100
                
                fig_multi_radar = go.Figure()
                radar_cats = list(norm_means.columns)
                colors = ['#00f2fe', '#00ff87', '#ff007f', '#ffe600', '#7928ca']
                
                for idx, (seg_name, row) in enumerate(norm_means.iterrows()):
                    fig_multi_radar.add_trace(go.Scatterpolar(
                        r=row.tolist() + [row.tolist()[0]],
                        theta=radar_cats + [radar_cats[0]],
                        fill='toself',
                        name=seg_name,
                        line=dict(color=colors[idx % len(colors)]),
                        opacity=0.6
                    ))
                
                fig_multi_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)"),
                        angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    template="plotly_dark",
                    margin=dict(t=20, b=20, l=10, r=10),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_multi_radar, use_container_width=True)

            st.divider()

            st.subheader("📋 Cohort Benchmark Breakdown")
            benchmark_table = df.groupby("Segment").agg(
                Nodes=("Total Spend", "count"),
                Avg_Spend=("Total Spend", "mean"),
                Avg_Items=("Items Purchased", "mean"),
                Avg_Rating=("Average Rating", "mean"),
                Avg_Recency=("Days Since Last Purchase", "mean")
            ).reset_index()

            st.dataframe(
                benchmark_table,
                use_container_width=True,
                column_config={
                    "Avg_Spend": st.column_config.NumberColumn("Avg Spend", format="$%.2f"),
                    "Avg_Items": st.column_config.NumberColumn("Avg Basket", format="%.1f units"),
                    "Avg_Rating": st.column_config.NumberColumn("Avg Rating", format="%.2f ★"),
                    "Avg_Recency": st.column_config.NumberColumn("Avg Recency", format="%.1f days")
                }
            )

        except FileNotFoundError:
            st.error("`customer_intelligence_data.csv` was not found.")

    # ----------------- VIEW 3: CYBER EXPLORER -----------------
    elif page == "🔍 Cyber Customer Explorer":
        st.markdown('<h1>// CYBER NODE EXPLORER</h1>', unsafe_allow_html=True)
        st.caption("Deep memory inspection and vector slicing across raw client records.")
        st.divider()

        @st.cache_data
        def load_explorer_data():
            data = pd.read_csv("customer_intelligence_data.csv")
            feature_cols = ["Total Spend", "Items Purchased", "Average Rating", "Days Since Last Purchase"]
            if all(col in data.columns for col in feature_cols):
                scaled_vals = scaler.transform(data[feature_cols])
                cluster_preds = model.predict(scaled_vals)
                data["Segment"] = [segment_names.get(c, f"Cluster {c}") for c in cluster_preds]
            return data

        try:
            df = load_explorer_data()

            f1, f2, f3 = st.columns([1.5, 2, 2])
            with f1:
                available_segments = ["All Clusters"] + sorted(list(df["Segment"].dropna().unique())) if "Segment" in df.columns else ["All Clusters"]
                selected_segment = st.selectbox("Isolate Cluster Subspace", available_segments)
            with f2:
                spend_range = st.slider(
                    "Spend Bandwidth ($)",
                    min_value=float(df["Total Spend"].min()),
                    max_value=float(df["Total Spend"].max()),
                    value=(float(df["Total Spend"].min()), float(df["Total Spend"].max())),
                    step=50.0
                )
            with f3:
                min_rating, max_rating = st.slider(
                    "Sentiment Bounds",
                    min_value=1.0,
                    max_value=5.0,
                    value=(1.0, 5.0),
                    step=0.1
                )

            filtered_df = df[
                (df["Total Spend"] >= spend_range[0]) & 
                (df["Total Spend"] <= spend_range[1]) &
                (df["Average Rating"] >= min_rating) &
                (df["Average Rating"] <= max_rating)
            ]

            if selected_segment != "All Clusters" and "Segment" in df.columns:
                filtered_df = filtered_df[filtered_df["Segment"] == selected_segment]

            st.markdown(f"**FILTER ACTIVE:** Sliced **{len(filtered_df):,}** of **{len(df):,}** node vectors.")

            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=300,
                column_config={
                    "Total Spend": st.column_config.NumberColumn("Total Spend", format="$%.2f"),
                    "Average Rating": st.column_config.NumberColumn("Rating", format="%.2f ★"),
                    "Items Purchased": st.column_config.NumberColumn("Items Purchased", format="%d units"),
                    "Days Since Last Purchase": st.column_config.NumberColumn("Recency", format="%d d")
                }
            )

            st.divider()

            st.subheader("🔬 Single Node Telemetry")
            if not filtered_df.empty:
                selected_idx = st.selectbox(
                    "Select Vector Memory Address",
                    options=filtered_df.index,
                    format_func=lambda x: f"Node #{x:04d} | {filtered_df.loc[x, 'Segment']} (${filtered_df.loc[x, 'Total Spend']:,.2f})"
                )
                node = filtered_df.loc[selected_idx]

                n1, n2, n3, n4, n5 = st.columns(5)
                n1.metric("Lifetime Yield", f"${node['Total Spend']:,.2f}")
                n2.metric("Basket Volume", f"{int(node['Items Purchased'])} units")
                n3.metric("Sentiment Score", f"{node['Average Rating']:.2f} ★")
                n4.metric("Cycle Latency", f"{int(node['Days Since Last Purchase'])} days")
                n5.metric("Segment Vector", f"{node.get('Segment', 'N/A')}")
            else:
                st.warning("No node vectors match the active filter bandwidth.")

        except FileNotFoundError:
            st.error("`customer_intelligence_data.csv` was not found.")
