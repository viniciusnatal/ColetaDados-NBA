import pandas as pd
import time
import selenium
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

#
url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1"
top10ranking = {}

rankings = {
    'Cesta de 3 Pontos': {'field': 'FG3M', 'label': '3PM'},
    'Total de Pontos': {'field': 'PTS', 'label': 'PTS'},
    'Assistencias': {'field': 'AST', 'label': 'AST'},
    'Rebotes': {'field': 'REB', 'label': 'REB'},
    'Roubos de Bola': {'field': 'STL', 'label': 'STL'},
    'Bloqueios': {'field': 'BLK', 'label': 'BLK'},
}

def criarRank(type):
    field = rankings[type]['field']
    label = rankings[type]['label']
    time.sleep(4)
    driver.find_element_by_xpath(
        f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()
    element = driver.find_element_by_xpath(
        "//div[@class='nba-stat-table']//table")
    html_content = element.get_attribute('outerHTML')

    # Organizar conteudo HMTL
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # Estruturar conteudo em DataFrame
    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', label]]
    df.columns = ['Posicao', 'Jogador', 'Time', 'Pontos']

    # Conversão do dataFrame com dicionário proprio

    return df.to_dict('records')


#Ativar cookies
option = Options()
option.headless = True
driver = webdriver.Firefox(executable_path='D:/Certificados/webscraping_python_selenium-master/'
                                           'geckodriver-v0.27.0-win64/geckodriver.exe')
driver.get(url)
driver.implicitly_wait(20)

driver.find_element_by_id("onetrust-accept-btn-handler").click()
for k in rankings:
    top10ranking[k] = criarRank(k)
driver.quit()

#Converter/Salvar em arquivo Json
with open('ranking.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(top10ranking, indent=4)
    jp.write(js)






