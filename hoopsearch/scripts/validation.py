'''
    Created on Mon September  30 2019

    @author danie

    script to run validation tests.  First, a set number of games are randomly
    selected to serve as the validation corpus.
'''
# import sys
# sys.path.insert(1, '/mnt/c/Users/danie/OneDrive/Documents/Insight/')

import pandas as pd
import random
import ast
from hoopsearch.common.games import Game
from  hoopsearch.models.LSA_model import LemmaTokenizer
from hoopsearch.common.search_engine import search
from hoopsearch.common.summarizer import summarize

from hoopsearch.common.constants import RAW_DATA_PATH

JUDGEMENTS_PATH = 'hoopsearch/static/data/raw/relevancy_judgements.csv'

# set the size of the test corpus
TEST_CORP_SIZE = 100

raw_data = pd.read_csv(RAW_DATA_PATH, index_col=0)
id_list = raw_data.index


def display_headlines(id_list):
    for game_id in id_list:
        game = Game(game_id, df=raw_data)
        print('\n\n' + game.headline + '\n\n' + summarize(game_id,raw_data) 
                + '\n')
        input('continue? ')

def compute_AP(eval_list):
    n_relevant = 0
    n_results = 0
    cumulative_precision = 0
    for eval in eval_list:
        n_results = n_results + 1
        n_relevant = n_relevant + eval
        precision = n_relevant / n_results
        cumulative_precision = cumulative_precision + precision
    return cumulative_precision / len(eval_list)

def get_results(query,stop,mode='LSA'):
    top_results = search(query, VALIDATING=True, mode=mode)
    eval_list = []
    for i in range(0,stop):
        game_id = top_results[i]
        game = Game(game_id, df=raw_data)
        print('\n' + str(i) + '\n' + game.headline + '\n\n' + summarize(game_id,raw_data) 
                + '\n')
        eval = input('evaluate: ')
        eval_list.append(int(eval))
    return eval_list


if __name__ == "__main__":
    

    # set query for which you wish to compute the Average Precision
    query = 'thrilling overtime buzzer-beater buzzer beater close game'

    # set the path for the csv containing the test query, game ids, 
    # evaluations, and average precision
    AVERAGE_PRECISION_PATH = ('hoopsearch/static/data/validation/' 
                            + query + '.csv')

    # create a subset of TEST_CORP_SIZE id's
    test_list = [id_list[random.randint(0,len(id_list))] 
                for i in range(0,TEST_CORP_SIZE)]

    # set the number of results you wish to evaluate. Should be close to the
    # number of relevant documents in the full corpus.
    stop = 85

    # get results for the query and evaluate all results between 0 and 'stop'.
    # Evaluations are saved in a list.
    eval_list = get_results(query,stop)

    # compute the average precision for the query
    AP = compute_AP(eval_list)

    # put all the information above into a .csv if ever needed later.
    validation_quantities = {'test_ids' : [test_list],
                            'query' : [query],
                            'eval_list' : [eval_list],
                            'AP' : [AP]
                            }
    
    df = pd.DataFrame(validation_quantities)
    df.to_csv(AVERAGE_PRECISION_PATH)

    df = pd.read_csv(AVERAGE_PRECISION_PATH, index_col = 0)

    test_ids = ast.literal_eval(df['test_ids'].to_list()[0])