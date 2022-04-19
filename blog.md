# MADS Capstone - Project Movie Night

## Introduction
We started out with a simple problem to solve. Picture two people, showing up to movie night with two totally different movies, and neither of them want to compromise. Our goal is to create a compromise for them, by looking at the features that make their favorite movies their favorite and selecting a new movie that will make them both happy. Of course, we didn’t want to leave out those among us who enjoy a good movie alone, so we also wanted to create a similar solution when you can’t think of a movie to watch.

## Model #1 The Movie Combination Model

### Datasets & Feature Extraction
To start out, we needed movie data, and lots of it.

For combining two movies, we wanted to create our own custom formula that would be the summation of weighted scores, one score per feature. So for every feature, every movie in our database would be assigned a score that would reflect how close that particular movie matched the two input movies in regards to that particular feature. It’ll make more sense as we look at each individual feature and scoring system in turn.
 
**The first feature we looked as was cast members.**<br>
To begin, we created a network graph where movies titles were the nodes and the edges were the cast members. If two movies shared the same actor, they would be connected in the network. To generate the score, we took the two input movies and looked for all the paths between them included just one other node. That is we found all the movies that had a cast member in common with the first input movie and a cast member in common with the second input movie. All these movies were assigned the score of 2. Next we looked for all that paths between the inputs movies that included two nodes. That is, movies that had a cast member in common with one of the input movies and a cast member in common with any node that had a cast member in common with the other input movie. These movies were assigned a score of 1. All other movies were assigned a score of 0.

<img src="/assets/network.png" alt="drawing" width="700"/>
(Visualization of 1000 randomly sampled nodes from the cast graph, visualized using Gephi)


**The next feature we looked at was movie summaries.**<br>
To begin with vectorized the text of the summaries with a tfidf vectorizer and used them to find the cosine similarity between every movie. The plan from there was to use this cosine similarity matrix to identify movies that were most similar to both input movies, but the matrix proved too large to efficiently store in memory. Instead we used the cosine similarity matrix to train a Kmean classifiers and group the movies into 10 clusters. Then we could save each movies cluster membership in a vector that would be much smaller that the entire cosine similarity matrix. To produce the score, all the movies that matched the input movies’s clusters were give a 1 and all other movies given a 0.
 
**The next score we’re going to create is genre.** <br>
Initially, started with the simple approach of taking the genres from the input movies and assigning the genres where they intersect a score of 1 and all other genres a score of 0. But it quickly became apparent that many movie combinations had no intersect and so all genres would be assigned a score of zero. A quick solution to this would be to assign all of the input movie genres a score of 1, but that might fail to capture the combination of movies that we were looking for. So instead we counted how many times each genre was associated with every other genre. So now if the input movies had no intersecting genres, we could find the mostly closely associated genres and see if those intersected. This enabled many more movie combinations to have intersecting genres.

**The final two features we used were a popularity score and a voter rating score.** <br>
We used the respective scores of the two input movies to create a bounded range. Any movie with a score inside the range was assigned a 1 and any movie outside of it was assigned a 0. The purpose of this was to ensure that two blockbuster input movies would be less likely to produce a B movie and vice versa.

Now that we have the scores we needed to find a way to combine them in order to produce a meaningful, and accurate, output movie. To achieve this, we added a weight to adjust each score. We then sum each weighted score for each movie and output the movie with the highest score. Initially we’ve chosen scores that we think anecdotally make sense. Since we used a custom scoring method
