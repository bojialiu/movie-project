# MADS Capstone - Project Movie Night

This is the backend implementation of movie recommender system with two machine learning models based on NLP+Network and Collaborative Filtering.

**Web app address:**: https://share.streamlit.io/eolhcz/movie-project/main/app.py 

## Dataset

- movie metadata: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?select=movies_metadata.csv
- rating: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?select=ratings_small.csv
- movie summaries scraped from wikipedia: http://www.cs.cmu.edu/~ark/personas/
- additional metadata we can cross reference: https://www.imdb.com/interfaces/

## Models in Jupyter
- Capstone.ipynb -- network-based system that recommend the most similar movie based on two movies user inputs
- user-based recommender.ipynb -- user-based collavrative filtering system that recommend movie based on user behaviour 


## How To Use
- online: https://share.streamlit.io/eolhcz/movie-project/main/app.py 
- local:
```bash
# install requirements
# $ pip install -r requirements.txt
streamlit run app.py
```

## Team Members
- Chloe Zhang ([GitHub](https://github.com/eolhcz))
- Michael Conrad ([GitHub](https://github.com/conradma))
- Bojia Liu ([GitHub](https://github.com/bojialiu))
