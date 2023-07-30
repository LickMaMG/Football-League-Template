from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests, os, re, unidecode, datetime
from dotenv import load_dotenv
from team import Team
from match import Match


class League:
    
    def __init__(self, name) -> None:
        # self.name = name
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
        pass
    
    
    def create_teams(self) -> None:
        pass
    
    def create_calendar(self) -> None:
        pass
    
    def create_gameweek(self, week: int) -> None:
        pass
    
    def set_gameweek_time(self):
        pass
    
