import streamlit as st
import pandas as pd
import altair as alt
import csv
from network_model import movie_matcher
from collab_model import provide_movies_to_user, recommend_to_user
import ast
import streamlit.components.v1 as components

# ======== page config ========
st.set_page_config(
    page_title="The Movie Project",
    page_icon = "🎬",
    layout = "wide"
)

@st.cache
def load_movies_df():
    df = pd.read_csv('dataset/network_metadata.zip', compression='zip', header=0, sep=',')
    return(df)
metadata_df = load_movies_df()

# constants & settings
pd.set_option('display.max_colwidth', None)

# helper functions

def space(num_lines=1):
    for _ in range(num_lines):
        st.write("")

def page_switcher(page):
    st.session_state.runpage = page

def refresh_random_movies():
    f = open('dataset/temp.csv','w+') # empty the reandom file
    f.close()
    movies = provide_movies_to_user(8)
    df = pd.DataFrame(movies)
    df.to_csv('dataset/temp.csv',header=None,index=False)

def common():
    # ======== title ========
    st.title("️🎥 MADS Capstone - Project Movie Night")
    st.subheader("⚡️ Your new one-stop movie selector that makes no compromise!")
    # ======== side bar ========
    st.sidebar.write("")
    st.sidebar.image("assets/movie_logo.png",width=110)
    st.sidebar.write("")
    if st.sidebar.button("Model Selection",on_click=page_switcher,args=(main,)):
        st.experimental_rerun()
    st.sidebar.markdown("## **About this project**")
    intro = '''
        Can't decide what to wear,
        don't know what to eat for lunch, 
        struggling with what to watch on your next movie night...

        Life is full of annoying choices, so at least this time, let us help you out!!
        '''
    st.sidebar.markdown(intro)
    st.sidebar.markdown("## **Contributors**")
    st.sidebar.markdown("Chloe Zhang <br> Michael Conrad <br> Bojia Liu",unsafe_allow_html=True)
    st.sidebar.markdown("## **Source Code**")
    st.sidebar.markdown("[GitHub Link](https://github.com/bojialiu/movie-project)",unsafe_allow_html=True)


def main():
    common()
    space()
    st.markdown('## <center>👉 Model Selection 👈</center>',unsafe_allow_html=True)
    space()
    model1, model2 = st.columns(2)
    with model1:
        st.markdown("#### 👭 Movie night with a friend")
        st.markdown("Still struggling with what to watch on your next movie night? In this <b>Network+NLP</b> based model, you and your friend can each select a parent movie and generate a baby movie based on their metadata & plot!",unsafe_allow_html=True)
        btn1 = st.button('Use the NLP + Network Model',on_click=page_switcher,args=(network_model_page,))
        space(3)
        st.image('assets/watch_tv_img.png')
    with model2:
        st.markdown("#### 🙋‍♀️ Movie night with myself")
        st.markdown("Do you want people with similar tastes to recommend movies to you? In this model, we are using a <b>collaborative filtering</b> to help you pick your next movie to watch based on thousands of users on IMDb!",unsafe_allow_html=True)
        btn2 = st.button('Use the Collaborative Filtering Model',on_click=page_switcher,args=(collab_model_page,))
        st.image('assets/girl.png')
    if btn1 or btn2:
        st.experimental_rerun()

    if "page" not in st.session_state:
        st.session_state.page = 0
    if "counter" not in st.session_state:
        st.session_state.counter = 1

    components.html(
        f"""
            <!--{st.session_state.counter}-->
            <script>
                window.parent.document.querySelector('section.main').scrollTo(0, 0);
            </script>
        """,
        height=0
    )

    st.write(f"Page load: {st.session_state.counter}")

def network_model_page():
    # title & side bar
    common()
    col1, col_space, col2 = st.columns([7,1,10])

    with col1:
        space(2)
        st.image('assets/watch_tv_img.png')
    with col2:
        # ======== input movies========
        st.markdown("#### **_Please enter two parent movies_** ⬇️")
        random_button = st.button("Try something random!")
        st.write('Replace the following movies with your favorite ones!')
        movie1 = st.empty()
        movie2 = st.empty()

        if random_button:
            refresh_random_movies()

        try:
            random_df = pd.read_csv("dataset/temp.csv",header=None,index_col=False)
            input1 = random_df[0][0]
            input2 = random_df[1][0]
        except:
            input1 = ""
            input2 = ""
        movie_input1 = movie1.text_input("Movie 1:",input1,placeholder="movie name")
        movie_input2 = movie2.text_input("Movie 2:",input2,placeholder="movie name")


        space()
        submit_button = st.button("Submit")

    # ======== result showcase ========
    st.write("-----")

    result_area = st.empty()

    res_col, x, rate_col = st.columns([14,1,7])

    if submit_button:
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
                    # st.radio("😌 How do you like the result?",(1,2,3,4,5))
                    st.image("assets/girl.png")
        if movie_input1 == "" or movie_input2 == "":
            st.markdown("### *👀 Did you forgot to enter the movies?*",unsafe_allow_html=True)
        # else:
        #     st.markdown("### *😭 Sorry, we can't find the movies in our DB...*",unsafe_allow_html=True)

def collab_model_page():

    # title & side bar
    common()
    # constants
    options_dict = {
        '👎 Dislike':-10,
        '😐 ‍Neutral/Never Watched':0,
        '👍 Like':10
    }
    result_movie_names = ""
    results_title_text = ""
    st.markdown("### First, let's find out what kind of movies you like! ")
    cf_col1, cf_col2 = st.columns([2,1.8])
    with cf_col1:
        with st.form("my_form", clear_on_submit=False):
            # streamlit doesn't work well here because it refreshes every time
            #  retrive random values
            random_movies = pd.read_csv("dataset/temp.csv",header=None,index_col=False,).values.tolist()
            movie_lst = [item for sublist in random_movies for item in sublist][:8]
            st.write("Please rate the movies:")
            v1 = st.select_slider(str(movie_lst[0]),options=['👎 Dislike', '😐 ‍Neutral/Never Watched', '👍 Like'],value='😐 ‍Neutral/Never Watched')
            v2 = st.select_slider(str(movie_lst[1]),options=['👎 Dislike', '😐 ‍Neutral/Never Watched', '👍 Like'],value='😐 ‍Neutral/Never Watched')
            v3 = st.select_slider(str(movie_lst[2]),options=['👎 Dislike', '😐 ‍Neutral/Never Watched', '👍 Like'],value='😐 ‍Neutral/Never Watched')
            v4 = st.select_slider(str(movie_lst[3]),options=['👎 Dislike', '😐 ‍Neutral/Never Watched', '👍 Like'],value='😐 ‍Neutral/Never Watched')
            v5 = st.select_slider(str(movie_lst[4]),options=['👎 Dislike', '😐 ‍Neutral/Never Watched', '👍 Like'],value='😐 ‍Neutral/Never Watched')
            v6 = st.select_slider(str(movie_lst[5]),options=['👎 Dislike', '😐 ‍Neutral/Never Watched', '👍 Like'],value='😐 ‍Neutral/Never Watched')
            v7 = st.select_slider(str(movie_lst[6]),options=['👎 Dislike', '😐 ‍Neutral/Never Watched', '👍 Like'],value='😐 ‍Neutral/Never Watched')
            v8 = st.select_slider(str(movie_lst[7]),options=['👎 Dislike', '😐 ‍Neutral/Never Watched', '👍 Like'],value='😐 ‍Neutral/Never Watched')
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                output_lst = [options_dict[v1],options_dict[v2],options_dict[v3],options_dict[v4],options_dict[v5],options_dict[v6],options_dict[v7],options_dict[v8]]
                # st.write(output_lst)
                result_movie_names = recommend_to_user(random_movies,output_lst)
                # st.write(result_movie_name)
                results_title_text = "People with similar movie taste also like..."

    with cf_col2:
        st.image('assets/girl.png')
        st.markdown("#### <b>Haven't seen most of the movies on the list?</b>",unsafe_allow_html=True)
        st.write("👇  👇  👇")
        if st.button('Refresh movie options'):
            refresh_random_movies()

    st.write("-----")
    st.subheader(results_title_text)
    for result_movie_title in result_movie_names:
        # if title not in metadata_df, don't show in results
        try:
            result_movie_intro = metadata_df[metadata_df['title']==result_movie_title]['overview'].to_string(index=False)
            rating = metadata_df[metadata_df['title']==result_movie_title]['vote_average'].to_string(index=False)
            result_movie_rating = f"<b>IMDB: {rating}/10</b>"
            directors = ", ".join(ast.literal_eval(metadata_df[metadata_df['title']==result_movie_title]['director'].to_string(index=False)))
            result_movie_director = f"Directed by <b>{directors}</b>"
            imdb_id = metadata_df[metadata_df['title']==result_movie_title]['imdbId'].astype(int).to_string(index=False).rjust(7,'0')
            result_imdb_link = f"https://www.imdb.com/title/tt{imdb_id}/"
            cast = ", ".join(ast.literal_eval(metadata_df[metadata_df['title']==result_movie_title]['cast'].to_string(index=False))[:5])
            result_movie_cast = f"Cast: <b>{cast}</b>"
            st.subheader("🎬 " + result_movie_title)
            st.markdown(result_movie_rating,unsafe_allow_html=True)
            st.markdown(result_movie_director,unsafe_allow_html=True)
            st.markdown(result_movie_cast,unsafe_allow_html=True)
            st.markdown("#### Introduction")
            st.markdown(result_movie_intro,unsafe_allow_html=True)
            st.markdown(f'Go to IMDb Page: [{result_imdb_link}]({result_imdb_link})')
            st.write('-----')
        except:
            print("")

    # st.write(result_movie_name)

if __name__ == '__main__':
    if 'runpage' not in st.session_state :
        st.session_state.runpage = main
    st.session_state.runpage()
