from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests, os, re, unidecode, datetime
from dotenv import load_dotenv
from team import create_team
from match import create_match
from utils import get_soup
from variables import LA_LIGA_TEAMS_URL, ONE_FOOTBALL_URL, LA_LIGA_CALENDAR_URL

load_dotenv()
MATCHES_DB_ID = os.getenv("MATCHES_DB_ID")
LA_LIGA_PAGE_ID = os.getenv("LA_LIGA_PAGE_ID")




def get_la_liga_teams():
    team_links = []
    
    soup = get_soup(LA_LIGA_TEAMS_URL)
    teams = soup.find(attrs={"class": "styled__ClubesHeaderContainer-sc-1azasvg-0"})
    for team in teams.find_all(name="a"):
        team_link = team.attrs["href"]
        # print(team_link)
        team_links.append(team_link)
    teams = {}
    soup = get_soup(ONE_FOOTBALL_URL)

    for team_soup in soup.find_all(name="li", attrs={"class":"standings__row"}):
        # print(team.get_text().split())
        try:
            team_title = team_soup.find(name="a").attrs["aria-label"]
            pattern = unidecode.unidecode(team_title.lower()).split()
            pattern1 = r".*{}".format(pattern[-1])
            pattern2 = r".*{}".format("".join(pattern))
            pattern3 = r".*{}".format("-".join(pattern))
            pattern4 = r".*{}".format(pattern[0])
            for i,link in enumerate(team_links):
                if re.match(pattern1,link) and re.match(pattern2,link):
                    teams[team_title] = [link]
                    team_links.pop(i)
                elif re.match(pattern3,link):
                    teams[team_title] = [link]
                    team_links.pop(i)

            if not team_title in teams:
                teams[team_title] = [LA_LIGA_TEAMS_URL]   
        except:
            pass
    # print(teams)

    for team in list(teams.keys()):
        search_url = "https://en.wikipedia.org/wiki/football {}".format(team)
        soup = get_soup(search_url)
        link = soup.find(name="a", href=re.compile(r"^(https://en).*wikipedia.*(?<!edit)$")).attrs["href"]
        soup = get_soup(link)
        team_wiki_link = soup.find(attrs={"class":"mw-search-results-container"}).find(name="a").attrs["href"]
        team_wiki_link = "https://en.wikipedia.org"+team_wiki_link
        soup = get_soup(team_wiki_link)
        team_logo = "https:"+soup.find(attrs={"class":"image"}).find(name="img").attrs["src"]
        team_full_name = soup.find(name="h1").get_text()
        teams[team] += [team_logo, team_full_name]
    return teams




def create_la_liga_teams():
    teams = get_la_liga_teams()
    for team in teams:
        create_team(LA_LIGA_PAGE_ID,teams[team][0], teams[team][1], teams[team][2])

def create_la_liga_calendar():
    for i in range(1,39):
        soup = get_soup(LA_LIGA_CALENDAR_URL+str(i))

        matchday = "Matchday {}".format(i)
        for row in soup.find(name="table").find_all(name="tr"):
            data = []
            if len(row.find_all(name="td"))>1:
                for elem in row.find_all(name="td"):
                    if re.match(r"\w+",elem.get_text()):
                        data.append(elem.get_text())
                match_date = data[0].split(" ")[-1]
                match_date = datetime.datetime.strptime(match_date, "%d.%m.%Y")
                match_date = match_date.strftime("%Y-%m-%d")
                teams = data[1].split("VS")
                home_team = teams[0].strip()
                away_team = teams[1].strip()
                load_dotenv()
                home_team_key = os.getenv(unidecode.unidecode(home_team.replace(" ", "").lower()))
                away_team_key = os.getenv(unidecode.unidecode(away_team.replace(" ", "").lower()))

                create_match(LA_LIGA_PAGE_ID,matchday, home_team, home_team_key, away_team, away_team_key, match_date)
                print("Fetch {} : {} vs {}".format(matchday, home_team, away_team))


def gameday(week):
    pass

 