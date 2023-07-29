import requests, os
from auth import load_headers
from dotenv import load_dotenv
from variables import NOTION_ENDPOINT

load_headers()
TEAMS_DB_ID = os.getenv("TEAMS_DB_ID")

def create_team(league_db_id, team_url, team_logo, team_full_name):
    
    payload = {
        "parent": {
            "type": "database_id",
            "database_id": TEAMS_DB_ID
        },
        
        "icon": {
            "type": "external",
            "external": {"url": team_logo}
        },
        
        "cover": {
            "type": "external",
            "external": {"url": team_logo}
        },
        
        "properties": {
            "Name": {
                "title": [{
                    "text": {"content": team_full_name}
                }]
            },
            "Team URL": {"url": team_url},
            "League": {
                "relation": [{"id": league_db_id}]
            }
        }
    }
    response = requests.post(NOTION_ENDPOINT+"pages/", headers=load_headers(), json=payload)
    response.raise_for_status()