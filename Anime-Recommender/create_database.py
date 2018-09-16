import sqlite3
import re
from sklearn.feature_extraction import DictVectorizer
from collections import Counter
import pandas as pd
import numpy as np
import os

# I intentionally don't check for existing DB/tables
# TODO: maybe check and throw an error ?
conn = sqlite3.connect("anime.db")
db = conn.cursor()


## USERS
print("Creating users table...")
df = pd.read_csv("anime/users_filtered.csv")
# Dropped users who (supposedly) watched more than
# 100,000 episodes watching these (~20 minutes each,
# for 12 hours a day, for 365 days a year) should take
# about 10-15 years, which I find highly unlikely (aka
# outliers). This removed less than 100 users, so it
# shouldn't affect the recommender a lot. access_rank
# is a null column (the only one). I'm also dropping
# columns I don't plan to use
df = df[df["stats_episodes"]<1e5].drop(["access_rank", "join_date",
                                        "last_online", "user_days_spent_watching",
                                         "user_plantowatch",], axis=1)
# Save to table named users
df.to_sql("users", conn, index=False)

## RATINGS
print("Creating ratings table...")
# Use the same name to reclaim memory
df = pd.read_csv("anime/animelists_filtered.csv")
df.drop(["my_last_updated", "my_tags",
         "my_start_date", "my_finish_date"],
        axis=1, inplace=True)
df.to_sql("ratings", conn, index=False)

## ANIME
print("Creating anime and genres tables")
df = pd.read_csv("anime/AnimeList.csv")
# Cleaning titles a bit by combining them all (except the main title) in one column
df["alt_title"] = (df["title_english"] +" (" + df["title_japanese"]+"," + df["title_synonyms"] + ")")
# Convert dates, set unknowns to 2001 (useful for when <2000 will be dropped)
df["start_year"] = pd.to_datetime(df["aired"].apply(lambda x: eval(x)["from"]).fillna('2001-01-01'))
df["start_year"] = df["start_year"].apply(lambda x: x.year)
# Dropping other columns I don't plan to use
df.drop(["title_english", "title_japanese", "title_synonyms",
         "airing", "broadcast", "background", "licensor",
         "opening_theme", "ending_theme", "aired"], axis=1, inplace=True)
# Convert duration to numeric
df["duration"] = df["duration"].apply(lambda x: x.split()[0] if len(x.split())>1 and 'min' in x.split()[1] else '0').str.replace("Unknown", '0').astype(int)
# This creates a set of all different genres
genres = set([f for y in df["genre"].tolist()
              for x in [y.split(", ") if isinstance(y,str) else "None"]
              for f in x if len(f)>1]).union(['None'])
# A feature DataFrame where the columns are the genres
# The rows are the different anime (titles in the first row)
df_genres = pd.DataFrame(df[['title','genre']])
for genre in genres:
    df_genres[genre] = 1 * df_genres["genre"].str.contains(genre)

df_genres.drop('genre', 1, inplace=True)

# save both
df.to_sql("anime", conn, index=False)
df_genres.to_sql("genres", conn, index=False)


# No need to commit, just close
print("Closing...")
conn.close()
