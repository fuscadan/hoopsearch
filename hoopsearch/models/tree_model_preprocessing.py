'''
    Created on Wed September  18 2019

    @author danie
    
    For each game, this script processes every paragraph in its recap article 
    in the following way:  A feature vector for that paragraph is constructed,
    and the paragraph is labelled as either similar or dissimilar to the 
    one-sentence descriptor appearing on the game summary page.  Feature 
    vectors and their labels are stored in a csv at Xy_DATA_PATH.

    This X-y data is used to train the decision tree model that predicts the
    most descriptive sentence of a given game article.
'''


import pandas as pd
import numpy as np
import random
from hoopsearch.common import features as ft
from hoopsearch.common.games import Game
from hoopsearch.common.constants import (Xy_DATA_PATH, RAW_DATA_PATH, 
    LABELLED_DATA_PATH)


def build_feat_vector(paragraph):
    feature_list = [ft.n_names(paragraph),
                    ft.n_teams(paragraph),
                    ft.n_numbers(paragraph),
                    ft.n_sentences(paragraph)]
    return feature_list


if __name__ == "__main__":
    # load raw data and its labels
    raw_data = pd.read_csv(RAW_DATA_PATH, index_col = 0)
    labels = pd.read_csv(LABELLED_DATA_PATH, index_col= 0)
    id_list = labels.index
    
    # Construct X, a list of feature vectors, and y, a list of labels for the
    # vectors in X.  This is the training data.  It is stored as a csv 
    # saved at Xy_DATA_PATH.  Each row of the outputted file contains the
    # feature vector and label of a single paragraph of a single game article,
    # and every paragraph from every game article is included in the final
    # data file.
    X = []
    y = []

    for game_id in id_list:
        game = Game(game_id, df_path=RAW_DATA_PATH)
        # pull a list of labels for the paragraphs in the current game article
        paragraph_labels = labels.loc[game_id].dropna()

        # match those labels with the feature vector of the corresponding
        # paragraph and append them to the lists y and X respectively.
        for i in range(len(paragraph_labels)):
            # there is a balance problem with the data, since in a given game
            # article, the ratio of paragraphs classified as "non-descriptive" 
            # and those classified as "descriptive" is maybe 30-to-1.  To 
            # compensate, we undersample from the "non-descriptive" set.
            if paragraph_labels[i] == 1:
                paragraph = game.article[i]
                X.append(build_feat_vector(paragraph))
                y.append(paragraph_labels[i])
            elif random.randint(0,29) == 0:
                paragraph = game.article[i]
                X.append(build_feat_vector(paragraph))
                y.append(paragraph_labels[i])
    
    Xy_df = pd.DataFrame([X,y]).transpose()
    Xy_df.to_csv(Xy_DATA_PATH)



