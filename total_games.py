import pandas as pd
import requests
from bs4 import BeautifulSoup

website = 'https://www.esportsearnings.com/games'

new_url = 'https://www.esportsearnings.com'

response = requests.get(website)    


soup = BeautifulSoup(response.content, 'html.parser')

results = soup.find('table', {'class': 'detail_list_table'}).find('tbody').find_all('tr')

top_5_list =  soup.find_all('div', {'class' : 'detail_box_game'})

print(top_5_list)

game_href = results[0].find('td', {'class': 'format_cell detail_list_game_left'}).find('a')['href']

game_name = results[0].find('td', {'class': 'format_cell detail_list_game_left'}).text

print(game_name)

game_href_list = []
game_name_list = []
country_list = []
game_list = []
master_list = []
players_list = []
Prize_pool = []


def get_each_game(game, game_url):
    
    url = 'https://www.esportsearnings.com' + str(game_url) + '/countries'
    response = requests.get(url)    
    soup = BeautifulSoup(response.content, 'html.parser')
    geg_results = soup.find('table', {'class': 'detail_list_table'}).find('tbody').find_all('tr')

    print(geg_results[0].find_all('td', {'class': 'format_cell detail_list_prize'})[0].text)
    print(int((geg_results[0].find_all('td', {'class': 'format_cell detail_list_prize'})[1].text).split(' ')[0]))

    #sd = results[0].find('td', {'class': 'format_cell detail_list_player'}).find_all('a')[1].text
    print(url)
    for i in geg_results:
        country_list.append(i.find('td', {'class': 'format_cell detail_list_player'}).find_all('a')[1].text)
        players_list.append(int((i.find_all('td', {'class': 'format_cell detail_list_prize'})[1].text).split(' ')[0]))
        Prize_pool.append(i.find_all('td', {'class': 'format_cell detail_list_prize'})[0].text)
        game_list.append(game)

for i in top_5_list:
    game_href_list.append(i.find('div', {'class' : 'games_top_games_title'}).find('a')['href'])
    game_name_list.append(i.find('div', {'class' : 'games_top_games_title'}).find('a').text)

for i in results:
    game_href_list.append(i.find('td', {'class': 'format_cell detail_list_game_left'}).find('a')['href'])
    game_name_list.append(i.find('td', {'class': 'format_cell detail_list_game_left'}).text)


df = pd.DataFrame({'game_href': game_href_list, 'game_name' : game_name_list})

master_list = df.values.tolist()

print(master_list)

for i in master_list:
    get_each_game(i[1], i[0])



final_df = pd.DataFrame({'country': country_list, 'total_earnings': Prize_pool, 'players': players_list, 'game': game_list})

final_df.to_csv('total_games.csv', index=False)

