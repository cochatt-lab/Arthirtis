
import streamlit as st
import pandas as pd
import plotly.express as px

# Google Sheets CSV export URL
sheet_url = "https://docs.google.com/spreadsheets/d/1f0yIgSceCetFiiC08Rg3uUpdMonEGImB5NoWC0ngNhg/export?format=csv"

# Load data from Google Sheets
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data():
    df = pd.read_csv(sheet_url)
    return df

# Load and process data
df = load_data()
df_melted = df.melt(id_vars="Year", var_name="Marital Status", value_name="Estimate")

# Streamlit UI
st.title("📊 Arthritis Estimates Dashboard")
st.markdown("Data Source: [Google Sheets](https://docs.google.com/spreadsheets/d/1f0yIgSceCetFiiC08Rg3uUpdMonEGImB5NoWC0ngNhg/edit?usp=sharing)")

# Filter options
statuses = st.multiselect(
    "Select Marital Status Groups:",
    options=df_melted["Marital Status"].unique(),
    default=df_melted["Marital Status"].unique()
)

filtered_df = df_melted[df_melted["Marital Status"].isin(statuses)]

# Plot
fig = px.line(
    filtered_df,
    x="Year",
    y="Estimate",
    color="Marital Status",
    title="Arthritis Estimates by Marital Status (2019–2024)",
    markers=True
)
st.plotly_chart(fig)

# Show data table
st.markdown("### 📋 Data Table")
st.dataframe(filtered_df)
