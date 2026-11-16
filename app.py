import joblib
import numpy as np
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title='TerraVal - Natural Capital Engine',
    page_icon='🌿',
    layout='wide',
)

# Load Trained Models
@st.cache_resource
def load_models():
  val_model = joblib.load('asset_value_model.pkl')
  risk_model = joblib.load('depreciation_risk_model.pkl')
  return val_model, risk_model


val_model, risk_model = load_models()

# App Header
st.title('🌿 TerraVal: AI-Driven Natural Capital Valuation & Risk Engine')
st.markdown(
    'Transforming standing ecosystems into quantifiable financial assets'
    ' aligned with **TNFD (Taskforce on Nature-related Financial'
    ' Disclosures)** standards.'
)
st.markdown('---')

# Sidebar for User Inputs (Interactive Sliders)
st.sidebar.header('🛰️ Ecological Telemetry Inputs')

ndvi = st.sidebar.slider(
    'NDVI (Plant Health Index)',
    0.20,
    0.95,
    0.65,
    help='0.2 = Barren/Degraded land | 0.95 = Dense rainforest',
)
tree_cover = st.sidebar.slider(
    'Tree Cover Density (%)',
    10.0,
    95.0,
    60.0,
    help='Percentage of land covered by forest canopy',
)
water_stress = st.sidebar.slider(
    'Water Stress Index',
    0.0,
    0.80,
    0.25,
    help='0.0 = Abundant water | 0.8 = Severe drought',
)
bii = st.sidebar.slider(
    'Biodiversity Intactness Index (BII)',
    0.30,
    0.99,
    0.70,
    help='Species health model score',
)
proximity = st.sidebar.slider(
    'Proximity to Threat (km)',
    0.5,
    40.0,
    15.0,
    help='Distance from active industrial zones or deforestation fronts',
)

# Currency Selector (as recommended in testing feedback)
currency = st.sidebar.selectbox('Currency Selection', ['USD ($/ha)', 'INR (₹/ha)'])
currency_multiplier = 83.0 if currency == 'INR (₹/ha)' else 1.0
curr_symbol = '₹' if currency == 'INR (₹/ha)' else '$'

# Prepare input array for prediction
input_data = pd.DataFrame([[ndvi, tree_cover, water_stress, bii, proximity]], columns=['ndvi', 'tree_cover_density', 'water_stress_index', 'bii', 'proximity_to_threat'])

# Make Predictions
pred_value = val_model.predict(input_data)[0] * currency_multiplier
pred_risk = risk_model.predict(input_data)[0]

# Determine Risk Status Badge
if pred_risk < 20:
  risk_badge = '🟢 LOW RISK (Healthy Conservation Asset)'
  badge_color = 'green'
elif pred_risk <= 50:
  risk_badge = '🟡 MODERATE RISK (Requires Ecological Attention)'
  badge_color = 'orange'
else:
  risk_badge = '🔴 HIGH RISK (Severe Threat / Urgent Action Needed)'
  badge_color = 'red'

# Display Main Dashboard Results
col1, col2 = st.columns(2)

with col1:
  st.metric(
      label='Estimated Asset Value per Hectare',
      value=f'{curr_symbol}{pred_value:,.2f}/ha',
  )

with col2:
  st.metric(
      label='5-Year Depreciation Risk Rate', value=f'{pred_risk:.2f}%'
  )

st.markdown('### Risk Status Classification')
st.markdown(f'#### :{badge_color}[{risk_badge}]')
st.markdown('---')

# Feature Importance (Explainable AI)
st.markdown('### 📊 Feature Importance Breakdown (Explainable AI)')
st.markdown(
    'Understanding which ecological drivers had the greatest impact on this'
    ' valuation:'
)

feature_importance = pd.DataFrame({
    'Ecological Factor': [
        'NDVI (Plant Health)',
        'Tree Cover Density',
        'Water Stress Index',
        'Biodiversity (BII)',
        'Proximity to Threat',
    ],
    'Importance Score': val_model.feature_importances_,
}).sort_values(by='Importance Score', ascending=True)

st.bar_chart(feature_importance.set_index('Ecological Factor'))

# Export Audit Summary Button
st.markdown('---')
if st.button('📄 Generate Printable Risk Audit Report'):
  st.success(
      'Audit report successfully generated! You can now present this summary'
      ' to your ESG committee.'
  )
  st.json({
      'Project': 'TerraVal Engine',
      'NDVI': ndvi,
      'Tree Cover Density (%)': tree_cover,
      'Water Stress Index': water_stress,
      'Biodiversity Intactness (BII)': bii,
      'Proximity to Threat (km)': proximity,
      'Calculated Asset Value': f'{curr_symbol}{pred_value:,.2f}/ha',
      '5-Year Depreciation Risk (%)': f'{pred_risk:.2f}%',
      'Risk Status': risk_badge,
  })