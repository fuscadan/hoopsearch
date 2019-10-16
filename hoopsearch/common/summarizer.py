'''
    Created on Thur September  18 2019

    @author danie

    Predict the most important sentence from a given game recap article.
'''


import joblib
from hoopsearch.common import features as ft
from hoopsearch.common.games import Game
from hoopsearch.common.constants import TREE_MODEL_PATH

model = joblib.load(TREE_MODEL_PATH)

def summarize(game_id, raw_data):
    game = Game(game_id, df=raw_data)
    candidates = []
    
    # for each paragraph in the given game's article, build a feature vector
    # and send it through the decision tree (model.predict). If the tree 
    #  
    # Send that vector 
    for paragraph in game.article:
        X = [[ft.n_names(paragraph),
                ft.n_teams(paragraph),
                ft.n_numbers(paragraph),
                ft.n_sentences(paragraph)]]

        if model.predict(X) == 1:
            candidates.append(paragraph)

    if len(candidates) != 0:
        return candidates[0] + '\n'
    else:
        return 'Summary not available. \n'



