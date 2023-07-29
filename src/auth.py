from dotenv import load_dotenv
import os, requests

def load_headers():
    load_dotenv()
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
        "Authorization": "Bearer " + NOTION_API_KEY 
    }
    return headers