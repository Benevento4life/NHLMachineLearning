
'''
Programmet använder en webdriver för att hämta texten från 87 olika flikar av hemsidan oddsportal.com.
Oddsen till matcher i NHL mellan 2014 och 2017 extraheras sedan från denna text, och oddsen paras ihop med datum och lag med samma system som i datasetet från Kaggle.
Programmet skapar till sist en .csv-fil bestående av datasetet där oddsen lagts till.
Programmet tar inte input. Användaren bes istället att skriva in sitt önskade namn på .csv-filen på rad 185.
'''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Avkodningar av månader och lag till rätt format

teams = {"New York Rangers": "0", "Pittsburgh Penguins": "1", "Edmonton Oilers": "2", "Winnipeg Jets": "3", "Philadelphia Flyers": "4", "Dallas Stars": "5", "New Jersey Devils": "6", "Tampa Bay Lightning": "7", "Minnesota Wild": "8", "Colorado Avalanche": "9", "Anaheim Ducks": "10", "Toronto Maple Leafs": "11", "New York Islanders": "12", "Montreal Canadiens": "13", "St. Louis Blues": "14", "Florida Panthers": "15", "Buffalo Sabres": "16", "Arizona Coyotes": "17", "Ottawa Senators": "18", "Washington Capitals": "19", "Columbus Blue Jackets": "20", "Chicago Blackhawks": "21", "Nashville Predators": "22", "Calgary Flames": "23", "Boston Bruins": "24", "Detroit Red Wings": "25", "Vancouver Canucks": "26", "Carolina Hurricanes": "27", "San Jose Sharks": "28", "Los Angeles Kings": "29"}

months = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}

# Initialisering av listorna där bland annat oddsen ska lagras

home_odds_list = []
draw_odds_list = []
away_odds_list = []
away_team_list = []
date_list = []
counter = 0

# Baslänkarna till hemsidorna som används

basicurls = ["https://www.oddsportal.com/hockey/usa/nhl-2014-2015/results/#/page/", "https://www.oddsportal.com/hockey/usa/nhl-2015-2016/results/#/page/", "https://www.oddsportal.com/hockey/usa/nhl-2016-2017/results/#/page/"]

# Loopar igenom alla länkar till hemsidor

for url in basicurls:
    for i in range(1, 30):
        val = url + str(i) + '/'

        # Kör drivern

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        driver.get(val)

        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        page_source = driver.page_source

        driver.quit()

        # Sparar källkoden, och tar fram all text i en viss sorts div

        soup = BeautifulSoup(page_source, 'html.parser')

        all_divs = soup.find_all('div', class_='eventRow')
        for div in all_divs:
            text = list(div.text)

            # Hanteringen av texten är väldigt specifikt gjord för att extrahera oddsen från just den här sortens format.
            # Oddsen läggs slutligen till i korresponderande lista och datum samt bortalag sparas också för ihopparning

            text.pop()
            if text[-2] == '-':
                counter += 1
                continue
            odds_loss = round((int(text[-4])+0.1*int(text[-2])+0.01*int(text[-1])),2)
            for _ in range(4):
                text.pop()
            odds_draw = round((int(text[-4])+0.1*int(text[-2])+0.01*int(text[-1])),2)
            for _ in range(4):
                text.pop()
            odds_win = round((int(text[-4])+0.1*int(text[-2])+0.01*int(text[-1])),2)
            for _ in range(4):
                text.pop()
            if text[-1] == 'T':
                for _ in range(3):
                    text.pop()
            elif text[-1] == '.':
                for _ in range(5):
                    text.pop()
            text.pop()
            i = -1
            while text[i] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                i += -1
            i += 1
            away_team = []
            while i < 0:
                away_team.append(text[i])
                i += 1
            try:
                away_team = teams["".join(away_team)]
            except KeyError:
                continue
            if text[2] == ':':
                starttime = text[0]
            else:
                if text[0] == 'H':
                    for _ in range(24):
                        text.pop(0)
                words = ("".join(text)).split()
                curr_date = words[2]+months[words[1]]+words[0]
                if words[3] == '-':
                    continue
                else:
                    starttime = list(words[3])[6]
            date = curr_date
            if starttime == '0':
                list_date = list(date)
                if int(list_date[7]) > 1 or ((list_date[7] == '1') and (list_date[6] != '0')):
                    list_date[7] = str(int(list_date[7])-1)
                elif int(list_date[6]) > 0:
                    list_date[7] = '9'
                    list_date[6] = str(int(list_date[6])-1)
                else:
                    if list_date[4] == '1' and list_date[5] == '2':
                        list_date[5] = '1'
                        list_date[7] = '0'
                        list_date[6] = '3'
                    elif list_date[4] == '1' and list_date[5] == '1':
                        list_date[5] = '0'
                        list_date[7] = '1'
                        list_date[6] = '3'
                    elif list_date[4] == '1' and list_date[5] == '0':
                        list_date[5] = '9'
                        list_date[4] = '0'
                        list_date[7] = '0'
                        list_date[6] = '3'
                    elif list_date[4] == '0' and list_date[5] == '9':
                        list_date[5] = '8'
                        list_date[7] = '1'
                        list_date[6] = '3'
                    elif list_date[4] == '0' and list_date[5] == '8':
                        list_date[5] = '7'
                        list_date[7] = '1'
                        list_date[6] = '3'
                    elif list_date[4] == '0' and list_date[5] == '7':
                        list_date[5] = '6'
                        list_date[7] = '0'
                        list_date[6] = '3'
                    elif list_date[4] == '0' and list_date[5] == '6':
                        list_date[5] = '5'
                        list_date[7] = '1'
                        list_date[6] = '3'
                    elif list_date[4] == '0' and list_date[5] == '5':
                        list_date[5] = '4'
                        list_date[7] = '0'
                        list_date[6] = '3'
                    elif list_date[4] == '0' and list_date[5] == '4':
                        list_date[5] = '3'
                        list_date[7] = '1'
                        list_date[6] = '3'
                    elif list_date[4] == '0' and list_date[5] == '3':
                        list_date[5] = '2'
                        if list_date[3] == '6':
                            list_date[7] = '9'
                        else:
                            list_date[7] = '8'
                        list_date[6] = '2'
                    elif list_date[4] == '0' and list_date[5] == '2':
                        list_date[4] = '1'
                        list_date[7] = '1'
                        list_date[6] = '3'
                    else:
                        list_date[5] = '2'
                        list_date[4] = '1'
                        list_date[7] = '1'
                        list_date[6] = '3'
                        list_date[3] = str(int(list_date[3])-1)
                date = "".join(list_date)
            home_odds_list.append(odds_win)
            draw_odds_list.append(odds_draw)
            away_odds_list.append(odds_loss)
            away_team_list.append(away_team)
            date_list.append(date)

# Oddsen organiseras i ett kalkylark som sparas

toprow = {"Date": date_list, "Away Team": away_team_list, "Home Odds": home_odds_list, "Draw Odds": draw_odds_list, "Away Odds": away_odds_list}

df = pd.DataFrame(toprow, index=None)
df.to_csv('exampleOdds.csv', index=False) # Byt ut filnamnet om du så önskar

print('Program finished as expected.')
