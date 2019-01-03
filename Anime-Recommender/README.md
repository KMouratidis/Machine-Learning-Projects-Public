
The motivation for this project was to get familiar with recommender systems (RecSys), but there are too many recommenders
for books and movies. I've seen implementations of the basic approaches to RecSys on anime, such as 
[this](https://www.kaggle.com/tianxinl0106/content-based-anime-recommender) and 
[this](https://www.kaggle.com/astandrik/simple-anime-recommendation-system-content-based) content-based RecSys but
suggestions are not really that great. [Mayank Bhatia's implementation](https://github.com/Mayank-Bhatia/Anime-Recommender)
is in the same boat, but more interesting. Still, all of these worked with 
[a much smaller dataset](https://www.kaggle.com/CooperUnion/anime-recommendations-database).
Instead, [Azathoth's data](https://www.kaggle.com/azathoth42/myanimelist/home) which contains ~80 million ratings, of which
I'm using ~21.8 million.

Then, there is one online recommender,
 [http://animesuggestions.com](http://animesuggestions.com), which allows you to add your preferences (including rating),
and having given it a list of ~40 ratings, it offered some really good results (12 already seen, although with various ratings, 11 that I
had on my watchlist, 1 that I could potentially be interested in, and 6 I wouldn't watch, half of which I wouldn't penalize
the recommender for).