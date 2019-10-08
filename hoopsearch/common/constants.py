"""
    Created Mon  Oct 7 2019

    @author: danie

    List of constants 
"""

# parameters for the scope of the scrape in id_finder.py
START_YEAR = 2003
END_YEAR = 2009
SEASON_TYPE = 2     #see SEASON_TYPE_NAMES below

# static elements of the urls that are to be looked up. Typical format:
# http://www.espn.com/nba/team/schedule/_/name/wsh/season/2016/seasontype/2
SCHEDULE_ROOT = 'http://www.espn.com/nba/team/schedule/_/name/'
TEAM_ABBREVIATIONS = ['atl', 'bos', 'bkn', 'cle', 'cha', 'chi', 'dal', 'den', 
    'det', 'gs', 'hou', 'ind', 'lac', 'lal', 'mem', 'mia', 'mil', 'min', 'no', 
    'ny', 'okc', 'orl', 'phi', 'phx', 'por', 'sac', 'sa', 'tor', 'utah', 'wsh']
SEASON_TYPE_NAMES = {1 : 'preseason', 2 : 'regular_season' , 3 : 'postseason'} 

# file path strings
RELATIVE_PATH = 'hoopsearch/'
ID_FILE_PATH = (RELATIVE_PATH
    + 'data/raw/' 
    + 'espn_game_ids_{0}_{1}-{2}.txt'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )
URL_RETRY_PATH = RELATIVE_PATH + 'data/raw/id_retry_urls.txt'




RAW_DATA_PATH = (RELATIVE_PATH 
    + 'data/raw/' 
    + 'raw_data_{0}_{1}-{2}.csv'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )
ID_RETRY_PATH = RELATIVE_PATH + 'raw/error_ids.txt'


LABELLED_DATA_PATH = (RELATIVE_PATH 
    + 'processed/' 
    + 'labels_{0}_{1}-{2}.csv'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )

Xy_DATA_PATH = (RELATIVE_PATH 
    + 'processed/'
    + 'Xy_data_balanced_{0}_{1}-{2}.csv'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )



LSA_MODEL_PATH = RELATIVE_PATH + 'models/lsa_model.joblib'


FEATURES_PATH = (RELATIVE_PATH 
    + 'data/processed/'
    + 'game_features_{0}_{1}-{2}.pickle'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )
ART_NAMES_PATH = (RELATIVE_PATH 
    + 'data/processed/'
    + 'article_names_{0}_{1}-{2}.pickle'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )
TEAMS_PATH = (RELATIVE_PATH 
    + 'data/processed/'
    + 'teams_{0}_{1}-{2}.pickle'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )
LEADERS_PATH = (RELATIVE_PATH 
    + 'data/processed/'
    + 'leaders_{0}_{1}-{2}.pickle'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )

# objects related to cleaning punctuation from text
PUNCTUATION = '!"#$%&\'()*+,./;<=>?@[\\]^_`{|}~'
translator = str.maketrans('', '', PUNCTUATION)


NAMES_LIST_PATH = RELATIVE_PATH + 'data/raw/nba_player_names.txt' 
TEAMS_LIST_PATH = RELATIVE_PATH + 'data/raw/nba_team_names.txt'


TREE_MODEL_PATH = RELATIVE_PATH + 'models/tree_model_balanced.joblib'