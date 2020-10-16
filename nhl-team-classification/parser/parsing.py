import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import csv

save_path = "../dl-for-hockey/nhl-team-classification/parser/players_photos.csv"

df = pd.read_csv("/Users/alexeytopolnitskiy/Projects/dl-for-hockey/nhl-players-data/players-data/players_info.csv", sep=";")
players_sites = df.loc[:, "Webpage"]
players_photo_urls = []

for i in tqdm(range(len(players_sites))):

    url = players_sites[i]
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")

    player_photo_1 = soup.find("div", class_="player-jumbotron player-jumbotron--responsive")
    player_photo_2 = player_photo_1.find("div", class_="player-jumbotron-cover__image")
    player_photo = player_photo_2.get("data-img")
    players_photo_urls.append(player_photo)

with open(save_path, "w", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow([
        "Team",
        "Photo"
    ])
    for j in tqdm(range(len(players_photo_urls))):
        writer.writerow([
            df.loc[j, "Team"],
            players_photo_urls[j]
        ])
