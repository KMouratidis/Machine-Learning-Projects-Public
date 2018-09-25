from .utilities import load_dataset, anime_list
import pandas as pd
import numpy as np
from collections import defaultdict

# fow show
username = "kmourat"

# if the user does not provide values then
# they will be assumed to be 0
# user_ratings should be a dict
def predict_anime(user_ratings, df, *, model=None, corrs=None,
                  anime_list=anime_list, username=username):
    # Create an empty user DataFrame (for convenience)
    user = pd.DataFrame(columns=anime_list, index=[username])

    # Since lack of ratings means zeros, their sum can be used as a boolean
    if sum(user_ratings.values()):

        for anime, rating in user_ratings:
            user[anime] = rating

        # fill missing values just like we did in the
        # dataset preprocessing phase
        user = user - user.min(1).values[0]
        user = user / user.max(1).values[0]
        user = user.fillna(user.mean(1).values[0])

        # vectorize
        user_features = user @ features
        # normalize
        user_features = user_features.apply(lambda x: x / x.max(), 1)

        preds = model.predict(user_features)
        preds = pd.DataFrame([preds[0,:]], columns=anime_list, index=[username])
        preds = preds.T.sort_values(username, ascending=False)
        preds = preds[~preds.index.isin(user_list)]

        return preds

    # some other model, here correlation
    else:
        results = corrs[anime_list]
        pd.DataFrame(results, columns=[username])

        results = results[~results.index.isin(user_ratings.keys()
                            )].mean(1).sort_values(ascending=False).head(n)
        results = pd.DataFrame(results, columns=[username])

        return results
