import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd 
from tqdm import tqdm

HOST = "https://www.nhl.com"
save_path = "../dl-for-hockey/nhl-players-data/players-data/players_info.csv"

df = pd.read_csv("../dl-for-hockey/nhl-players-data/players-data/team_sites.csv", sep=";")
num_rows, num_cols = df.shape
players_info = []

for team_num in tqdm(range(num_rows)):

    team = df.loc[team_num, "Team"]
    url = df.loc[team_num, "Website"] + "/roster"
    html = requests.get(url).content

    soup = BeautifulSoup(html, "html.parser")
    players_table = soup.find("div", class_="card")
    positions = players_table.find_all("tr", class_="split-table-tr")

    for position in positions:

        players_names = position.find_all("td", class_="name-col")

        numbers = position.find_all("td", class_="number-col")
        pos = position.find_all("td", class_="position-col")
        shoots = position.find_all("td", class_="shoots-col")
        height = position.find_all("td", class_="height-col")
        weight = position.find_all("td", class_="weight-col")
        bd = position.find_all("td", class_="birthdate-col")
        hometown = position.find_all("td", class_="hometown-col")

        for i, player in enumerate(players_names):

            players_info.append(
                {
                    "FirstName": player.find("span", class_="name-col__item name-col__firstName").get_text(strip=True),
                    "LastName": player.find("span", class_="name-col__item name-col__lastName").get_text(strip=True),
                    "Team": team,
                    "Webpage": HOST + player.find("a").get("href"),
                    "Img": player.find("img", class_="player-photo").get("src"),
                    "Number": numbers[i].get_text(),
                    "Position": pos[i].get_text(),
                    "Shoots": shoots[i].get_text(),
                    "Height": height[i].find("span", class_="xs-sm-md-only").get_text(),
                    "Weight": weight[i].get_text(),
                    "Birthdate": bd[i].find("span", class_="xs-sm-md-only").get_text(),
                    "Hometown": hometown[i].get_text()
                }
            )
    
with open(save_path, "w", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow([
        "FirstName",
        "LastName",
        "Team",
        "Webpage",
        "Img",
        "Number",
        "Position",
        "Shoots",
        "Height",
        "Weight",
        "Birthdate",
        "Hometown"
    ])
    for player in players_info:
        writer.writerow([
            player["FirstName"],
            player["LastName"],
            player["Team"],
            player["Webpage"],
            player["Img"],
            player["Number"],
            player["Position"],
            player["Shoots"],
            player["Height"],
            player["Weight"],
            player["Birthdate"],
            player["Hometown"]
        ])
