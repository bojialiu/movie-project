import streamlit as st
from network import movie_matcher


st.set_page_config(
    page_title="The Movie Project",
    page_icon = "🎬",
    layout = "wide"
)
# ======== title ========
st.title("️🎥 MADS Capstone - Project Movie Night")
st.subheader("⚡️ An Network+NLP based movie selector that makes no compromise!")

movie1 = st.empty()
movie2 = st.empty()
movie_input1 = movie1.text_input("Movie 1:",placeholder="movie name")
movie_input2 = movie2.text_input("Movie 2:",placeholder="movie name")

submit_button = st.button("Submit")
if submit_button:
    results = movie_matcher(movie_input1,movie_input2)
    st.write(results)
