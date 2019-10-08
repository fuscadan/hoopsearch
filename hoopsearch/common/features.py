'''
    Created on Wed September  18 2019

    @author danie

    Definition of features that a string (typically a paragraph in a game 
    recap) may have. Used to construct feature vectors.
'''

from sklearn.feature_extraction.text import CountVectorizer
from hoopsearch.common.games import Game
from hoopsearch.common.constants import (RAW_DATA_PATH, NAMES_LIST_PATH,
    TEAMS_LIST_PATH)



with open(NAMES_LIST_PATH,'r') as names_file:
    names = names_file.read().split('\n')
with open(TEAMS_LIST_PATH,'r') as teams_file:
    teams = teams_file.read().split('\n')

names_vectorizer = CountVectorizer()
names_bow = names_vectorizer.fit(names) 
teams_vectorizer = CountVectorizer()
teams_bow = teams_vectorizer.fit(teams)

def n_numbers(paragraph):
    # Count the number of numbers (word or digits) appearing in paragraph
    number_words = ['one','two','three','four',
        'five','six','seven','eight','nine']
    n_num = len([s for s in paragraph.split() 
                    if s.isdigit() or s in number_words])

    # count the number of strings of the form "125-536" (game scores)
    possible_scores = [s for s in paragraph.split() if '-' in s]
    n_scores = len([s for s in possible_scores 
                    if 2 == len([i for i in s.split('-') if i.isdigit()])])
    
    return n_num + n_scores

def n_names(paragraph):   
    return len([s for s in paragraph.split() if s in names])

def n_teams(paragraph):   
    return len([s for s in paragraph.split() if s in teams])

def n_sentences(paragraph):
    return len(paragraph.split('.')) - 1

def get_names(paragraph):
    names_list = [s for s in paragraph.split() if s in names]
    names_tokens = names_bow.transform([paragraph])
    return names_list, names_tokens

def get_teams(paragraph):
    teams_list = [s for s in paragraph.split() if s in teams]
    teams_tokens = teams_bow.transform([paragraph])
    return teams_list, teams_tokens

def has_pts(paragraph):
    for s in ['point', 'points', 'pt', 'pts']: 
        if s in paragraph.lower().split():
            return True
    return False

def has_reb(paragraph):
    for s in ['rebound', 'rebounds', 'reb']: 
        if s in paragraph.lower().split():
            return True
    return False

def has_ast(paragraph):
    for s in ['assist', 'assists', 'ast']: 
        if s in paragraph.lower().split():
            return True
    return False

def get_numbers(paragraph):
    numbers = [int(s) for s in paragraph.split() if s.isdigit()]
    return numbers
    

if __name__ == "__main__":
    game_id = 400899380

    game = Game(game_id,df_path=RAW_DATA_PATH)

    paragraph_number = 4
    paragraph = game.article[paragraph_number]

    n_numbers(paragraph)

    print('For game with id {0}, paragraph {1} has {2} numbers, \
            {3} player names, and {4} team names'.format(str(game_id), 
            str(paragraph_number),
            str(n_numbers(paragraph)),
            str(n_names(paragraph)),
            str(n_teams(paragraph)),))
