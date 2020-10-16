import requests
from bs4 import BeautifulSoup
import csv

HOST = "https://www.nhl.com/"
URL = "https://www.nhl.com/info/teams"
save_path = "../dl-for-hockey/nhl-players-data/players-data/team_sites.csv"

params = ""
html = requests.get(URL, params=params).content

soup = BeautifulSoup(html, "html.parser")
items = soup.find_all("div", class_="ticket-team_name")

team_sites = []
for item in items[:-1]:
    team_sites.append(
        {
            "team": item.find("span", class_="team-name").get_text(strip=True),
            "website": item.find("a").get("href")
        }
    )

team_sites = sorted(team_sites, key=lambda x: x["team"])

with open(save_path, "w", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Team", "Website"])
    for team in team_sites:
        writer.writerow([team["team"], team["website"]])
