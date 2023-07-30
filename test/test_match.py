import sys
sys.path.append("./src")

import os
from dotenv import load_dotenv

from match import Match

if __name__ == "__main__":
    load_dotenv()
    LA_LIGA_PAGE_ID = os.getenv("LA_LIGA_PAGE_ID")

if __name__ == "__main__":
    Match(
       league_db_id  = LA_LIGA_PAGE_ID,
       matchday      = "Friendly Match",
       match_date    = "2023-07-29 23:00",
       home_team     = "FC Barcelona",
       away_team     = "Real Madrid",
       POST          = False 
   )