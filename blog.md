# MADS Capstone - Project Movie Night

## Introduction
We started out with a simple problem to solve. Picture two people, showing up to movie night with two totally different movies, and neither of them want to compromise. Our goal is to create a compromise for them, by looking at the features that make their favorite movies their favorite and selecting a new movie that will make them both happy. Of course, we didn’t want to leave out those among us who enjoy a good movie alone, so we also wanted to create a similar solution when you can’t think of a movie to watch.

## Model #1 The Movie Combination Model

To start out, we needed movie data, and lots of it.

For combining two movies, we wanted to create our own custom formula that would be the summation of weighted scores, one score per feature. So for every feature, every movie in our database would be assigned a score that would reflect how close that particular movie matched the two input movies in regards to that particular feature. It’ll make more sense as we look at each individual feature and scoring system in turn.
 
### The first feature we looked as was cast members.
To begin, we created a network graph where movies titles were the nodes and the edges were the cast members. If two movies shared the same actor, they would be connected in the network. To generate the score, we took the two input movies and looked for all the paths between them included just one other node. That is we found all the movies that had a cast member in common with the first input movie and a cast member in common with the second input movie. All these movies were assigned the score of 2. Next we looked for all that paths between the inputs movies that included two nodes. That is, movies that had a cast member in common with one of the input movies and a cast member in common with any node that had a cast member in common with the other input movie. These movies were assigned a score of 1. All other movies were assigned a score of 0.

<img src="/assets/network.png" alt="drawing" width="700"/>
(Visualization of 1000 randomly sampled nodes from the cast graph, visualized using Gephi)


### The next feature we looked at was movie summaries.
To begin with vectorized the text of the summaries with a tfidf vectorizer and used them to find the cosine similarity between every movie. The plan from there was to use this cosine similarity matrix to identify movies that were most similar to both input movies, but the matrix proved too large to efficiently store in memory. Instead we used the cosine similarity matrix to train a Kmean classifiers and group the movies into 10 clusters. Then we could save each movies cluster membership in a vector that would be much smaller that the entire cosine similarity matrix. To produce the score, all the movies that matched the input movies’s clusters were give a 1 and all other movies given a 0.
 
### The next score we’re going to create is genre.
Initially, started with the simple approach of taking the genres from the input movies and assigning the genres where they intersect a score of 1 and all other genres a score of 0. But it quickly became apparent that many movie combinations had no intersect and so all genres would be assigned a score of zero. A quick solution to this would be to assign all of the input movie genres a score of 1, but that might fail to capture the combination of movies that we were looking for. So instead we counted how many times each genre was associated with every other genre. So now if the input movies had no intersecting genres, we could find the mostly closely associated genres and see if those intersected. This enabled many more movie combinations to have intersecting genres.

### The final two features we used were a popularity score and a voter rating score.
We used the respective scores of the two input movies to create a bounded range. Any movie with a score inside the range was assigned a 1 and any movie outside of it was assigned a 0. The purpose of this was to ensure that two blockbuster input movies would be less likely to produce a B movie and vice versa.

Now that we have the scores we needed to find a way to combine them in order to produce a meaningful, and accurate, output movie. To achieve this, we added a weight to adjust each score. We then sum each weighted score for each movie and output the movie with the highest score. Initially we’ve chosen scores that we think anecdotally make sense. Since we used a custom scoring method




## Design of the Web App
As a user-oriented machine learning project, the ultimate goal is to present it to the audience, which means a smooth user experience is as critical as a good model. In this project, our website development and model design happened in parallel. Without any previous web design experience, we decided to use Streamlit, an open-source app framework designed specifically for Python-based data science projects, as our ultimate tool for web design and deployment. Despite the loss of some freedom in web design, this framework made it possible to deploy our project in a short period of time.

Starting with a bare-bone design, we iterated three versions during the development process, and our final UI design contains these three parts:
A model selection page
A page for Network + NLP Model
A page for Collaborative Filtering Model

<img src="/assets/network.png" alt="drawing" width="700"/>
(The model selection page)

### Web page for Network + NLP Model

This page allows users to input two different movies, and use our networl+NLP model to generate a new one in real-time. To begin with, we put two text-input fields on the page, along with a submit button. Although our model can take imperfect spelling using fuzzy logic, it was really annoying for us to type in two different movies each time we test the app. To make the app testing easier for both us as developers and users who just want to play with the app, we also put a “Try Something Random!” button, so we don’t have to manually input movie names every time we open the app. The logic is pretty simple, right?

However, that’s the moment we found Streamlit was not as powerful as it sounds in the beginning. One big issue with Streamlit is that the framework refreshes the entire app whenever it takes a new input. This is reasonable because when a user interacts with the buttons and sliders, we want the content of the page, an interactive visualization, for example, to change along. However, this means it doesn’t allow us to go read the user’s inputs and feedback to the model or script more than one time. In our case, if we want to randomly select two movies and put them in the input box, after the “Try Something Random!” button is clicked, the random movies variables will be generated and removed at the same time, because the app refreshes!

To solve this issue, we created a temporary file to cache the random movies and read from that file at the beginning of each run. Although not a perfect solution, this workaround allows us to make this function possible.

The rest of the steps are much more straightforward for us. The web app will feed our model with two user-entered movies, then generate a new movie. Next, the app will find the corresponding movie information (such as title, cast, director, IMDb rating, introduction, etc.) from our metadata dictionary created in the previous steps, and display them nicely at the bottom of the page.

<img src="/assets/network.png" alt="drawing" width="700"/>
(Example output from our Network+NLP model. When user input ironman + titanic, we got “The Fifth Element” as the result)

When time allowed, we’d also like to add movie posters to the result page as our next step. We found the TMDB API (https://developers.themoviedb.org/3/getting-started) can provide such services at no cost.

### Web page for Collaborative Filtering Model

With the previous experience, we paid extra attention to the management of user input information when designing this page. Usually, a collaborative filtering model will feed new users’ input back to the model, however, this was not possible given the time frame of this project and the limitations of Streamlit. To make it happen, we used user reviews found in the IMDb dataset as described in previous steps.

This page requires users to input their preferences on 8-10 random movies before generating the results. For UI design, we considered three options:
radio button
drop-down list
selection slider 
After a few rounds of testing and collecting feedback from family and friends, we decided to use the selection slider option. This design not only looks neater but can also be easily operated on mobile platforms. Unfortunately, when deploying this part using Streamlit, we found the font size and design of slider titles are not adjustable. The lesson we learn is that when the UI design of your data science web app is important, Streamlit may not be your best choice because of its limitations.

<img src="/assets/network.png" alt="drawing" width="700"/>
(For better user experience, we also added a button to refresh the movie list, this is especially useful when the user hasn’t seen most of the movies in the list)

### Deployment with Streamlit

Deploying a web app with Streamlit is a breeze. Streamlit allows users to deploy their web app directly from their GitHub repo. Users can save secrets like API keys for each app when external databases like GoogleSheet API are used. Given GitHub can’t hold files with size > 100MB (there are workarounds, for example, GitHub Large File Storage), saving all original datasets online is clearly not an option. To minimize the memory run-time of each model, we removed any original datasets and only saved fully cleansed metadata and pickled trained models for the app to read from.


