import pandas as pd
import ast
import numpy as np
import random
import re
from collections import Counter
import networkx as nx
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import ast
import csv
import pickle

# read files
metadata_df = pd.read_csv('dataset/network_metadata.zip', compression='zip', header=0, sep=',')
G = pickle.load(open('dataset/graph.txt','rb'))

#get cosine similarity matrix of vectorized summaries
tfidf_summary = TfidfVectorizer(stop_words='english',max_df=0.3,max_features=3000).fit_transform(metadata_df['Summary'])
cosine_similarity = linear_kernel(tfidf_summary, tfidf_summary)

#gets the shortest paths from above network given two movie title inputs to create cast_score

def cast_paths(movie1, movie2):
    #shortest_path = nx.shortest_path_length(G, source=movie1, target=movie2)
    cast_score = dict.fromkeys(metadata_df['title'], 0)
    for path in nx.all_simple_paths(G, source=movie1, target=movie2, cutoff = 2):#shortest_path):
        cast_score[path[0]] += 2
    for path in nx.all_simple_paths(G, source=movie1, target=movie2, cutoff = 3):
        for movie in path:
            if cast_score[movie] == 0:
                cast_score[movie] += 1

    cast_score[movie1] = 0
    cast_score[movie2] = 0

    return cast_score

#get all cosine similarities for one movie. helper func for cos_sim_match
def get_cos_sim(title, cos_sim = cosine_similarity):
    index = metadata_df.index[metadata_df['title'] == title]
    cs = cosine_similarity[index][0]
    cs[index] = 0 #set cosine sim with self to zero so we don't recommend same movie as input
    return cs

#given values and assuming keys are movie title, create dictionary. helper func for cos_sim_match
def list_to_dict(values):
    keys = metadata_df['title']
    dictionary = dict(zip(keys, values))
    #dictionary = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
    return dictionary

#get cosine_sim for both movie inputs and add together for cosine_sim score
def cos_sim_match(movie1, movie2):
    cs_movie1 = get_cos_sim(title = movie1)
    cs_movie2 = get_cos_sim(title = movie2)
    summary_score = list_to_dict(cs_movie1*np.max(cs_movie2) + cs_movie2*np.max(cs_movie1))
    return dict(summary_score)

# read genre dict
read_dict = pd.read_csv('dataset/genres.csv').to_dict('list')
genres_dict = {}
for k, v in read_dict.items():
    genres_dict[k] = [ast.literal_eval(x) for x in v]
genres_dict['Drama']

#create genre score

#randomly pick genre from available options if movie has more than one genre,
#and take the genre most commonly associated with that chosen genre (do for both movies)
#and check to see if those two new genres match each other or any of the original genres
#helper func for match_genres
def randomized_genre_pick(genre1, genre2):
    genre1_pick = genres_dict[random.choice(genre1[0])][1][0]
    genre2_pick = genres_dict[random.choice(genre2[0])][1][0]
    return set([genre1_pick, genre2_pick, genre1, genre2])


def match_genres(movie1, movie2):
    genre1 = list(metadata_df.loc[metadata_df['title'] == movie1, 'genres'])
    genre2 = list(metadata_df.loc[metadata_df['title'] == movie2, 'genres'])
    intersect = set(genre1[0]) & set(genre2[0])

    #if the two movie inputs don't have a genre in common,
    #we'll use randomized_genre_pick to try to find a similar genre in common
    emergency_count = 0
    while len(intersect) == 0:
        intersect = randomized_genre_pick(genre1, genre2)
        emergency_count += 1

        #the most common genre is drama. If it can't find a matching one
        #after x iterations, we'll just pick drama as the matching one
        if emergency_count > 20:
            intersect = set(['Drama'])
            break

    genre_score = dict.fromkeys(metadata_df['title'], 1)
    for i in metadata_df.index:
        if intersect.issubset(metadata_df['genres'].iloc[i]):
            genre_score[metadata_df['title'].iloc[i]] = 2

    #to help avoid picking input movies for output
    genre_score[movie1] = 0
    genre_score[movie2] = 0

    return genre_score

#match_genres('Jumanji', 'Grumpier Old Men')

#create score for ranking varaiables like vote and popularity
#find range between two input movies and give higher score to new movies in that range
def range_score(movie1, movie2, prop):
    movie1 = float(metadata_df[metadata_df['title'] == movie1][prop])
    movie2 = float(metadata_df[metadata_df['title'] == movie2][prop])

    max_score = max(movie1, movie2)
    min_score = min(movie1, movie2)

    score = dict.fromkeys(metadata_df['title'], 1)
    for index in metadata_df.index:
        this_move_score = float(metadata_df[prop].iloc[index])
        if this_move_score > min_score and this_move_score < max_score:
            score[metadata_df['title'].iloc[index]] = 2

    score[movie1] = 0
    score[movie2] = 0

    return score

#use levenshtein distance to match mispelled inputs with a movie title in metadata_df

import Levenshtein as lev
def fuzzy_match(movie):
    ratio_list = []
    for i in metadata_df['title']:
        #if statement to remove release years added to titles where name refers to more than one movie
        if i[-1] == ')' and i[-6] == '(':
            ratio_list.append(lev.ratio(movie.lower(), i[0:-6].lower()))
        else:
            ratio_list.append(lev.ratio(movie.lower(), i.lower()))
    return movie, metadata_df['title'].iloc[np.argmax(ratio_list)] #return closest match


#combine scores defined above with weights to calculate score for each movie to recommend

def movie_matcher(movie1, movie2):

    #match user query to movie title in metadata_df
    user_query_1, movie1 = fuzzy_match(movie1)
    user_query_2, movie2 = fuzzy_match(movie2)

    #get each score for movie combo
    summary_score = cos_sim_match(movie1, movie2)
    cast_score = cast_paths(movie1, movie2)
    genre_score = match_genres(movie1, movie2)
    vote_score = range_score(movie1, movie2, 'vote_average')
    popularity_score = range_score(movie1, movie2, 'popularity')

    #weights for each score
    w1 = 3
    w2 = 1
    w3 = 3
    w4 = 1
    w5 = 1

    #update scores with weights
    summary_score.update((x,y*w1) for x,y in summary_score.items())
    cast_score.update((x,y*w2) for x,y in cast_score.items())
    genre_score.update((x,y*w3) for x,y in genre_score.items())
    vote_score.update((x,y*w4) for x,y in vote_score.items())
    popularity_score.update((x,y*w5) for x,y in popularity_score.items())

    final_score = Counter(summary_score) + Counter(cast_score) + Counter(genre_score) \
                    + Counter(vote_score) + Counter(popularity_score)
    final_score = sorted(final_score.items(), key=lambda item: item[1], reverse=True)

    print('User Query 1: '+user_query_1+'    Matched to: '+movie1)
    print('User Query 2: '+user_query_2+'    Matched to: '+movie2)

    return final_score[0:10]#summary_score, cast_score, genre_score
