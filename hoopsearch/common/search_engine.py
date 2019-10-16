'''
    Created on Wed September  25 2019

    @author danie

    Takes a query and searches the database of NBA games
'''

import joblib
import pandas as pd
import numpy as np
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
from scipy import sparse
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from hoopsearch.common.summarizer import summarize
from hoopsearch.common.games import Game
from hoopsearch.models.LSA_model import LemmaTokenizer
import hoopsearch.common.features as ft
import hoopsearch.models.LSA_model as LSA_model
from hoopsearch.common.constants import (RAW_DATA_PATH, LSA_MODEL_PATH,
    FEATURES_PATH, ART_NAMES_PATH, TEAMS_PATH, LEADERS_PATH, PUNCTUATION,
    translator)


# load the LSA model and dataframes
LSA = joblib.load(LSA_MODEL_PATH)

df_features = pd.read_pickle(FEATURES_PATH)
df_teams = pd.read_pickle(TEAMS_PATH)
df_players = pd.read_pickle(LEADERS_PATH)
df_art_names = pd.read_pickle(ART_NAMES_PATH)

raw_data = pd.read_csv(RAW_DATA_PATH, index_col = 0)
ID_LIST = raw_data.index


def search(query, id_search_list = ID_LIST, VALIDATING = False, mode = 'LSA'):
    # the main search engine function. 


    global df_players
    global df_art_names
    # parse the query string
    q_teams = ft.get_teams(query)[1]
    q_players = ft.get_names(query)[1]
    q_LSA = LSA.transform([query])
    q_numbers = ft.get_numbers(query)

    # reduce the search, if possible, to games with teams mentioned in the query
    db_teams = sparse.csr_matrix(df_teams.values)
    similarities = cosine_similarity(q_teams, db_teams)

    reduced_list = [id_search_list[i] for i in similarities.nonzero()[1]]

    # if the list can be reduced, reduce it and take the appropriate sub-dataframe
    # of df_players
    if len(reduced_list) != 0:
        id_search_list = reduced_list
        df_art_names = df_art_names.loc[id_search_list].fillna(0).astype(int)
    

    # reduce the search, if possible, to games where players mentioned in 
    # the query show up in the article
    # db_art_names = sparse.csr_matrix(df_art_names.values)
    # similarities = cosine_similarity(q_players, db_art_names)

    # reduced_list = [id_search_list[i] for i in similarities.nonzero()[1]]

    # if len(reduced_list) != 0:
    #     id_search_list = reduced_list
    #     df_players = df_players.loc[id_search_list].fillna(0).astype(int)

    # reduce the search, if possible, to games with players mentioned in the query
    db_players = sparse.csr_matrix(df_players.values) 
    similarities = cosine_similarity(q_players, db_players)
    reduced_list = [id_search_list[i] for i in similarities.nonzero()[1]]

    if len(reduced_list) != 0:
        id_search_list = reduced_list


    # reduce the search, if possible, to games with numbers mentioned in the query
    reduced_list = []
    for game_id in id_search_list:
        if len([n for n in q_numbers if n in df_features.loc[game_id]['pts']]) > 0:
            reduced_list.append(game_id)

    if len(reduced_list) != 0:
        id_search_list = reduced_list

    # finally apply LSA context-matching (or BOW similarity) between the query 
    # and the games in the reduced list
    if mode == 'LSA':
        LSA_similarities = np.array([cosine_similarity(q_LSA, 
            df_features.loc[game_id]['LSA'])[0][0]
            for game_id in id_search_list])
    elif mode == 'BOW':

        X = []
        for game_id in ID_LIST:
            game = Game(game_id, df_path=RAW_DATA_PATH)

            full_article = ''
            for paragraph in game.article:
                full_article = full_article + paragraph + '\n'
            full_article = full_article.translate(translator)
            X.append(full_article)
        
        BOW_model = LSA_model.vectorizer.fit(X)

        q_bow = BOW_model.transform([query])

        BOW_similarities = []
        for game_id in id_search_list:
            game = Game(game_id, df=raw_data)

            full_article = ''
            for paragraph in game.article:
                full_article = full_article + paragraph + '\n'
            full_article = full_article.translate(translator)

            article_bow = BOW_model.transform([full_article])
            BOW_similarities.append(
                cosine_similarity(q_bow, article_bow)[0][0]
            )
        LSA_similarities = np.array(BOW_similarities)

    if VALIDATING == True:
        top_game_ids = [id_search_list[i] 
            for i in np.argsort(LSA_similarities)]
        top_game_ids.reverse()
        return top_game_ids
    else:
        top_game_ids = [id_search_list[i] 
            for i in np.argsort(LSA_similarities)[-10:]]
        top_game_ids.reverse()

        results = [(Game(game_id, df=raw_data).headline,
                    Game(game_id, df=raw_data).date,
                    summarize(game_id,raw_data),) 
                        for game_id in top_game_ids]

        return results

if __name__ == "__main__":
    
    query = 'close game exciting overtime high energy'
    results = search(query)

    print('\n')
    for result in results:
        print(result[0] + '\n\n' + result[1] + '\n' + result[2] + '\n')