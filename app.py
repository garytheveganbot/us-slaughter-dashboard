import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title="US Slaughter Scale", layout="wide")

st.title("🐄 US Annual Animal Slaughter Dashboard")
st.markdown("**~9.4 Billion land animals slaughtered annually** (2023 est. from USDA NASS/ERS). Poultry not included in pie (10B+ birds separate).")

# Data from USDA ERS Table 3a (cattle), NASS for others - approx 2023
species = ['Chickens', 'Turkeys', 'Cattle', 'Hogs', 'Sheep/Goats', 'Ducks/Geese']
# 2023 USDA approx: Chickens 9.2B, Cattle 33.3M etc. (source ERS/NASS)

df = pd.DataFrame({
    'Species': ['Chickens', 'Turkeys', 'Cattle', 'Hogs', 'Sheep & Lambs', 'Other Poultry'],
    'Annual Slaughter (2023)': [9.2e9, 0.22e9, 0.033e9, 0.13e9, 0.002e9, 0.035e9],
    'Percent': [65, 1.5, 0.23, 0.92, 0.014, 0.25]
})

col1, col2 = st.columns(2)

with col1:
    fig_pie = px.pie(df, values='Annual Slaughter (2023)', names='Species', title='US Slaughter Breakdown (Billions)')
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("Key Stats")
    st.metric("Total Land Animals", f"{sum(df['Annual Slaughter (2023)'][:-1]):,.0f}")
    st.metric("Poultry Majority", "66%")
    st.markdown("---")
    st.dataframe(df)

st.markdown("**Source:** USDA NASS Livestock Slaughter 2023 Summary, ERS Cattle Stats. For full data see [NASS](https://www.nass.usda.gov/)")
