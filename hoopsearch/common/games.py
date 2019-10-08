'''
Created on Tue September  17 2019

@author: danie

    Defines a class 'Game'.
'''


from bs4 import BeautifulSoup
import urllib3
import certifi
import pandas as pd
import ast

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())

game_summary_root = 'https://www.espn.com/nba/game?gameId='
game_article_root = 'https://www.espn.com/nba/recap?gameId='

class Game:
    
    def __init__(self,game_id,df_path=None, df=None):
        # cast the given game ID to an int if given as a str
        if type(game_id) == str:
            game_id = int(game_id.strip())
        
        # if a path to a local file is given, load game info from that file
        if df is not None:
            game_row = df.loc[game_id]
            
            self.headline = game_row['headline']
            self.summary = game_row['summary']
            self.article = ast.literal_eval(game_row['article'])
            self.date = game_row['date']
            self.winner = game_row['winner']            
            self.names = ast.literal_eval(game_row['names'])
            self.scores = ast.literal_eval(game_row['scores'])
            self.quarters = game_row['quarters']
            self.pts = ast.literal_eval(game_row['pts'])
            self.reb = ast.literal_eval(game_row['reb'])
            self.ast = ast.literal_eval(game_row['ast'])

        elif df_path is not None:
            df = pd.read_csv(df_path, index_col = 0)
            game_row = df.loc[game_id]
            
            self.headline = game_row['headline']
            self.summary = game_row['summary']
            self.article = ast.literal_eval(game_row['article'])
            self.date = game_row['date']
            self.winner = game_row['winner']            
            self.names = ast.literal_eval(game_row['names'])
            self.scores = ast.literal_eval(game_row['scores'])
            self.quarters = game_row['quarters']
            self.pts = ast.literal_eval(game_row['pts'])
            self.reb = ast.literal_eval(game_row['reb'])
            self.ast = ast.literal_eval(game_row['ast'])
        
        # if no path to a local data file is given, scrape game info from web
        else:
            # get the game recap article and store it as a list of strings

            # grab the html from the game recap page, eg:
            # https://www.espn.com/nba/recap?gameId=400899380
            url = game_article_root + str(game_id)
            r = http.request('GET' , url)
            soup = BeautifulSoup(r.data, 'html.parser')

            article_tag = soup.select('.article-body')[0]
            paragraphs = article_tag.find_all('p')
            
            article = []
            for i in range(len(paragraphs)):
                article.append(paragraphs[i].get_text())
            
            self.article = article


            # get other game features from the game summary page

            # grab the html from the game summary page, eg:
            # https://www.espn.com/nba/game?gameId=400899380
            url = game_summary_root + str(game_id)
            r = http.request('GET' , url)
            soup = BeautifulSoup(r.data, 'html.parser')

            # the headline and summary appear just below the top banner
            self.headline = soup.select('.top-stories__story-header h1')[0].text
            self.summary = soup.select('p' '.webview-internal')[0].text

            # grab the date the game was played
            self.date = soup.find_all("span", 
                attrs={"data-behavior": "date_time"})[0].get('data-date')[:10] 

            # locate the tags containing the info in the top banner
            top_banner = soup.select('.competitors')[0]
            # examine the tags containing the away and home team's data
            away_tag = top_banner.find_all('div', 
                                            attrs={'class': 'team away'})[0]
            home_tag = top_banner.find_all('div', 
                                            attrs={'class': 'team home'})[0]
            # examine the tag containing the box score
            score_tag = top_banner.select('.game-status')[0]
            away_scores_tags = list(score_tag.find_all('tr')[1].children)
            home_scores_tags = list(score_tag.find_all('tr')[2].children)

            # who won the game
            self.winner = top_banner.parent['class'][-1][:4]

            # get the variations of the home and away team's name and city
            self.names = { 'away' : {'team' : away_tag.select('.short-name')[0].text,
                                'city' : away_tag.select('.long-name')[0].text,
                                'abbr' : away_tag.select('.abbrev')[0].text} ,
                      'home' : {'team' : home_tag.select('.short-name')[0].text,
                                 'city' : home_tag.select('.long-name')[0].text,
                                 'abbr' : home_tag.select('.abbrev')[0].text} }
            
            # find the number of quarters played ( >4 if game goes to OT )
            number_of_quarters = len(away_scores_tags) - 2
            self.quarters = number_of_quarters

            # build lists containing the home and away team scores. Total scores
            # at index 0, quarterly scores stored at the following indices.
            away_scores = [int(away_scores_tags[number_of_quarters + 1].text)]
            for quarter in range(number_of_quarters):
                away_scores.append(int(away_scores_tags[quarter + 1].text))
            
            home_scores = [int(home_scores_tags[number_of_quarters + 1].text)]
            for quarter in range(number_of_quarters):
                home_scores.append(int(home_scores_tags[quarter + 1].text))
            
            self.scores = { 'away' : away_scores, 'home' : home_scores}


            # pull data on leaders in pts, reb, ast from "Game Leaders" panel. 
            # Each category has a dictionary containing player name, etc
            leader_tags = soup.select('.leader-column')
     
            away_pts_tags = leader_tags[0].select('.game-leader-details')[0].find_all('dd')
            home_pts_tags = leader_tags[0].select('.game-leader-details')[1].find_all('dd')
            
            self.pts = { 'away' : {'leader' : leader_tags[0].select('.long-name')[0].text,
                                   'pts' : int(away_pts_tags[0].select('.value')[0].text),
                                   'fg' : away_pts_tags[1].select('.value')[0].text,
                                   'ft' : away_pts_tags[2].select('.value')[0].text} ,
                        'home' : {'leader' : leader_tags[0].select('.long-name')[1].text,
                                   'pts' : int(home_pts_tags[0].select('.value')[0].text),
                                   'fg' : home_pts_tags[1].select('.value')[0].text,
                                   'ft' : home_pts_tags[2].select('.value')[0].text} }
    
            away_reb_tags = leader_tags[1].select('.game-leader-details')[0].find_all('dd')
            home_reb_tags = leader_tags[1].select('.game-leader-details')[1].find_all('dd')
            
            self.reb = { 'away' : {'leader' : leader_tags[1].select('.long-name')[0].text,
                                   'reb' : int(away_reb_tags[0].select('.value')[0].text),
                                   'dreb' : int(away_reb_tags[1].select('.value')[0].text),
                                   'oreb' : int(away_reb_tags[2].select('.value')[0].text)} ,
                        'home' : {'leader' : leader_tags[1].select('.long-name')[1].text,
                                   'reb' : int(home_reb_tags[0].select('.value')[0].text),
                                   'dreb' : int(home_reb_tags[1].select('.value')[0].text),
                                   'oreb' : int(home_reb_tags[2].select('.value')[0].text)} }
        
            away_ast_tags = leader_tags[2].select('.game-leader-details')[0].find_all('dd')
            home_ast_tags = leader_tags[2].select('.game-leader-details')[1].find_all('dd')
            
            self.ast = { 'away' : {'leader' : leader_tags[2].select('.long-name')[0].text,
                                   'ast' : int(away_ast_tags[0].select('.value')[0].text),
                                   'to' : int(away_ast_tags[1].select('.value')[0].text),
                                   'min' : int(away_ast_tags[2].select('.value')[0].text)} ,
                        'home' : {'leader' : leader_tags[2].select('.long-name')[1].text,
                                   'ast' : int(home_ast_tags[0].select('.value')[0].text),
                                   'to' : int(home_ast_tags[1].select('.value')[0].text),
                                   'min' : int(home_ast_tags[2].select('.value')[0].text)} }


    def to_dict(self):
        return {'article' : [self.article],
                'headline' : [self.headline],
                'date' : [self.date],
                'summary' : [self.summary],
                'winner' : [self.winner], 
                'names' : [self.names], 
                'scores' : [self.scores],
                'quarters' : [self.quarters],
                'pts' : [self.pts], 
                'reb' : [self.reb],
                'ast' : [self.ast],}

# feedback for testing
if __name__ == '__main__':
    game_id = '400899380\n'
    
    game = Game(game_id)
    print('article: ', game.article)
    print('\n headline: ', game.headline)
    print('\n summary: ', game.summary)
    print('\n date: ', game.date)
    print('\n winning team: ', game.winner)
    print('\n team names: \n', game.names)
    print('\n number of quarters played: ', game.quarters)
    print('\n total and quarterly scores: \n', game.scores)
    print('\n points leaders stats: \n', game.pts)
    print('\n rebounding leaders stats: \n', game.reb)
    print('\n assist leaders stats: \n', game.ast)


            
            