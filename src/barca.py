import os, re, unidecode, datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

from player import Player
from match import Match


BARCA_PLAYERS_URL = "https://www.fcbarcelona.com/en/football/first-team/players"
BARCA_CALENDAR_URL  ="https://www.fcbarcelona.com/en/football/first-team/schedule"


load_dotenv()
BARCA_PAGE_ID = os.getenv("BARCA_PAGE_ID")
LA_LIGA_PAGE_ID = os.getenv("LA_LIGA_PAGE_ID")


# class Barca
def get_soup(url: str) -> BeautifulSoup:
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html")
    return soup



def fetch_barca_players():
    soup = get_soup(BARCA_PLAYERS_URL)

    player_pos_tag = "player-hero__info-meta"
    player_name_tag = "player-hero__name"
    player_img_tag = "player-hero__img"
    player_data_tag = "player-strip__data"
    player_promo_tag = "content-promo__title"
    player_bio_tag = "player-bio__description"

    def find_player_info(soup, tag):
        return soup.find(attrs={"class":tag}).get_text()

    def find_player_img(soup, tag):
        return soup.find(attrs={"class":tag}).attrs["src"]

    def find_player_data(soup, player_data_tag):
        data = [tag.get_text() for tag in soup.find_all(attrs={"class":player_data_tag})]
        return data

    def find_player_honours(soup):
        player_honour_data = []
        for elem in soup.find_all(attrs={"class":"player-honour"}):
            player_honour_title = elem.find(attrs={"class": "player-honour__title"}).get_text()
            player_honour_dates = elem.find(attrs={"class": "player-honour__dates"}).get_text().split()
            player_honour_dates = [dates for dates in player_honour_dates if len(dates)>1]
            player_honour_title_total = len(player_honour_dates)
            player_honour_dates = " | ".join(player_honour_dates)
            player_honour_data_meta = "{} {}🏆 → {}".format(player_honour_title, player_honour_title_total, player_honour_dates)
            player_honour_data.append(player_honour_data_meta)
        return player_honour_data

    for link in soup.find_all(href=re.compile(r"https.*first-team")):
        try:
            player_soup = get_soup(link.attrs["href"])
            player_soup = player_soup.find(attrs={"class":"teams-page"})
            
            player_data = {}
            
            player_name = find_player_info(player_soup,player_name_tag)
            player_name = re.sub("\n | \s+", " ", player_name).split()
            player_num = int(player_name[0])
            player_name = " ".join(player_name[1:])
            player_pos = find_player_info(player_soup, player_pos_tag)
            player_img = find_player_img(player_soup, player_img_tag)
            player_promo = find_player_info(player_soup, player_promo_tag)
            player_bio = find_player_data(player_soup, player_bio_tag)
            player_bio = " ".join(player_bio)
            
            player_data = find_player_data(player_soup, player_data_tag)
            player_national_team = player_age = player_weight = player_height = ""

            for elem in player_data:
                if re.match(r"\D", elem):
                    player_national_team = elem.split(", ")[-1]
                else:
                    if re.match(r"\d+/", elem) and int(elem.split("/")[-1])<2008:
                        player_age = 2023-int(elem.split("/")[-1])
                    elif re.match(".*kg",elem):
                        player_weight = int(re.sub("kg","", elem))
                    elif re.match(".*cm",elem):
                        player_height = int(re.sub("cm","", elem))
            player_honours = find_player_honours(player_soup)
            # print(player_name, player_national_team, player_age, player_pos, player_weight, player_height, player_num, player_img, player_honour_data)
            create_player(BARCA_PAGE_ID,player_name, player_national_team, player_age, player_pos, player_weight, player_height, player_num, player_img, player_promo, player_bio, player_honours)
            print("Fetch {}".format(player_name))
        except:
            print("Data retrieval failed.")
            

def create_barca_calendar():
    
    load_dotenv()

    soup = get_soup(BARCA_CALENDAR_URL)
    soup = soup.find(attrs={"class":"body-content"})
    for link in soup.find_all(name="a", attrs={"class":"fixture-result-list__link"}):
        match_link = "https://www.fcbarcelona.com" + link.attrs["href"]
        # print(match_link)
        match_soup = get_soup(match_link)
        home_team = match_soup.find(attrs={"class":"fixture-info__name--home"}).get_text()
        away_team = match_soup.find(attrs={"class":"fixture-info__name--away"}).get_text()
        matchday = match_soup.find(attrs={"class":"match-details__value"}).get_text()
        match_date = match_soup.find(attrs={"class":"match-hero__date"}).get_text()
        # match_date += " 2023"
        match_date_time = datetime.datetime.strptime(match_date, "%a %d %b")
        if match_date_time.month in range(8,13):
            match_date += " 2023"
        else:
            match_date += " 2024"
        match_date = datetime.datetime.strptime(match_date, "%a %d %b %Y")
        match_date = match_date.strftime("%Y-%m-%d")
        
        home_team_key = os.getenv(unidecode.unidecode(home_team.replace(" ", "").replace(".","").lower()))
        away_team_key = os.getenv(unidecode.unidecode(away_team.replace(" ", "").replace(".","").lower()))
        create_match(LA_LIGA_PAGE_ID,matchday, home_team, home_team_key, away_team, away_team_key, match_date)
        print("Fetch {} : {} vs {}".format(matchday, home_team, away_team))