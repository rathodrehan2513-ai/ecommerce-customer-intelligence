
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(
    page_title="Customer Intelligence Platform",
    page_icon="🛍️",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("customer_intelligence_data.csv")

@st.cache_resource
def load_model_files():
    model = joblib.load("customer_segmentation_model.pkl")
    scaler = joblib.load("customer_scaler.pkl")
    labels = joblib.load("segment_names.pkl")
    return model, scaler, labels

df = load_data()
kmeans, scaler, segment_names = load_model_files()

st.title("🛍️ E-Commerce Customer Intelligence Platform")
st.caption("Machine-learning customer segmentation and business analytics")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Customer Segment Predictor", "Customer Explorer"]
)

if page == "Dashboard":
    total_customers = len(df)
    total_spend = df["Total Spend"].sum()
    average_spend = df["Total Spend"].mean()
    vip_customers = (df["Customer Segment"] == "VIP Customers").sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Recorded Customer Spend", f"${total_spend:,.0f}")
    col3.metric("Average Customer Spend", f"${average_spend:,.2f}")
    col4.metric("VIP Customers", f"{vip_customers:,}")

    st.subheader("Customer Segment Distribution")
    segment_counts = df["Customer Segment"].value_counts().reset_index()
    segment_counts.columns = ["Customer Segment", "Customers"]

    chart1 = px.bar(
        segment_counts,
        x="Customer Segment",
        y="Customers",
        color="Customer Segment",
        text="Customers"
    )
    st.plotly_chart(chart1, use_container_width=True)

    st.subheader("Spending vs Purchase Recency")
    chart2 = px.scatter(
        df,
        x="Total Spend",
        y="Days Since Last Purchase",
        color="Customer Segment",
        size="Items Purchased",
        hover_data=["Customer ID", "Membership Type", "Average Rating"],
        title="Customer Behaviour Segments"
    )
    st.plotly_chart(chart2, use_container_width=True)

elif page == "Customer Segment Predictor":
    st.subheader("Predict a Customer Segment")
    st.write("Enter customer behaviour details to classify the customer with K-Means.")

    col1, col2 = st.columns(2)

    with col1:
        total_spend = st.number_input("Total Spend", min_value=0.0, value=1000.0)
        items_purchased = st.number_input("Items Purchased", min_value=0, value=10)

    with col2:
        average_rating = st.slider("Average Rating", 1.0, 5.0, 4.0, 0.1)
        days_since_purchase = st.number_input(
            "Days Since Last Purchase",
            min_value=0,
            value=20
        )

    if st.button("Predict Customer Segment", type="primary"):
        customer = pd.DataFrame([{
            "Total Spend": total_spend,
            "Items Purchased": items_purchased,
            "Average Rating": average_rating,
            "Days Since Last Purchase": days_since_purchase
        }])

        scaled_customer = scaler.transform(customer)
        cluster = kmeans.predict(scaled_customer)[0]
        predicted_segment = segment_names[cluster]

        st.success(f"Predicted Segment: {predicted_segment}")

elif page == "Customer Explorer":
    st.subheader("Explore Customers")

    selected_segment = st.selectbox(
        "Filter by customer segment",
        ["All"] + sorted(df["Customer Segment"].unique().tolist())
    )

    filtered_df = df.copy()

    if selected_segment != "All":
        filtered_df = filtered_df[
            filtered_df["Customer Segment"] == selected_segment
        ]

    st.dataframe(filtered_df, use_container_width=True)
