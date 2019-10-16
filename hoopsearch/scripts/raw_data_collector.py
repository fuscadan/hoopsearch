'''
    simple script to scrape basic NBA game data from ESPN using the 'games' 
    module and store the data in a pandas dataframe. Exports a .csv file at
    location specified by RAW_DATA_PATH.  Web pages to scrape are identified
    by a list of game IDs in ID_FILE_PATH (defined in constants.py).  IDs for 
    web pages that could not be accessed are recorded in ID_RETRY_PATH. 

    This script can be run in a 'retry' mode that will scrape game data for
    the IDs stored in ID_RETRY_PATH.  Retrying is important since web pages 
    that would not load for certain IDs (the IDs in ID_RETRY_PATH) can often
    be loaded if you try again. 
'''

import pandas as pd
from hoopsearch.common.games import Game
from hoopsearch.common.constants import (ID_FILE_PATH, ID_RETRY_PATH, 
    RAW_DATA_PATH)

# Set RETRYING to True if you're scraping game info for IDs in 'ID_RETRY_PATH'
RETRYING = True

def game_scrape(id_list):
    df = pd.DataFrame()
    errors = []
    for game_id in id_list:
        # a few game pages have variations in the standard html structure that 
        # will not be parsed correctly by the BeautifulSoup code in the Game 
        # class.  A simple try catch handles these exceptions.
        try:
            game = Game(game_id)
            new_row = pd.DataFrame(game.to_dict() , index=[game_id])
            df = df.append(new_row)
        except:
            print('missing data at game id ' + game_id)
            errors.append(game_id)
    
    return df, errors


if __name__ == '__main__':
    # read the game ids from the text file, and add raw game data row by row
    # into the dataframe df.  Write the dataframe containing raw game data to a 
    # csv file.

    if RETRYING == True:
        file_path = ID_RETRY_PATH
    else:
        file_path = ID_FILE_PATH

    with open(file_path, 'r') as id_file:
        id_list = id_file.readlines()

    df, errors = game_scrape(id_list)

    with open(ID_RETRY_PATH, 'w') as err_file:
        for game_id in errors:
            err_file.write(game_id)        

    if RETRYING == True:
        with open(RAW_DATA_PATH, 'a') as f:
            df.to_csv(f, header=False)
    else:
        df.to_csv(RAW_DATA_PATH)