"""
    Created on Thurs September  19 2019

    @author danie

    Script to scrape a list of all NBA players' first and last names with no
    duplicates.
"""

from bs4 import BeautifulSoup
import urllib3
import certifi

# path of the file to be created and filled with player names
NAMES_PATH = 'hoopsearch/static/data/raw/nba_player_names.txt' 


# connect to each player list page on basketball-reference.com (one page per 
# letter in the alphabet) and scrape all player names that appear. Add those 
# names to a set (to avoid duplicates) and write to the file at NAMES_PATH.
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())

ALPHABET = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
    'q', 'r','s','t','u','v','w','y','z']

nba_names = set()

for letter in ALPHABET:
    url = 'https://www.basketball-reference.com/players/' + letter + '/'
    r = http.request('GET' , url)
    soup = BeautifulSoup(r.data, 'html.parser')
    tags = soup.find_all('th')

    for tag in tags[8:]: 
        full_name = tag.get_text().split(' ')
        for name in full_name:
            nba_names.add(name.strip('*')) 

with open(NAMES_PATH,'w') as file:
    for name in nba_names:
        file.write(name + '\n')

