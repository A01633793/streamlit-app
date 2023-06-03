import pandas as pd
import streamlit as st
import plotly.express as px

st.title("ITESM Class JP")
st.header("Airbnb Example Analytics")
st.write("### Subtitle")


# data will be in cache
@st.cache_data
def get_data():
    # URL = "http://data.insideairbnb.com/united-states/ny/new-york-city/2023-03-06/visualisations/listings.csv"
    # URL = "http://data.insideairbnb.com/canada/qc/montreal/2021-07-08/visualisations/listings.csv"
    URL = "http://data.insideairbnb.com/australia/nsw/sydney/2023-03-13/visualisations/listings.csv"
    return pd.read_csv(URL)


df = get_data()
st.dataframe(df.tail())


# step 1 sort
st.subheader("Sorting in tables")
st.text("The top five most expensive")
st.write(df.query("price>=0").sort_values("price", ascending=False).head())

# Step 2 - Map Visualization
st.header("Map")
st.subheader("Most Expensive properties")
st.map(df.query("price>=900")[["latitude", "longitude"]].dropna(how="any"))

# step 3 - column filter
st.subheader("Select a column to see")
default_cols = ["name", "host_id", "price"]
cols = st.multiselect("Columns", df.columns.tolist(), default=default_cols)
st.dataframe(df[cols].head(10))

# step 4 -  Static grouping
st.subheader("Avg minimum nights for a room type")
st.table(df.groupby("room_type").minimum_nights.mean().reset_index().sort_values("minimum_nights", ascending=False))

# step 5 - Distributions - Sidebars
st.write("Select a range for pricing within the sidebar")
values = st.sidebar.slider("Price Range", float(df.price.min()), float(df.price.clip(upper=1000.).max()), (10., 500.))
hist = px.histogram(df.query(f"price.between{values}"), x="price", nbins=100, title= "Price Distrution")
hist.update_xaxes(title="Price")
hist.update_yaxes(title="# of Apartments/Rooms/Hotels")
st.plotly_chart(hist)

# step 6 -   Radio buttons
neighbourhood = st.radio("Neighbourhood", df.neighbourhood_group.unique())

@st.cache_data
def get_availability(neighbourhood):
    return df.query("""neighbourhood_group==@neighbourhood\
        and availability_365>0""").availability_365.describe(\
            percentiles=[.1, .25, .5, .75, .9, .99]).to_frame().T

st.table(get_availability(neighbourhood))
