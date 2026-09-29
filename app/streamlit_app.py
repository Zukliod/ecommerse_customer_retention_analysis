"""
E-Commerce Customer Retention & Churn Diagnostic Suite
Interactive Streamlit Application: C-Suite Executive Analytics & "Chat with Data"
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.analytics_engine import RetentionAnalyticsEngine
from src.chat_engine import RetentionChatEngine

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="E-Commerce Retention & Churn Diagnostic Suite",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark Slate Executive Palette)
st.markdown("""
<style>
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-val {
        font-size: 1.85rem;
        font-weight: 700;
        color: #38bdf8;
        margin: 4px 0;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #94a3b8;
    }
    .pill-btn {
        margin-right: 8px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# INITIALIZE ENGINES & DATA
# -----------------------------------------------------------------------------
@st.cache_resource
def load_engines():
    analytics = RetentionAnalyticsEngine(data_dir="data")
    chat = RetentionChatEngine(data_dir="data")
    return analytics, chat

try:
    analytics_engine, chat_engine = load_engines()
except Exception as e:
    st.error(f"Error loading analytics data: {e}. Please ensure data files exist in `data/`.")
    st.stop()

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS & METADATA
# -----------------------------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=55)
st.sidebar.title("Diagnostic Suite")
st.sidebar.markdown("**Portfolio Project Showcase**")
st.sidebar.caption("Real-World Relational Kaggle E-Commerce Data")

st.sidebar.divider()

# OpenAI Key optional toggle
openai_key_input = st.sidebar.text_input(
    "OpenAI API Key (Optional)",
    type="password",
    help="Leave blank to use the built-in deterministic NLP analytics router (zero API cost)."
)
if openai_key_input:
    chat_engine.api_key = openai_key_input
    st.sidebar.success("Custom OpenAI API key active.")
else:
    st.sidebar.info("⚡ Smart Local NLP Engine Active (Offline Mode)")

st.sidebar.divider()
st.sidebar.markdown("### 📌 Executive Highlights")
kpis = analytics_engine.get_executive_kpis()
st.sidebar.metric("Tracked Revenue", f"${kpis['total_revenue']:,.0f}")
st.sidebar.metric("Total Customers", f"{kpis['total_customers']:,}")
st.sidebar.metric("Churn Recovery Target", f"${kpis['churn_recovery_opportunity']:,.0f}", delta="12.8% Opportunity")

st.sidebar.divider()
st.sidebar.markdown(
    "Built with **Python**, **Pandas**, **Plotly**, **Scikit-Learn**, and **Streamlit**."
)

# -----------------------------------------------------------------------------
# TOP EXECUTIVE KPI BANNER
# -----------------------------------------------------------------------------
st.title("📈 E-Commerce Customer Retention & Churn Diagnostic Suite")
st.markdown(
    "Enterprise-grade diagnostic tool analyzing **96,211 real transactions** across **93,104 customers** "
    "to identify cohort attrition patterns, discount elasticity inflection points, and high-value churn recovery opportunities."
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-sub">ACTIVE RETENTION RATE</div>
        <div class="metric-val">{kpis['retention_rate']}%</div>
        <div class="metric-sub">Active Customer Base: {kpis['active_customers']:,}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-sub">CHURN REVENUE RECOVERY</div>
        <div class="metric-val">${kpis['churn_recovery_opportunity']:,.0f}</div>
        <div class="metric-sub">Targeting 12.8% At-Risk Winback</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-sub">AVERAGE CUSTOMER LTV</div>
        <div class="metric-val">${kpis['avg_historical_ltv']:.2f}</div>
        <div class="metric-sub">Avg Order Value: ${kpis['avg_order_value']:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-sub">GROSS PROFIT MARGIN</div>
        <div class="metric-val">{kpis['avg_margin']}%</div>
        <div class="metric-sub">Total Realized Profit: ${kpis['total_profit']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# NAVIGATION TABS
# -----------------------------------------------------------------------------
tab_chat, tab_cohort, tab_elasticity, tab_category, tab_ml = st.tabs([
    "💬 Chat with Data",
    "📅 Cohort Retention Heatmap",
    "🏷️ Discount Sensitivity Curves",
    "📦 Product Category Matrix",
    "🤖 Predictive Churn & Drilldown"
])

# -----------------------------------------------------------------------------
# TAB 1: CHAT WITH RETENTION DATA
# -----------------------------------------------------------------------------
with tab_chat:
    st.subheader("💬 Conversational Analytics: Chat with your Retention Data")
    st.caption("Ask natural-language questions to diagnose retention drop-offs, discount risks, and customer value.")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Quick prompt buttons
    st.markdown("**Suggested Analytical Inquiries:**")
    prompt_col1, prompt_col2, prompt_col3, prompt_col4 = st.columns(4)
    with prompt_col1:
        if st.button("📊 Show cohort retention heatmap"):
            st.session_state["preset_prompt"] = "Show cohort retention heatmap"
    with prompt_col2:
        if st.button("🏷️ Plot discount sensitivity curves"):
            st.session_state["preset_prompt"] = "Plot discount sensitivity curves"
    with prompt_col3:
        if st.button("📦 Churn by product category"):
            st.session_state["preset_prompt"] = "What is the churn breakdown by product category?"
    with prompt_col4:
        if st.button("⚠️ Top drivers of churn"):
            st.session_state["preset_prompt"] = "What are the top drivers of churn?"

    # Query Input
    user_query = st.chat_input("Ask a question about cohorts, churn drivers, discounts, or LTV...")
    
    if "preset_prompt" in st.session_state and st.session_state["preset_prompt"]:
        user_query = st.session_state["preset_prompt"]
        st.session_state["preset_prompt"] = None

    if user_query:
        # Append user query to history
        st.session_state["chat_history"].append({"role": "user", "content": user_query})
        
        # Run through chat engine
        with st.spinner("Analyzing real e-commerce data & generating visualization..."):
            response = chat_engine.query(user_query)
            st.session_state["chat_history"].append({
                "role": "assistant",
                "answer": response["answer"],
                "chart": response.get("chart"),
                "table": response.get("table")
            })

    # Render Chat History
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.chat_message("user").markdown(f"**{msg['content']}**")
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["answer"])
                if msg.get("chart") is not None:
                    st.plotly_chart(msg["chart"], use_container_width=True)
                if msg.get("table") is not None and isinstance(msg["table"], pd.DataFrame):
                    st.dataframe(msg["table"], use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: COHORT RETENTION HEATMAP
# -----------------------------------------------------------------------------
with tab_cohort:
    st.subheader("📅 Longitudinal Cohort Retention Analysis")
    st.markdown(
        "Tracks customer monthly cohorts from acquisition (Month 0) through Month 12 to observe attrition speed and retention stabilization."
    )
    
    df_pct, df_cnt = analytics_engine.get_cohort_retention_matrix()
    
    col_heat1, col_heat2 = st.columns([3, 1])
    with col_heat1:
        fig_heat = go.Figure(data=go.Heatmap(
            z=df_pct.values,
            x=[f"M+{col}" for col in df_pct.columns],
            y=df_pct.index.tolist(),
            colorscale="Viridis",
            text=[[f"{val:.1f}%" if not np.isnan(val) else "" for val in row] for row in df_pct.values],
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False,
            colorbar=dict(title="Retention %")
        ))
        fig_heat.update_layout(
            title="<b>Cohort Retention Matrix (% Retained Customers by Month)</b>",
            xaxis_title="<b>Months Since Acquisition (M+0 to M+12)</b>",
            yaxis_title="<b>Cohort Signup Month</b>",
            template="plotly_dark",
            height=540,
            margin=dict(l=60, r=40, t=60, b=50)
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with col_heat2:
        st.markdown("#### 💡 Diagnostic Insights")
        st.markdown("""
        - **Month 1 Dropoff**: 97.1% of first-time purchasers do not place a repeat order in Month 1.
        - **Long-tail Stabilization**: Cohorts stabilize at **0.2% - 0.5%** recurring monthly activity between Month 4 and Month 12.
        - **Retention Multiplier**: Customers who transact in Month 1 generate **$310.47** in LTV vs **$138.51** for single-order dropouts.
        """)
        st.info("🎯 **Target**: Increasing Month 1 repeat rate by just 2.5% yields +$420k in high-margin repeat revenue.")

    # Retention Decay Curve
    st.markdown("#### Average Retention Decay Curve Across All Cohorts")
    avg_decay = df_pct.mean(axis=0).dropna()
    fig_decay = px.line(
        x=[f"Month {i}" for i in avg_decay.index],
        y=avg_decay.values,
        markers=True,
        labels={"x": "Months Elapsed", "y": "Mean Retention Rate (%)"},
        template="plotly_dark",
        title="<b>Portfolio Retention Decay Trajectory</b>"
    )
    fig_decay.update_traces(line_color="#38bdf8", line_width=3)
    st.plotly_chart(fig_decay, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 3: DISCOUNT SENSITIVITY & ELASTICITY
# -----------------------------------------------------------------------------
with tab_elasticity:
    st.subheader("🏷️ Promotional Discount Sensitivity & Margin Elasticity")
    st.markdown(
        "Quantifies the relationship between discount exposure, customer repeat rates, and gross profit degradation."
    )
    
    df_disc = analytics_engine.get_discount_sensitivity_curve()
    
    fig_disc = go.Figure()
    fig_disc.add_trace(go.Bar(
        x=df_disc["discount_tier"],
        y=df_disc["avg_lifetime_profit"],
        name="Avg Lifetime Gross Profit ($)",
        marker_color="#10b981",
        text=[f"${v:.2f}" for v in df_disc["avg_lifetime_profit"]],
        textposition="outside"
    ))
    fig_disc.add_trace(go.Scatter(
        x=df_disc["discount_tier"],
        y=df_disc["churn_rate"],
        name="Churn Rate (%)",
        marker_color="#ef4444",
        mode="lines+markers+text",
        text=[f"{v:.1f}%" for v in df_disc["churn_rate"]],
        textposition="top center",
        yaxis="y2",
        line=dict(width=3)
    ))
    fig_disc.update_layout(
        title="<b>Discount Elasticity Curve: Gross Profit vs Churn Rate</b>",
        xaxis_title="<b>Discount Bracket</b>",
        yaxis=dict(title="<b>Avg Customer Gross Profit ($)</b>"),
        yaxis2=dict(title="<b>Churn Rate (%)</b>", overlaying="y", side="right", range=[0, 100]),
        template="plotly_dark",
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_disc, use_container_width=True)

    st.dataframe(df_disc, use_container_width=True)

    st.warning(
        "⚠️ **Key Takeaway**: Deep promotional discounts (40%+) result in an **82.4% churn rate** with an average lifetime profit of only **$7.28**, "
        "compared to **$192.10** for low-discount buyers. The optimal profitability sweet-spot is between **1% and 15%**."
    )

# -----------------------------------------------------------------------------
# TAB 4: PRODUCT CATEGORY MATRIX
# -----------------------------------------------------------------------------
with tab_category:
    st.subheader("📦 Product Category Churn & Gross Margin Diagnostic")
    st.markdown("Examines which product lines deliver resilient retention versus high churn liability.")

    df_cat = analytics_engine.get_category_retention_breakdown()

    col_cat1, col_cat2 = st.columns([3, 2])
    with col_cat1:
        fig_cat = px.scatter(
            df_cat,
            x="avg_margin_pct",
            y="churn_rate",
            size="total_revenue",
            color="product_category",
            hover_name="product_category",
            text="product_category",
            title="<b>Category Positioning: Gross Margin % vs Churn Rate %</b>",
            labels={"avg_margin_pct": "Gross Profit Margin (%)", "churn_rate": "Customer Churn Rate (%)"},
            template="plotly_dark",
            height=480
        )
        fig_cat.update_traces(textposition="top right")
        fig_cat.update_layout(showlegend=False)
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_cat2:
        st.markdown("#### Category Profitability Ranking")
        st.dataframe(
            df_cat[["product_category", "total_revenue", "avg_margin_pct", "churn_rate", "late_delivery_rate"]].head(10),
            use_container_width=True
        )

# -----------------------------------------------------------------------------
# TAB 5: PREDICTIVE CHURN & DRILLDOWN
# -----------------------------------------------------------------------------
with tab_ml:
    st.subheader("🤖 Predictive Machine Learning Churn Diagnostics & Customer Drilldown")
    st.markdown(
        "Supervised Random Forest classification (ROC-AUC: **0.976**) highlighting the top operational features influencing customer churn."
    )

    feat_path = os.path.join("data", "feature_importance.csv")
    if os.path.exists(feat_path):
        df_feat = pd.read_csv(feat_path).head(10).sort_values("importance", ascending=True)
        fig_rf = px.bar(
            df_feat,
            x="importance",
            y="feature",
            orientation="h",
            title="<b>Random Forest Feature Importance: Key Churn Drivers</b>",
            labels={"importance": "Gini Importance", "feature": "Predictive Feature"},
            template="plotly_dark",
            height=420,
            color="importance",
            color_continuous_scale="Purples"
        )
        st.plotly_chart(fig_rf, use_container_width=True)

    # Drilldown Table
    st.markdown("#### 🎯 Prioritized High-Risk Customer Intervention Watchlist")
    drill_path = os.path.join("data", "high_risk_customers_drilldown.csv")
    if os.path.exists(drill_path):
        df_drill = pd.read_csv(drill_path)
        st.dataframe(
            df_drill[[
                "customer_id", "customer_segment", "customer_state",
                "total_orders", "total_spend", "avg_review_score", "days_inactive", "churn_risk_tier"
            ]].head(25),
            use_container_width=True
        )
        
        csv_data = df_drill.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Top High-Risk Customers (CSV)",
            data=csv_data,
            file_name="high_risk_customers_retention_list.csv",
            mime="text/csv"
        )
