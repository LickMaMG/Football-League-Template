from urllib.request import urlopen
import requests, os
from dotenv import load_dotenv
from auth import load_headers

from variables import NOTION_ENDPOINT

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
MATCHES_DB_ID = os.getenv("MATCHES_DB_ID")

def create_match(league_id, matchday, home_team, home_team_key, away_team, away_team_key, match_date):
    payload = {
        "parent": {
            "type": "database_id",
            "database_id": MATCHES_DB_ID
        },
        
        "properties": {
            "Name": {
                "title": [{
                    "text": {"content": "{} : {} vs {}".format(matchday, home_team, away_team)}
                }]
            },
            "Home Team": {"relation": [{"id": home_team_key}]},
            "Away Team": {"relation": [{"id": away_team_key}]},
            "Date": {"date": {"start": match_date}},
            "League": {"relation": [{"id": league_id}]}
        },
        "children": [
            {
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": "Your impressions on the match !!!"}
                    }]
                }
            }
        ]
    }
    response = requests.post(NOTION_ENDPOINT+"pages/", headers=load_headers(), json=payload)
    response.raise_for_status()