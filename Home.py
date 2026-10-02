import streamlit as st
import pandas as pd
import plotly.express as px

# Code for Streamlit app by Nicholas Flach, 2026, all rights reserved.


# Gray text
st.markdown("""
<style>
p {
    color: #B3B3B3;
}
</style>
""", unsafe_allow_html=True)

# font size increase

st.markdown("""
<style>
/* Increase normal text */
html, body, [class*="css"] {
    font-size: 21px;
}

/* Title */
h1 {
    font-size: 43px !important;
}

/* Subheaders */
h3 {
    font-size: 30px !important;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_icon="📊"
)
st.title("Meteodyn WT vs WindSim 11.0")
st.write("RMSE comparisons by weather station combination")
st.write("⬅️ Use the tabs on the left to navigate between comparisons of different numbers of stations.")