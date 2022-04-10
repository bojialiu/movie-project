import streamlit as st
import pandas as pd
import altair as alt
import csv
from random import randint, seed
from network_model import movie_matcher, metadata_df
import ast
# helper functions

def space(num_lines=1):
    for _ in range(num_lines):
        st.write("")

# constants & settings
seed = 42
pd.set_option('display.max_colwidth', None)

def main():
    # ======== page config ========
    st.set_page_config(
        page_title="The Movie Project",
        page_icon = "🎬",
        layout = "wide"
    )
    # ======== title ========
    st.title("️🎥 MADS Capstone - Project Movie Night")
    st.subheader("⚡️ An Network+NLP based movie selector that makes no compromise!")
    # ======== side bar ========
    st.sidebar.write("")
    st.sidebar.image("assets/movie_logo.png",width=110)
    st.sidebar.markdown("## **About this project**")
    st.sidebar.markdown("Placeholder for **a _good_ introduction**\nPlaceholder for **a _good_ introduction**\nPlaceholder for **a _good_ introduction**")
    st.sidebar.markdown("## **Contributors**")
    st.sidebar.markdown("Chloe Zhang <br> Michael Conrad <br> Bojia Liu",unsafe_allow_html=True)
    st.sidebar.markdown("## **Source Code**")
    st.sidebar.markdown("[GitHub Link](https://github.com/bojialiu/movie-project)",unsafe_allow_html=True)

    col1, col_space, col2 = st.columns([7,1,10])

    with col1:
        space()
        st.image('assets/watch_tv_img.png')

    with col2:

        # space(2)
        # ======== input movies========
        st.markdown("#### **_Please enter two parent movies_**")
        random_button = st.button("Try something random!")
        movie1 = st.empty()
        movie2 = st.empty()


        if random_button:
            f = open('temp.csv','w+') # empty the reandom file
            f.close()
            m1 = randint(0,100) #random movie1
            m2 = randint(0,100) #random movie2
            df = pd.DataFrame([m1,m2])
            df.to_csv('temp.csv',header=None,index=False)

        try:
            random_df = pd.read_csv("temp.csv",header=None,index_col=False)
            input1 = random_df.iloc[0].to_string().split()[1]
            input2 = random_df.iloc[1].to_string().split()[1]
        except:
            input1 = ""
            input2 = ""
        movie_input1 = movie1.text_input("Movie 1:",input1,placeholder="movie name")
        movie_input2 = movie2.text_input("Movie 2:",input2,placeholder="movie name")


        space()
        submit_button = st.button("Submit")

    # ======== result showcase ========
    "________"


    # result_movie_title = "WALLE-E"
    # result_movie_intro = "In a distant, but not so unrealistic, future where mankind has abandoned earth because it has become covered with trash from products sold by the powerful multi-national Buy N Large corporation, WALL-E, a garbage collecting robot has been left to clean up the mess. Mesmerized with trinkets of Earth's history and show tunes, WALL-E is alone on Earth except for a sprightly pet cockroach. One day, EVE, a sleek (and dangerous) reconnaissance robot, is sent to Earth to find proof that life is once again sustainable. WALL-E falls in love with EVE. WALL-E rescues EVE from a dust storm and shows her a living plant he found amongst the rubble. Consistent with her 'directive', EVE takes the plant and automatically enters a deactivated state except for a blinking green beacon. WALL-E, doesn't understand what has happened to his new friend, but, true to his love, he protects her from wind, rain, and lightning, even as she is unresponsive. One day a massive ship comes to reclaim EVE, but WALL-E, out of love or loneliness, hitches a ride on the outside of the ship to rescue EVE. The ship arrives back at a large space cruise ship, which is carrying all of the humans who evacuated Earth 700 years earlier. The people of Earth ride around this space resort on hovering chairs which give them a constant feed of TV and video chatting. They drink all of their meals through a straw out of laziness and/or bone loss, and are all so fat that they can barely move. When the auto-pilot computer, acting on hastily-given instructions sent many centuries before, tries to prevent the people of Earth from returning by stealing the plant, WALL-E, EVE, the portly captain, and a band of broken robots stage a mutiny."
    # result_movie_rating = "<b>IMDB: 8.4/10</b>"
    # result_movie_director = "Directed by <b>Andrew Stanton</b>"

    result_area = st.empty()

    res_col, x, rate_col = st.columns([14,1,7])

    if submit_button:
        f = open('temp.csv','w+')
        if movie_input1 != "" and movie_input2 != "":
            with st.spinner("Generating a baby movie for " + movie_input1 + " + " + movie_input2):
                result_area.write(movie_input1 + " + " + movie_input2 + " = ...")
                # results here
                result_movie_title = movie_matcher(movie_input1,movie_input2)[0][0]
                result_movie_intro = metadata_df[metadata_df['title']==result_movie_title]['overview'].to_string(index=False)
                result_movie_rating = f"<b>IMDB: {metadata_df[metadata_df['title']==result_movie_title]['vote_average'].to_string(index=False)}/10</b>"
                directors = ", ".join(ast.literal_eval(metadata_df[metadata_df['title']==result_movie_title]['director'].to_string(index=False)))
                result_movie_director = f"Directed by <b>{directors}</b>"
                imdb_id = metadata_df[metadata_df['title']==result_movie_title]['imdbId'].astype(int).to_string(index=False).rjust(7,'0')
                result_imdb_link = f"https://www.imdb.com/title/tt{imdb_id}/"
                cast = ", ".join(ast.literal_eval(metadata_df[metadata_df['title']==result_movie_title]['cast'].to_string(index=False))[:5])
                result_movie_cast = f"Cast: <b>{cast}</b>"
                with res_col:
                    st.subheader("🎬 " + result_movie_title)
                    st.markdown(result_movie_rating,unsafe_allow_html=True)
                    st.markdown(result_movie_director,unsafe_allow_html=True)
                    st.markdown(result_movie_cast,unsafe_allow_html=True)
                    st.markdown("#### Introduction")
                    st.markdown(result_movie_intro,unsafe_allow_html=True)
                    st.markdown(f'Go to IMDb Page: [{result_imdb_link}]({result_imdb_link})')
                with rate_col:
                    space(3)
                    st.radio("😌 How do you like the result?",(1,2,3,4,5))
        if movie_input1 == "" or movie_input2 == "":
            st.markdown("### *👀 Did you forgot to enter the movies?*",unsafe_allow_html=True)
        # else:
        #     st.markdown("### *😭 Sorry, we can't find the movies in our DB...*",unsafe_allow_html=True)
    # res = result_area.text_area("Resulting Baby Movie:")

    # ======== side bar ========


if __name__ == '__main__':
    main()
