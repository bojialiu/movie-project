import pandas as pd
import numpy as np
import re
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import random
from collections import Counter
import pickle

# read in saved datasets & model
user_movie_pivot = pd.read_csv('dataset/user_movie_pivot.zip', compression='zip', header=0, sep=',')
movie_list = user_movie_pivot.columns.tolist()
model_nn = pickle.load(open('dataset/cf_model.sav', 'rb'))
read_dict = pd.read_csv('dataset/movie_lookup_dict.csv').to_dict('list')
movie_lookup_dict = {}
for k, v in read_dict.items():
    movie_lookup_dict[k] = v[0]

# helper functions
# This functin returns movies names and ids. To use it, there should be a variable storing the id for the next recommending function.
def provide_movies_to_user(num):
    ran_id = random.sample(movie_list, num)
    ran_name = [movie_lookup_dict[ran] for ran in ran_id]
    return ran_name,ran_id

# Helper function 1 -- to exclude movies that users already seen from the recommendation list
def exclude_seen_movies(u_select):
    # get seen movie id from user feedback
    seen_id_list = [m for m,r in u_select]
    seen_name_list = [movie_lookup_dict[x] for x in seen_id_list]
    return seen_name_list

# Helper function 2 -- to get users with similar preferences for these 10 movies
def get_similar_users(u_select):
    # get movie id of user feedback
    p_id_list = [m for m,r in u_select if r>0]
    n_id_list = [m for m,r in u_select if r<0]

    # get index of movie for user feedback
    p_idx_list = [movie_list.index(x) for x in p_id_list]
    n_idx_list = [movie_list.index(x) for x in n_id_list]

    # create input array of same dimension for prediction
      # modify value of corresponding index to 10/-10
    user_fb_arr = np.zeros((1,1468))
    for idx1 in p_idx_list:
        user_fb_arr[0,idx1] = 10
    for idx2 in n_idx_list:
        user_fb_arr[0,idx2] = -10

    # find users who have similar preferences for these movies
    neigh_idx = model_nn.kneighbors(user_fb_arr, 3, return_distance=False)
    users_id = []
    for user_idx, val in enumerate(user_movie_pivot.index[neigh_idx][0]):
        users_id.append(val)
        #print((user_idx+1),". ",val)
    return users_id


# Helper function 3 -- To get movies liked by those similar users
def get_sim_user_like(sim_user_idx):
    user_row = user_movie_pivot.loc[[sim_user_idx]].values.flatten().tolist()
    user_like_movie_idx = []
    i = 0
    for y in user_row:
        if y == 10:
            user_like_movie_idx.append(i)
        i += 1
    if len(user_like_movie_idx) > 0:
        user_like_movie_id = [movie_list[m] for m in user_like_movie_idx]
        user_like_movie_name = [movie_lookup_dict[n] for n in user_like_movie_id]
        return user_like_movie_name
    else:
        print('no similar user found')

# Recommendation function
def recommend_to_user(provide,u_fb):
    # provide = output of func provide_movies_to_user()
    feedback_list = list(zip(provide[1],u_fb))
    sim_user_ids = get_similar_users(feedback_list)
    movie_exclude = exclude_seen_movies(feedback_list)

    recommend_list = []
    for each in sim_user_ids:
        each_like = get_sim_user_like(each)
        each_like_cl = [mov for mov in each_like if mov not in movie_exclude]
        recommend_list.extend(each_like_cl)

    counter = Counter(recommend_list)
    toplist = counter.most_common(5)
    recommend_movies = [tl for tl,ct in toplist]
    return recommend_movies
