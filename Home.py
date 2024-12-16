import streamlit as st

st.set_page_config(
    page_title="Movie Guesser",
    page_icon="assets/icon.png",
)

col1, col2, col3 = st.columns([1, 10, 1])
with col2:
    st.write("# 🎥 The Movie Guessing Game")

st.sidebar.success("Choose a Mode to play!")

col1, col2, col3 = st.columns([10, 1, 10])

with col1:
    st.image("https://images-cdn.ubuy.co.in/63503469d017ab73b23f23fb-sholay-bollywood-movie-poster-metal-tin.jpg")
with col3:
    st.image("https://images-cdn.ubuy.co.in/63400e7f3866b57e3c3204e4-once-upon-a-time-in-hollywood-poster-24.jpg")
