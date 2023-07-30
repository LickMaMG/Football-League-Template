from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests, os, re, unidecode, datetime
from dotenv import load_dotenv
from team import Team
from match import Match
from league import League


class LaLiga:
    def __init__(self) -> None:
        self.NOTION_ENDPOINT = "https://api.notion.com/v1/"
        self.LA_LIGA_CALENDAR_URL = "https://www.laliga.com/en-GB/laliga-santander/results/2023-24/gameweek-"
        self.LA_LIGA_TEAMS_URL = "https://www.laliga.com/en-GB/laliga-santander"
        self.ONE_FOOTBALL_URL = "https://onefootball.com/en/competition/laliga-10/table"
        
        self.load_env()
        self.load_headers()
        
        # self.create_teams()
        # self.create_calendar()
        
    def load_headers(self) -> None:
        self.headers = {
            "accept": "application/json",
            "Notion-Version": "2022-06-28",
            "content-type": "application/json",
            "Authorization": "Bearer " + self.NOTION_API_KEY 
        }
    
    def load_env(self) -> None:
        load_dotenv()
        self.NOTION_API_KEY = os.getenv("NOTION_API_KEY")
        self.LA_LIGA_PAGE_ID = os.getenv("LA_LIGA_PAGE_ID")
        self.NOTION_API_KEY = os.getenv("NOTION_API_KEY")

    def get_soup(self, url: str) -> BeautifulSoup:
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html")
        return soup
    
    
    def get_teams(self) -> dict[str, list[str]]:
        team_links = []
        
        soup = self.get_soup(self.LA_LIGA_TEAMS_URL)
        teams = soup.find(attrs={"class": "styled__ClubesHeaderContainer-sc-1azasvg-0"})
        for team in teams.find_all(name="a"):
            team_link = team.attrs["href"]
            # print(team_link)
            team_links.append(team_link)
        teams = {}
        soup = self.get_soup(self.ONE_FOOTBALL_URL)

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
                    teams[team_title] = [self.LA_LIGA_TEAMS_URL]   
            except:
                pass

        for team in list(teams.keys()):
            search_url = "https://en.wikipedia.org/wiki/football {}".format(team)
            soup = self.get_soup(search_url)
            link = soup.find(name="a", href=re.compile(r"^(https://en).*wikipedia.*(?<!edit)$")).attrs["href"]
            soup = self.get_soup(link)
            team_wiki_link = soup.find(attrs={"class":"mw-search-results-container"}).find(name="a").attrs["href"]
            team_wiki_link = "https://en.wikipedia.org"+team_wiki_link
            soup = self.get_soup(team_wiki_link)
            team_logo = "https:"+soup.find(attrs={"class":"image"}).find(name="img").attrs["src"]
            team_full_name = soup.find(name="h1").get_text()
            teams[team] += [team_logo, team_full_name]
        return teams

    def create_teams(self) -> None:
        teams = self.get_teams()
        for team in teams:
            Team(
                league_db_id   = self.LA_LIGA_PAGE_ID,
                team_url       = teams[team][0],
                team_logo      = teams[team][1],
                team_full_name = teams[team][2]
            )

    def create_calendar(self) -> None:
        for week in range(1,39):
            self.create_gameweek(week=week)
    
    def create_gameweek(self, week: int) -> None:
        url = self.LA_LIGA_CALENDAR_URL+str(week)
        soup = self.get_soup(url)

        matchday = "Matchday {}".format(week)
        for row in soup.find(name="table").find(name="tbody").find_all(name="tr")[::3]:
            data = []
            for elem in row.find_all(name="td"):
                if re.match(r"\w+",elem.get_text()):
                    data.append(elem.get_text())
            match_date = data[1].split(" ")[-1]
            match_date = datetime.datetime.strptime(match_date, "%d.%m.%Y")
            if len(data)==4:         
                match_time = data[2].split(":")
                match_date=match_date.replace(hour=int(match_time[0]), minute=int(match_time[1]))
                match_date = match_date.strftime("%Y-%m-%d %H:%M")
            else: match_date = match_date.strftime("%Y-%m-%d %H:%M")
            teams = data[-1].split("VS")
            home_team = teams[0].strip()
            away_team = teams[1].strip()
            
            Match(
                league_db_id  = self.LA_LIGA_PAGE_ID,
                matchday      = matchday,
                match_date    = match_date,
                home_team     = home_team,
                away_team     = away_team
            )
            
            # print("Fetch {} : {} vs {}".format(matchday, home_team, away_team))
        
        def set_gameweek_time(self):
            pass
    



def update_gameday(week):
    pass

 