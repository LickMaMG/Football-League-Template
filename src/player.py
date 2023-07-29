from dotenv import load_dotenv
import os, requests
from auth import load_headers
from variables import NOTION_ENDPOINT

load_dotenv()
PLAYERS_DB_ID = os.getenv("PLAYERS_DB_ID")


def create_player(team_page_id, player_name, player_national_team, player_age, player_pos, player_weight, player_height, player_num, player_img, player_promo, player_bio, player_honours):
    payload = {
        "parent": {
            "type": "database_id",
            "database_id": PLAYERS_DB_ID
        },
        
        "icon": {
            "type": "external",
            "external": {"url": player_img}
        },
        
        "cover": {
            "type": "external",
            "external": {"url": player_img}
        },
        
        "properties": {
            "Name": {
                "title": [{
                    "text": {"content": player_name}
                }]
            },
            "Club": {
                "relation": [{
                    "id": team_page_id
                }]
            },
            "National Team": {
                "rich_text": [{
                    "text": {"content": player_national_team}
                }]
            },
            "Age": {"number": player_age},
            "Position": {
                "select": {"name": player_pos}
            },
            "Weight": {"number": player_weight},
            "Height": {"number": player_height},
            "Jersey Number": {"number": player_num},
        },
        
        "children": [
            {
                "object":"block",
                "type": "heading_1",
                "heading_1" : {"rich_text": [{"text": {"content": player_promo}}]}
            },
            
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            }
            
            ] + [
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"text": {"content": honour}}]}
            }
        
        for honour in player_honours]
    }
    
    response = requests.post(url=NOTION_ENDPOINT+"pages/",headers=load_headers(), json=payload)
    response.raise_for_status()