# MADS Capstone - Project Movie Night

## Introduction
We started out with a simple problem to solve. Picture two people, showing up to movie night with two totally different movies, and neither of them want to compromise. Our goal is to create a compromise for them, by looking at the features that make their favorite movies their favorite and selecting a new movie that will make them both happy. Of course, we didn’t want to leave out those among us who enjoy a good movie alone, so we also wanted to create a similar solution when you can’t think of a movie to watch.

## Datasets & Feature Extraction
To start out, we needed movie data, and lots of it.

For combining two movies, we wanted to create our own custom formula that would be the summation of weighted scores, one score per feature. So for every feature, every movie in our database would be assigned a score that would reflect how close that particular movie matched the two input movies in regards to that particular feature. It’ll make more sense as we look at each individual feature and scoring system in turn.
 
**The first feature we looked as was cast members.**<br>
To begin, we created a network graph where movies titles were the nodes and the edges were the cast members. If two movies shared the same actor, they would be connected in the network. To generate the score, we took the two input movies and looked for all the paths between them included just one other node. That is we found all the movies that had a cast member in common with the first input movie and a cast member in common with the second input movie. All these movies were assigned the score of 2. Next we looked for all that paths between the inputs movies that included two nodes. That is, movies that had a cast member in common with one of the input movies and a cast member in common with any node that had a cast member in common with the other input movie. These movies were assigned a score of 1. All other movies were assigned a score of 0.

