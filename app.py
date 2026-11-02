import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="EV Market Performance & Insights", page_icon="🔋", layout="wide")
st.title("🔋 Electric Vehicle Market Performance & Insights")
st.caption("Interactive demo dashboard • Uses clearly labelled illustrative sample data")

@st.cache_data
def load_data():
    p = Path(__file__).parent / "data" / "ev_market_sample.csv"
    return pd.read_csv(p)

df = load_data()
st.sidebar.header("Dashboard Filters")
years = sorted(df["Year"].unique())
selected_years = st.sidebar.slider("Year range", int(min(years)), int(max(years)), (int(min(years)), int(max(years))))
countries = st.sidebar.multiselect("Country", sorted(df["Country"].unique()), default=sorted(df["Country"].unique()))
makers = st.sidebar.multiselect("Manufacturer", sorted(df["Manufacturer"].unique()), default=sorted(df["Manufacturer"].unique()))
cats = st.sidebar.multiselect("Vehicle category", sorted(df["Vehicle_Category"].unique()), default=sorted(df["Vehicle_Category"].unique()))
bats = st.sidebar.multiselect("Battery technology", sorted(df["Battery_Technology"].unique()), default=sorted(df["Battery_Technology"].unique()))

f = df[
    df["Year"].between(*selected_years) &
    df["Country"].isin(countries) &
    df["Manufacturer"].isin(makers) &
    df["Vehicle_Category"].isin(cats) &
    df["Battery_Technology"].isin(bats)
]
if f.empty:
    st.warning("No records match these filters. Please widen your selections.")
    st.stop()

total_sales = int(f["Annual_Sales_Units"].sum())
avg_range = f["Driving_Range_KM"].mean()
avg_rating = f["Customer_Rating_5"].mean()
countries_count = f["Country"].nunique()
c1,c2,c3,c4 = st.columns(4)
c1.metric("Total EV sales", f"{total_sales:,}")
c2.metric("Average driving range", f"{avg_range:,.0f} km")
c3.metric("Average customer rating", f"{avg_rating:.2f}/5")
c4.metric("Markets covered", countries_count)

st.subheader("Market performance")
left,right = st.columns(2)
with left:
    trend = f.groupby("Year", as_index=False)["Annual_Sales_Units"].sum()
    st.plotly_chart(px.line(trend, x="Year", y="Annual_Sales_Units", markers=True,
                            title="Year-wise EV sales trend"), use_container_width=True)
with right:
    country_sales = f.groupby("Country", as_index=False)["Annual_Sales_Units"].sum().sort_values("Annual_Sales_Units", ascending=False)
    st.plotly_chart(px.bar(country_sales, x="Country", y="Annual_Sales_Units",
                           title="EV sales by country", color="Country"), use_container_width=True)

st.subheader("Manufacturer and vehicle insights")
left,right = st.columns(2)
with left:
    maker_sales = f.groupby("Manufacturer", as_index=False)["Annual_Sales_Units"].sum().sort_values("Annual_Sales_Units", ascending=False)
    st.plotly_chart(px.bar(maker_sales, x="Manufacturer", y="Annual_Sales_Units",
                           title="Manufacturer performance", color="Manufacturer"), use_container_width=True)
with right:
    category_sales = f.groupby("Vehicle_Category", as_index=False)["Annual_Sales_Units"].sum()
    st.plotly_chart(px.pie(category_sales, names="Vehicle_Category", values="Annual_Sales_Units",
                           title="Sales share by vehicle category"), use_container_width=True)

st.subheader("Battery technology")
battery = f.groupby("Battery_Technology", as_index=False).agg(
    Sales=("Annual_Sales_Units","sum"), Avg_Range_KM=("Driving_Range_KM","mean"),
    Avg_Price_USD=("Average_Price_USD","mean"))
left,right = st.columns(2)
with left:
    st.plotly_chart(px.bar(battery, x="Battery_Technology", y="Sales", title="Sales by battery technology"), use_container_width=True)
with right:
    st.plotly_chart(px.bar(battery, x="Battery_Technology", y="Avg_Range_KM", title="Average range by battery technology"), use_container_width=True)

st.subheader("Customer ratings and sustainability")
left,right = st.columns(2)
with left:
    ratings = f.groupby("Manufacturer", as_index=False)["Customer_Rating_5"].mean()
    st.plotly_chart(px.bar(ratings, x="Manufacturer", y="Customer_Rating_5", title="Average customer rating", range_y=[0,5]), use_container_width=True)
with right:
    yearly_co2 = f.groupby("Year", as_index=False)["CO2_Saved_Tonnes_Est"].sum()
    st.plotly_chart(px.area(yearly_co2, x="Year", y="CO2_Saved_Tonnes_Est", title="Estimated CO₂ saved trend"), use_container_width=True)

st.subheader("Filtered data")
st.dataframe(f, use_container_width=True, hide_index=True)
st.download_button("Download filtered data as CSV", f.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_ev_market_data.csv", mime="text/csv")

st.info("Academic/demo note: this package contains synthetic illustrative data, not verified real-world sales figures. Replace the CSV with an approved real dataset before making factual market claims.")
