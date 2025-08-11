import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Real-Time Earthquake Tracker", layout="wide")

@st.cache_data(ttl=60) 
def get_earthquake_data():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    r = requests.get(url)
    data = r.json()

    features = data["features"]
    table = []
    for i in features:
        props = i["properties"]
        coords = i["geometry"]["coordinates"]
        table.append({
            "Place": props["place"],
            "Magnitude": props["mag"],
            "Time": datetime.utcfromtimestamp(props["time"]/1000),
            "Longitude": coords[0],
            "Latitude": coords[1],
            "Depth (km)": coords[2]
        })
    return pd.DataFrame(table)

# st.title("Earthquake Tracker")
st.markdown("<h1 style='text-align: center;'>Earthquake Tracker</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center;'>Seismic Activities in the past hour.</h3>",
    unsafe_allow_html=True
)

df = get_earthquake_data()


fig = px.scatter_geo(
    df,
    lat="Latitude",
    lon="Longitude",
    color="Magnitude",
    size="Magnitude",
    hover_name="Place",
    hover_data=["Magnitude", "Time", "Depth (km)"],
    projection="miller",
    color_continuous_scale="Reds"
)

fig.update_layout(width=5000, height=750)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Recent Earthquakes")
st.dataframe(df)

if st.button("Refresh"):
    st.cache_data.clear()
