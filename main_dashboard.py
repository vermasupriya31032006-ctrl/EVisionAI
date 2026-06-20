from range_estimator import train_range_model
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from battery_trainer import load_dataset, train_health_model


# ---------------- HELPER FUNCTIONS ---------------- #

def get_risk_level(health):
    if health >= 85:
        return "🟢 SAFE"
    elif health >= 70:
        return "🟡 WARNING"
    else:
        return "🔴 CRITICAL"


def simulate_future_health(health, charge_cycles):
    future_health = health - (charge_cycles * 0.001)

    if future_health < 20:
        future_health = 20

    return future_health


def get_ai_recommendations(health, charge_cycles, temperature):

    recommendations = []

    if charge_cycles > 1200:
        recommendations.append(
            "⚠ High charge cycles detected. Reduce frequent fast charging."
        )

    if temperature > 35:
        recommendations.append(
            "🔥 High operating temperature may accelerate battery degradation."
        )

    if health < 75:
        recommendations.append(
            "🔧 Schedule battery inspection and health diagnostics."
        )

    if health >= 85:
        recommendations.append(
            "✅ Battery condition is excellent. Continue current usage pattern."
        )

    return recommendations


# ---------------- PAGE CONFIG ---------------- #

def generate_pdf_report(health, range_km, risk, recommendations):

    file_name = "EVisionAI_Report.pdf"
    doc = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("EVision AI - Battery Health Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Generated on: {datetime.now()}", styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Battery Health: {health:.2f}%", styles["Normal"]))
    content.append(Spacer(1, 8))

    content.append(Paragraph(f"Estimated Range: {range_km:.0f} km", styles["Normal"]))
    content.append(Spacer(1, 8))

    content.append(Paragraph(f"Risk Level: {risk}", styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Recommendations:", styles["Heading2"]))

    for rec in recommendations:
        content.append(Paragraph(f"- {rec}", styles["Normal"]))
        content.append(Spacer(1, 6))

    doc.build(content)

    return file_name
    st.set_page_config(
    page_title="EVision AI",
    layout="wide"
)
st.sidebar.title("🔋 EVision AI")

st.sidebar.markdown("---")

st.sidebar.info("AI Powered EV Battery Intelligence")

st.sidebar.metric("Version", "v1.0")
st.sidebar.metric("Models", "2 Active")

st.sidebar.markdown("---")

st.sidebar.markdown("""
### Features
- Battery Health Prediction
- EV Range Estimation
- Risk Analysis
- Predictive Maintenance
""")
st.sidebar.title("🔋 EVision AI")

st.sidebar.markdown("---")

st.sidebar.markdown("""
### 🚀 Platform Features

✅ Battery Health Prediction

✅ EV Range Estimation

✅ Risk Assessment

✅ Degradation Analysis

✅ Predictive Maintenance

✅ Interactive Dashboard
""")

st.sidebar.markdown("---")

st.sidebar.info(
    "Designed & Developed by Supriya Verma"
)
st.markdown("""
<style>

.main {
    background-color: #F5F7FA;
}

div[data-testid="metric-container"] {
    background-color: white;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
}

.stButton > button {
    background-color: #0F4C81;
    color: white;
    border-radius: 12px;
    height: 3.2em;
    width: 100%;
    font-weight: bold;
    font-size: 16px;
}

.stButton > button:hover {
    background-color: #1565C0;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center;
color:#0F4C81;
font-size:50px;'>
🔋 EVision AI
</h1>

<h3 style='text-align:center;
color:#555555;'>
Smart Battery Intelligence for Electric Vehicles
</h3>
""", unsafe_allow_html=True)
st.success(
    "🚗 Predict battery health, estimate EV range, analyze degradation trends and enable predictive maintenance using Machine Learning."
)
st.markdown("""
<div style="
background: linear-gradient(90deg,#0F4C81,#1565C0);
padding:25px;
border-radius:15px;
text-align:center;
color:white;
margin-bottom:20px;
">

<h2>⚡ Next Generation EV Battery Analytics</h2>

Predict • Analyze • Optimize • Maintain

</div>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ---------------- #

data = load_dataset()

health_model = train_health_model()
range_model = train_range_model()


# ---------------- DASHBOARD ---------------- #

st.header("📊 EV Fleet Analytics Dashboard")

st.dataframe(data.head())
st.markdown("### 📈 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Battery Health",
        f"{data['Battery_Health_%'].mean():.2f}%"
    )

with col2:
    st.metric(
        "Average Range",
        f"{data['Range_km'].mean():.0f} km"
    )

with col3:
    st.metric(
        "Vehicles Analysed",
        len(data)
    )


# ---------------- BATTERY HEALTH PREDICTION ---------------- #

st.header("🔮 AI Battery Health Predictor")

battery_capacity = st.number_input(
    "Battery Capacity (kWh)",
    value=75.0
)

range_km_input = st.number_input(
    "Range (km)",
    value=400
)

charge_cycles = st.number_input(
    "Charge Cycles",
    value=1000
)

energy_consumption = st.number_input(
    "Energy Consumption (kWh/100km)",
    value=15.0
)

mileage = st.number_input(
    "Mileage (km)",
    value=50000
)

avg_speed = st.number_input(
    "Average Speed (km/h)",
    value=60.0
)

temperature = st.number_input(
    "Temperature (°C)",
    value=25.0
)

if st.button("Predict Battery Health"):

    prediction = health_model.predict([[
        battery_capacity,
        range_km_input,
        charge_cycles,
        energy_consumption,
        mileage,
        avg_speed,
        temperature
    ]])

    health = float(prediction[0])
    st.balloons()

    # ---------------- HEALTH STATUS ---------------- #
    if health >= 85:
        st.success(f"🟢 Battery Health: {health:.2f}% (Excellent)")
    elif health >= 70:
        st.warning(f"🟡 Battery Health: {health:.2f}% (Good)")
    else:
        st.error(f"🔴 Battery Health: {health:.2f}% (Needs Attention)")

    # ---------------- RISK ---------------- #
    st.subheader("🚨 Battery Risk Assessment")
    risk = get_risk_level(health)
    st.info(risk)

    # ---------------- RECOMMENDATIONS ---------------- #
    st.subheader("🔧 Recommendations")

    recommendations = get_ai_recommendations(
        health,
        charge_cycles,
        temperature
    )

    for rec in recommendations:
        st.write("•", rec)

    # ---------------- FUTURE HEALTH (FIXED) ---------------- #
    future_health = max(
        health - (charge_cycles * 0.001),
        20
    )

    st.subheader("📉 Future Battery Health Estimate")
    st.info(f"Estimated Future Health: {future_health:.2f}%")

    # ---------------- GAUGE ---------------- #
    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=health,
            title={"text": "Battery Health"},
            gauge={"axis": {"range": [0, 100]}}
        )
    )

    st.plotly_chart(gauge, use_container_width=True)

    # ---------------- TREND ---------------- #
    st.subheader("📈 Battery Degradation Trend")

    

    future_cycles = np.arange(
        charge_cycles,
        charge_cycles + 1000,
        100
    )

    future_health_values = []

    for cycle in future_cycles:
        future_health_values.append(
            max(health - ((cycle - charge_cycles) * 0.01), 20)
        )

    trend_df = pd.DataFrame({
        "Charge Cycles": future_cycles,
        "Battery Health": future_health_values
    })

    st.line_chart(trend_df.set_index("Charge Cycles"))
    st.markdown("---")
    st.subheader("📄 Final Report Download")
    st.download_button(
    label="⬇ Download EVision AI Report",
    data=open(generate_pdf_report(
        health,
        range_km_input,
        risk,
        recommendations
    ), "rb"),
    file_name="EVisionAI_Report.pdf",
    mime="application/pdf"
 )




    # ---------------- EV RANGE PREDICTION ---------------- #

st.header("🚗 EV Range Predictor")

range_battery_capacity = st.number_input(
    "Battery Capacity for Range (kWh)",
    value=75.0,
    key="range_cap"
)

range_battery_health = st.number_input(
    "Battery Health (%)",
    value=85.0,
    key="range_health"
)

range_charge_cycles = st.number_input(
    "Charge Cycles",
    value=1000,
    key="range_cycles"
)

range_energy_consumption = st.number_input(
    "Energy Consumption (kWh/100km)",
    value=15.0,
    key="range_energy"
)

range_temperature = st.number_input(
    "Temperature (°C)",
    value=25.0,
    key="range_temp"
)

if st.button("Predict EV Range"):

    predicted_range = range_model.predict([[
        range_battery_capacity,
        range_battery_health,
        range_charge_cycles,
        range_energy_consumption,
        range_temperature
    ]])

    st.success(
        f"🚗 Estimated EV Range: {predicted_range[0]:.0f} km"
    )

# ---------------- DATA ANALYSIS ---------------- #

st.header("📊 Battery Health Analysis")

fig1 = px.histogram(data, x="Battery_Health_%", nbins=20)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.scatter(data, x="Charge_Cycles", y="Battery_Health_%")
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.scatter(data, x="Temperature_C", y="Battery_Health_%")
st.plotly_chart(fig3, use_container_width=True)

 # ---------------- FINAL ---------------- #


st.success("✅ EVision AI Dashboard Loaded Successfully")