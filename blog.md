# MADS Capstone - Project Movie Night

## Introduction

We started out with a simple problem. Picture two people, showing up to movie night with two totally different movies, and neither of them want to compromise. Our goal was to create a compromise for them, by looking at the features that make their favorite movies their favorite and selecting a new movie that will make them both happy. Of course, we didn’t want to leave out those among us who enjoy a good movie alone, so we also wanted to create a similar solution for anyone who just can’t think of a movie to watch.

To start out, we tried to find some comprehensive datasets that would contain a lot of popular movies, but also some not so popular movies. We landed with three datasets that covered a wide spectrum of films but also provided us with many of the features we wanted to work with. The first was from IMDb and contained a lot of the metadata that’s typically found on the website. The second was from Kaggle and contained ratings and reviews and the final database was of summaries scraped from Wikipedia. With some routine data cleaning, we grabbed the features we wanted from each dataset and put it all together in a single dataframe.

## Model #1 The Movie Combination Model

For combining two movies, we wanted to devise our own custom formula that would be the summation of weighted scores, one score per feature. So for every feature, every movie in our database would be assigned a score that would reflect how close that particular movie matched the two input movies in regards to that particular feature. It’ll make more sense as we look at each feature and scoring system in turn.
 
### The first feature we looked as was cast members.
To begin, we created a network graph where movie titles were nodes and the edges connecting them were cast members. If two movies shared the same actor, they would be connected in the network. To generate the score, we took the two input movies and looked for all the paths between them that included just one other node. Restated, we found the intersection of all movies that had a cast member in common with the first input movie and a cast member in common with the second input movie. These movies were assigned a score of 2. Next we looked for all the paths between the input movies that included exactly two nodes. These movies were assigned a score of 1. All other movies were assigned a score of 0. Let’s look at a quick illustration. If our two input movies are Forest Gump and The Santa Clause, we would assign Toy Story a score of 2 since Tom Hanks is in both Forrest Gump and Toy Story and Tim Allen is in both The Santa Clause and Toy Story. As shown in figure one, many movie combinations will return movies with a score of 2 or 1, but there are some potential input movies on the edges of the network that will result in all movies being scored with 0, so let’s look at some other features that we scored.

<img src="/assets/network.png" alt="drawing" width="700"/>
(Visualization of 1000 randomly sampled nodes from the cast graph, visualized using Gephi)

### The next feature we looked at was movie summaries.
We took some basic NLP steps and vectorized the text of the summaries with a tfidf vectorizer. From these vectorized summaries, we were able to find a cosine similarity between every movie. The plan from there was to use this cosine similarity matrix to identify movies that were most similar to both input movies, but the matrix proved too large to efficiently store in memory. As a work around,  the cosine similarity matrix was used to train a Kmeans classifier and group the movies into 10 clusters. Then each movie’s cluster membership was saved in a vector, solving the memory problem of the cosine similarity matrix. To produce a score, all the movies that matched an input movie’s cluster was given a 1 and all other movies given a 0.
 
### The next score we’re going to create is genre.
Initially, we started with the simple approach of assigning a score of 1 to the intersecting genres of the two input movies and assigning all other genres a score of 0. However, it quickly became apparent that many movie combinations had no intersecting genres and so all genres would be assigned a score of 0. A quick solution to this would be to assign all of the input movie genres a score of 1, but that might fail to capture the combination of movies that we were looking for. So instead we counted how many times each genre was associated with every other genre. So now if the input movies had no intersecting genres, we could find the most closely associated genres and see if those intersected, expanding the pool of genres our scoring system looked at.

### The final two features we used were a popularity score and a voter rating score.
We used the respective scores of the two input movies to create a bounded range. Any movie with a score inside the range was assigned a 1 and any movie outside of it was assigned a 0. The purpose of this was to ensure that two blockbuster input movies would be less likely to produce a B movie and vice versa. If a popular movie and an unpopular movie are selected as inputs, the algorithm is able to assign a score of 1 to a wide range of films.

### Now to combine the scores.
Now that we had generated scores for individual features, we needed to find a way to combine them in order to produce a meaningful, and accurate, output movie. To achieve this, we added a weight to adjust each score and then summed each weighted score for each movie and output the movie with the highest score. Initially we’ve chosen scores that we think anecdotally make sense. Since we used a custom scoring method, it was difficult to come up with a method to validate the performance of our model. Ultimately, we decided that the best way to validate it would be to gather user feedback over time and incorporate it into future iterations of the model.

## Model #2 The Collaborative Model

### There is another scenario for our web app.
Imagine a night when you are hanging out alone and in the mood for a movie but you don’t have anything in mind: this is where our collaborative model comes to the rescue.

This model adopts the collaborative filtering system, which takes in user’s preferences on movies as input and finds other users in the database with similar taste and recommend something that these similar users like. The classic collaborative filtering system requires a large amount of feedback from users directly to improve the model with each iteration upon users’ feedback. However, due to the strict limitation on host memory on our web app, built with Streamlit’s free version, this would prove a major obstacle to that kind of model. Therefore, we take in a small amount of information from the user and use user-based filtering to identify those with similar behavior in our existing dataset.

### Preparing the data
To achieve this, we use the ratings from the IMDb data of over 9000 movies as well as metadata to match these ratings to movie titles. After a typical data cleaning process, which involves removing duplicate IDs, dropping nan values, and matching movie IDs with names, we are left with about 2800 movies. The next step is to find a proxy of user liking. We could use ratings, ranging from 1 to 5, as is native to the dataset, but to put ourselves into web users’ shoe: would I rather give ratings on a scale of 5 or simply click like/dislike? We define any rating larger than 3 as like and below or equal to 3 as dislike, then create a sparse matrix with user ids and movie ids. Each row represents one user, and each column represents one movie, the value is their preferences towards each movie: 10 for like, -10 for dislike, and 0 for no reviews.

### Training the model
The machine learning model we use on this data is Nearest Neighbours and train this model on the user-movie matrix. Feeding this model with user’s feedback yields this user’s nearest neighbours, which are considered as people with similar movie taste. What kind of data we collect from the user? As mentioned before, it would be more user-friendly if the web app provides users with movie titles, rather than allowing the user to choose their own. Hence, our app shows a user 8 random movies from the database and stores the user’s feedback (as in like/dislike/never watched) as a single-row array with the same length as the user-movie matrix. We then feed this array into the KNN model. Upon getting the nearest neighbours, our model will collect movies that are favoured by these neighbours and recommend the ones that are most like the user’s input preferences.

<img src="/assets/Picture1.png" alt="drawing" width="300"/> (Example of movies shown to user)

<img src="/assets/Picture2.png" alt="drawing" width="300"/> (Example of movie recommendation upon user feedback)

## Optimization and future work
Above is the current deployed version. We also optimized the collaborative filtering model by conducting more detailed data pruning, training on larger datasets and parameter tuning. The current KNN model is trained on a wide form data. With further development, we think it might prove more accurate when long form data is used. With more users and less movies, it is more likely to find neighbours in shorter distances thereby improving recommendations to the user. A smaller selection of movies also reduces the chance that the function provides users with unpopular movies and helps to get more valid feedback. However, the optimised model utilises an 80000*1400 matrix which takes up a lot of memory and causes timeout issues that we cannot deploy with our current app interface (source code is provided on github). Hopefully, this problem can be fixed in future iteration of this project.  

## Design of the Web App
As a user-oriented machine learning project, the ultimate goal is to present it to the audience, which means a smooth user experience is as critical as a good model. In this project, our website development and model design happened in parallel. Without any previous web design experience, we decided to use Streamlit, an open-source app framework designed specifically for Python-based data science projects, as our ultimate tool for web design and deployment. Despite the loss of some freedom in web design, this framework made it possible to deploy our project in a short period of time.

Starting with a bare-bone design, we iterated three versions during the development process, and our final UI design contains these three parts:
A model selection page
A page for Network + NLP Model
A page for Collaborative Filtering Model

<img src="/assets/Picture3.png" alt="drawing" width="700"/>
(The model selection page)

### Web page for Network + NLP Model
This page allows users to input two different movies, and use our networl+NLP model to generate a new one in real-time. To begin with, we put two text-input fields on the page, along with a submit button. Although our model can take imperfect spelling using fuzzy logic, it was really annoying for us to type in two different movies each time we test the app. To make the app testing easier for both us as developers and users who just want to play with the app, we also put a “Try Something Random!” button, so we don’t have to manually input movie names every time we open the app. The logic is pretty simple, right?

However, that’s the moment we found Streamlit was not as powerful as it sounds in the beginning. One big issue with Streamlit is that the framework refreshes the entire app whenever it takes a new input. This is reasonable because when a user interacts with the buttons and sliders, we want the content of the page, an interactive visualization, for example, to change along. However, this means it doesn’t allow us to go read the user’s inputs and feedback to the model or script more than one time. In our case, if we want to randomly select two movies and put them in the input box, after the “Try Something Random!” button is clicked, the random movies variables will be generated and removed at the same time, because the app refreshes!

To solve this issue, we created a temporary file to cache the random movies and read from that file at the beginning of each run. Although not a perfect solution, this workaround allows us to make this function possible.

The rest of the steps are much more straightforward for us. The web app will feed our model with two user-entered movies, then generate a new movie. Next, the app will find the corresponding movie information (such as title, cast, director, IMDb rating, introduction, etc.) from our metadata dictionary created in the previous steps, and display them nicely at the bottom of the page.

<img src="/assets/Picture4.png" alt="drawing" width="700"/>
(Example output from our Network+NLP model. When user input ironman + titanic, we got “The Fifth Element” as the result)

When time allowed, we’d also like to add movie posters to the result page as our next step. We found the TMDB API (https://developers.themoviedb.org/3/getting-started) can provide such services at no cost.

### Web page for Collaborative Filtering Model

With the previous experience, we paid extra attention to the management of user input information when designing this page. Usually, a collaborative filtering model will feed new users’ input back to the model, however, this was not possible given the time frame of this project and the limitations of Streamlit. To make it happen, we used user reviews found in the IMDb dataset as described in previous steps.

This page requires users to input their preferences on 8-10 random movies before generating the results. For UI design, we considered three options:
radio button
drop-down list
selection slider 
After a few rounds of testing and collecting feedback from family and friends, we decided to use the selection slider option. This design not only looks neater but can also be easily operated on mobile platforms. Unfortunately, when deploying this part using Streamlit, we found the font size and design of slider titles are not adjustable. The lesson we learn is that when the UI design of your data science web app is important, Streamlit may not be your best choice because of its limitations.

<img src="/assets/Picture5.png" alt="drawing" width="700"/>
(For better user experience, we also added a button to refresh the movie list, this is especially useful when the user hasn’t seen most of the movies in the list)

### Deployment with Streamlit

Deploying a web app with Streamlit is a breeze. Streamlit allows users to deploy their web app directly from their GitHub repo. Users can save secrets like API keys for each app when external databases like GoogleSheet API are used. Given GitHub can’t hold files with size > 100MB (there are workarounds, for example, GitHub Large File Storage), saving all original datasets online is clearly not an option. To minimize the memory run-time of each model, we removed any original datasets and only saved fully cleansed metadata and pickled trained models for the app to read from.

## Statement of work

The network-based model is implemented by Michael Conrad and the collabrative filtering model is implemented by Bojia Liu. The web app design and deployment is implemented by Chloe Zhang. 
