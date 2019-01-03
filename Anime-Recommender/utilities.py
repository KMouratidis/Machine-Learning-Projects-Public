import pandas as pd
import numpy as np
import sqlite3

conn = sqlite3.connect("anime.db")
curr = conn.cursor()

with open("anime_list.txt") as f:
    anime_list = f.read()
    anime_list = anime_list.split("\n")[:-1] # last one is an empty line

def load_dataset(min_episodes=6, min_year=1999, min_score='avg',
                 scored_by=4999, min_ep_duration=7, drop_second_seaons=False,
                 normalize_users=True, scaling="min_max",
                 also_create_features=True, text_features=False,
                 save=False):
    """
    min_score: 'avg' or float.
    scaling: 'min_max' or 'zero_mean'.
    """

    min_score = "(SELECT AVG(score) FROM anime)" if min_score=='avg' else min_score

    query = r"""SELECT ratings.username, anime.title, ratings.my_score FROM ratings
    INNER JOIN anime ON anime.anime_id = ratings.anime_id
    WHERE anime.scored_by>{}
    AND anime.episodes>={}
    AND anime.start_year>{}
    AND anime.score > {}
    AND anime.duration > {}""".format(scored_by,min_episodes, min_year,
                                                   min_score, min_ep_duration)

    df = pd.read_sql(query, conn)
    # Each user should rate at least 10 anime
    # Typecast to float32 to save memory
    df = df.pivot_table("my_score", "username", "title").dropna(thresh=10,
                                                                axis=0).astype(np.float32)
    # For every user, rate each anime with the user average
    # conversion of boolean to 0/1
    df = df.apply(lambda x: x.fillna(x.mean()), axis=1*(not normalize_users))
    # For every user we are subtracting the mean (if normalize_users is True)
    if scaling == "zero_mean":
        df = df.apply(lambda x: x - x.mean(), axis=1)
    elif scaling == "min_max":
        # For every user subtract the minimum and divide by the maximum
        # so we get data in the range of 0-1 which can be interpreted
        # as a percentage rating
        df = df.apply(lambda x: x - x.min(), axis=1*normalize_users)
        df = df.apply(lambda x: x / x.max(), axis=1*normalize_users)
    else:
        print("[IMPORTANT INFO]: No scaling!")

    if drop_second_seaons:
        # drop (some) second seasons
        df.drop([x for x in df.columns if '2nd' in x], 1, inplace=True)

    feats = None
    if also_create_features:
        feats = pd.read_sql("SELECT * FROM features", conn).set_index('title')
        feats = feats.loc[df.columns]
        if not text_features:
            feats = feats.drop(["Reviwer1", "Reviwer2", "Reviwer3",
                                        "Reviwer4", "Description"], 1)
        # Handles missing values
        feats = feats.apply(lambda x: x.fillna(x.mean())
                                if x.dtype==np.float32 else x.fillna(0), 0)
        feats = feats.astype(np.float32)

    if save:
        df.to_csv("user_ratings.csv")
        feats.to_csv("features.csv")
    else:
        return df, feats
