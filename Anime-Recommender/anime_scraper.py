import requests
import re
import time
import sqlite3
import pandas as pd
import numpy as np
from tqdm import tqdm
from string import punctuation
from bs4 import BeautifulSoup as BS

# Get the list of anime that we are interested in
# (these are the filtered series)
with open("filtered_anime_list.txt", 'r') as f:
    anime_list = f.read()[:-1].split("\n\n")

# Connect to the database
conn = sqlite3.connect("anime.db")
curr = conn.cursor()
# Get all (id,title) pairs
anime_ids = curr.execute("SELECT anime_id, title FROM anime").fetchall()
# Dataframe for convenience
sel = pd.DataFrame(anime_ids, columns=["IDs", "title"]).set_index("title")
# Select only those present in the list 
sel = sel[sel.index.isin(anime_list)]
# Create links for each anime
sel = sel["IDs"].apply(lambda x: "https://myanimelist.net/anime/{}".format(x))

# print(sel.head())

rating_names = ['Overall', 'Story', 'Animation', 'Sound', 'Character', 'Enjoyment']

# Crawler, returns a list of 10 features (4 top reviews -text- and their average ratings)
def get_anime_features(anime_name="Lovely★Complex"):
    
    # Polite crawling 
    time.sleep(3)
    
    try:
        url = sel[anime_name]
        resp = requests.get(url)
        soup = BS(resp.text, 'lxml')

	    # Save the whole page so if we need more data
        # we don't have to scrape MAL again
        # Also, clear the name of punctuation so that it doesn't mess with the file system
        file = "anime_pages/"+"".join(c if c not in punctuation else " " for c in anime_name )+".html"
        with open(file, 'w') as f:
            written = f.write(resp.text)
            if written < 10:
                print("Something might have went wrong with:", anime_name)


	    description = soup.find("span", {"itemprop":"description"}).text

        reviews_list = []
        ratings_list = []
	
        for review in soup.findAll("div", {"class":"spaceit textReadability word-break pt8 mt8"}):
            # replace whitespace, remove the first part (ratings)
            reviews_list.append(re.sub("\s+", " ", review.text.split("Enjoyment")[1][3:].strip()))
            # take the ratings and typecast them to an array
            ratings_list.append(np.array([t.text for t in review.findAll('td')]).reshape((6,2))[:,1].astype(int))

        # if reviews were found, average the 4 ratings (per category)
        # else create 10 empty entries
	    if ratings_list:
            reviewer_ratings = np.array(ratings_list).mean(0) # shape: (6,) 
        else:
            reviews_list = [0] * 4
            ratings_list = [0] * 6

        # create a feature row by concatenating the reviews with the average ratings
        features = [description] + reviews_list + list(reviewer_ratings)

        
            
        return features
    except Exception as e:
        print("Something went wrong with:", anime_name)
        print(e)
        log.write("Error: {}\nAnime: {}\n".format(e, anime_name))
        return [0] * 11
        


if __name__ == "__main__":
    log = open("scraping_log.txt", 'w')
    feats = [get_anime_features(name) for name in tqdm(anime_list)]
    log.close()
    df = pd.DataFrame(feats, columns="Description Reviwer1 Reviwer2 Reviwer3 Reviwer4".split()+rating_names, index=anime_list)
    #print(df.head())
    df.to_excel("anime_additional_features.xlsx")
