# MADS Capstone - Project Movie Night

This is the backend implementation of movie recommender system with two machine learning models based on NLP+Network and Collaborative Filtering.

**Web app address:**: https://share.streamlit.io/eolhcz/movie-project/main/app.py 

## Dataset

- movie metadata: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?select=movies_metadata.csv
- rating: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?select=ratings_small.csv

## Models in Jupyter
network_model.py -- network-based system that recommend the most similar movie based on two movies user inputs
collab_model.py -- user-based collavrative filtering system that recommend movie based on user behaviour 


## How To Use
```bash
# Installing requirements
streamlit run app.py
```

## Team Members
- Chloe Zhang ([GitHub](https://github.com/eolhcz))
- Michael Conrad
- Bojia Liu
