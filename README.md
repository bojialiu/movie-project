# MADS Capstone - Project Movie Night

Can't decide what to wear, don't know what to eat for lunch, struggling with what to watch on your next movie night...
Life is full of annoying choices, so at least this time, let us help you out!

This project holds two different machine learning models to help you select the next movie for your movie night, whether you are by yourself or with friends, this web app could be your one-stop solution.
- With our **Network+NLP** based model, you and your friend can each select a parent movie and generate a baby movie right in the middle based on their metadata & plot.
- With our user-based model, we are using **Collaborative Filtering** to help you pick your next movie to watch based on thousands of users on IMDb.

**Web app address:**: https://share.streamlit.io/eolhcz/movie-project/main/app.py 

<img src="/assets/screenshot.png" alt="drawing" width="600"/>

## Dataset

- Metadata on 45,000 movies as ratings and reviews: https://www.kaggle.com/rounakbanik/the-movies-dataset
- Movie summaries scraped from wikipedia: http://www.cs.cmu.edu/~ark/personas/
- Additional metadata we can cross reference: https://www.imdb.com/interfaces/
- Movie ratings: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?select=ratings_small.csv

## Models in Jupyter
- Capstone.ipynb -- network-based system that recommend the most similar movie based on two movies user inputs
- user-based recommender.ipynb -- user-based collavrative filtering system that recommend movie based on user behaviour 


## How To Use
- online: https://share.streamlit.io/eolhcz/movie-project/main/app.py 
- local:
```bash
# install requirements
$ pip install -r requirements.txt
streamlit run app.py
```

## License
This project is distributed under MIT Licence.

## Team Members
- Chloe Zhang ([GitHub](https://github.com/eolhcz))
- Michael Conrad
- Bojia Liu
- Michael Conrad ([GitHub](https://github.com/conradma))
- Bojia Liu ([GitHub](https://github.com/bojialiu))
