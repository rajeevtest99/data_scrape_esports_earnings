import pandas as pd
import requests
from bs4 import BeautifulSoup



new_url = 'https://www.esportsearnings.com/history/'
year_list = []
country = []
players = []
prize_pool = []


i = 1997

def scrape(url, year):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find('table', {'class': 'detail_list_table'}).find('tbody').find_all('tr')

    tt = results[0].find('td',{'class': 'format_cell detail_list_player'}).find_all('a')[1].text

    for i in results:
        year_list.append(year)
        country.append(i.find('td',{'class': 'format_cell detail_list_player'}).find_all('a')[1].text)
        players.append(int((results[0].find_all('td',{'class': 'format_cell detail_list_prize'})[1].text).split(' ')[0]))
        prize_pool.append(i.find_all('td',{'class': 'format_cell detail_list_prize'})[0].text)

    
    print(tt)
    print(results[0].find_all('td',{'class': 'format_cell detail_list_prize'})[0].text)
    print((results[0].find_all('td',{'class': 'format_cell detail_list_prize'})[1].text).split(' ')[0])
    print(year)

while i<2022:
    i = i+1
    url = new_url + str(i) + '/countries'
    year_no = i
    print(url)
    scrape(url, year_no)
    


df = pd.DataFrame({'year': year_list, 'country': country, 'players': players, 'prize_pool': prize_pool})

print(df)

df.to_csv('year_wise_country.csv', index= False)