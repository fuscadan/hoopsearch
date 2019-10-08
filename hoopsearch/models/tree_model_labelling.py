'''
    Created on Wed September  18 2019

    @author danie

        script to take a given game recap and label each paragraph (which I 
        think on ESPN are usually 1 sentence long) and label it as either 
        similar or dissimilar to the one-sentence descriptor appearing on the
        game summary page.
'''

# import sys
# sys.path.insert(1, '/mnt/c/Users/danie/OneDrive/Documents/Insight/')

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from hoopsearch.common.games import Game
from hoopsearch.common.constants import (LABELLED_DATA_PATH,
    RAW_DATA_PATH)


# load raw game data and list of game IDs
raw_data = pd.read_csv(RAW_DATA_PATH, index_col = 0)
id_list = raw_data.index


if __name__ == '__main__':
    # if a given paragraph in the article is sufficiently similar to the 
    # summary, label it with 1. Otherwise, label with 0. Do this for all game 
    # articles. Store all the labels in a Dataframe. Each row is a game 
    # (indexed by game ID), and the i^th column of a row is the label (0 or 1) 
    # of the i^th paragraph of the corresponding game's recap article.
    labels = pd.DataFrame()

    for game_id in id_list:
        try:
            game = Game(game_id, df_path=RAW_DATA_PATH)
            sentences = [game.summary] + game.article

            vectorizer = CountVectorizer()
            vectorized_list = vectorizer.fit_transform(sentences)

            paragraph_tags = []
            for i in range(len(game.article)):
                if (cosine_similarity(
                        vectorized_list[i+1],
                        vectorized_list[0])[0][0] 
                        > 0.75):
                    paragraph_tags.append(1)
                else:
                    paragraph_tags.append(0)
            
            new_row = pd.DataFrame([paragraph_tags], index=[game_id])  
            labels = labels.append(new_row)
        
        except:
            print('problem at game id ' + str(game_id))

    labels.to_csv(LABELLED_DATA_PATH)
