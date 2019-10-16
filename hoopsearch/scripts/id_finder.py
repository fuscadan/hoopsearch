"""
Created on Mon September  16 2019

@author: danie

    This program creates a list of ESPN NBA game ID numbers by visiting each
    team's schedule page for each year in the selected range and scraping the 
    IDs for home games (to avoid double-counting).  Game IDs may be found for
    either the regular season or the postseason. 
    
    The parameters (range of seasons, type of season) for the scrape are 
    stored in 'constants.py', since these settings are fixed throughout the
    project and affect the naming conventions of files created in other 
    scripts.

    The ID numbers are saved to a file: 
        "espn_game_ids_(season type)_(start year)-(end year).txt"
"""

import urllib3
import certifi
from bs4 import BeautifulSoup
from hoopsearch.common.constants import (START_YEAR, 
    END_YEAR, SCHEDULE_ROOT, SEASON_TYPE, ID_FILE_PATH, URL_RETRY_PATH, 
    TEAM_ABBREVIATIONS)

# Set RETRYING to True if you're scraping game IDs from 'retries.txt'
RETRYING = True

def get_ids(urls):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())

    retry = []
    ids = []
    for url in urls:
        r = http.request('GET', url)

        if r.status != 200:
            retry.append(url)

        soup = BeautifulSoup(r.data, 'html.parser')

        n_games_in_season = len(soup.select('.ml4 a'))
        for i in range(n_games_in_season):
            # find the tag with the href link to the i^th game and grab the 
            # game ID as an integer
            game_link_tag = soup.select('.ml4 a')[i]
            game_id = game_link_tag.get('href')[-9:]

            # find the tag with the "vs" or "@" string (indicating whether the 
            # game was at home or not) and grab that string
            location_tag = game_link_tag.parent.parent.previous_sibling
            game_location = location_tag.select('.pr2')[0].text
                        
            # Only track game IDs of home games to avoid double-counting when 
            # the schedules of every team are scraped.
            if game_location == 'vs':
                ids.append(game_id)
    return ids, retry


if __name__ == '__main__':
    # Find ESPN game IDs from the webpages displaying the season schedule of
    # each team.  
    
    # decide if the list of season schedule urls should come from 
    # URL_RETRY_PATH (i.e. if you are retrying a previous id scrape that 
    # missed urls) or if the list of urls should be built from the START_YEAR,
    # END_YEAR and SEASON_TYPE data supplied in 'constants.py' (i.e. if you
    # are starting a new id scrape).
    if RETRYING == True:
        file_path = URL_RETRY_PATH
        with open(file_path, 'r') as url_file:
            urls = url_file.readlines()
    else:
        urls = []
        for year in range(START_YEAR, END_YEAR + 1):
            for team in TEAM_ABBREVIATIONS:
                url = (SCHEDULE_ROOT 
                    + team 
                    + '/season/' 
                    + str(year) 
                    + '/seasontype/' 
                    + str(SEASON_TYPE)
                    ) 
                urls.append(url)

    # get a list of game IDs from the list of urls, and get a list of urls
    # that could not be accessed and need to be retried
    ids, retry = get_ids(urls)

    # save the urls that could not be accessed to URL_RETRY_PATH
    with open(URL_RETRY_PATH, 'w') as err_file:
        for url in retry:
            err_file.write(url + '\n')        

    # either write the scraped game IDs to ID_FILE_PATH or append IDs to an 
    # existing file if in retry mode
    if RETRYING == True:
        id_write_mode = 'a'
    else:
        id_write_mode = 'w'

    with open(ID_FILE_PATH, id_write_mode) as f:
        for id in ids:
            f.write(id + '\n')

