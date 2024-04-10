import pandas as pd
import altair as alt
import streamlit as st
from ultil.connection import init_connection

clientmb = init_connection()

def get_data():
    db = clientmb.sentiment
    items = db.insurance.find()
    items = list(items)  # make hashable for st.cache_data
    return items
items = get_data()

sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
for item in items:
    try:
        sentiment = item.get("sentiment", "").lower()
        if sentiment in sentiment_counts:
           sentiment_counts[sentiment] += 1
    except:
       pass

df = pd.DataFrame(sentiment_counts.items(), columns=['category', 'value'])
donut_chart = alt.Chart(df).mark_arc().encode(
    theta="value",
    color="category"
)

st.altair_chart(donut_chart, use_container_width=True)

total_negative=sentiment_counts['negative']
total_positive=sentiment_counts["positive"]
total_neutral=sentiment_counts['neutral']

st.markdown(f"<h3><strong>Total of negative: {total_negative}</strong></h3>", unsafe_allow_html=True)
st.markdown(f"<h3><strong>Total of positive: {total_positive}</strong></h3>", unsafe_allow_html=True)
st.markdown(f"<h3><strong>Total of neutral: {total_neutral}</strong></h3>", unsafe_allow_html=True)
