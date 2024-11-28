import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import os



def insert_data_to_db(table_name, data):
    conn = sqlite3.connect('vikings.db')
    cursor = conn.cursor()

    if table_name == 'vikings_cast':
        for character in data:
            cursor.execute('''
            INSERT INTO vikings_cast (name, description, photo_url)
            VALUES (?, ?, ?)
            ''', (character['name'], character['description'], character['photo_url']))
    
    elif table_name == 'norsemen_characters':
        for character in data:
            cursor.execute('''
            INSERT INTO norsemen_characters (name, actor, description, photo_url)
            VALUES (?, ?, ?, ?)
            ''', (character['name'], character['actor'], character['description'], character['photo_url']))
    
    elif table_name == 'vikings_nfl_roster':
        for player in data:
            cursor.execute('''
            INSERT INTO vikings_nfl_roster (name, position, photo_url)
            VALUES (?, ?, ?)
            ''', (player['name'], player['position'], player['photo_url']))
    
    conn.commit()
    conn.close()

def scrape_vikings_cast():
    url = "https://www.history.com/shows/vikings/cast"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    characters = []
    
    # Find all character sections on the page (li elements with class 'm-card')
    cast_elements = soup.find_all('li')

    for cast in cast_elements:
        # Extract character name, description, and photo
        name_tag = cast.find('strong')
        description_tag = cast.find('small')
        image_tag = cast.find('img')
        
        if not name_tag:
            continue

        name = name_tag.text.strip() if name_tag else 'Unknown'
        description = description_tag.text.strip() if description_tag else 'No description available'
        photo_url = image_tag['src'] if image_tag else 'No image'

        characters.append({
            'name': name,
            'description': description,
            'photo_url': photo_url
        })
    
    return characters

# Example usage
vikings_cast = scrape_vikings_cast()
#print(vikings_cast)










def scrape_norsemen_characters():
    url = "https://www.imdb.com/title/tt5905354/fullcredits/?ref_=tt_cst_sm"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    characters = []
    cast_table = soup.find_all('table', class_='cast_list')
    
    for table in cast_table:      
        rows = table.find_all('tr')
        
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 3:
                character_details = cols[3].find_all('a')
                name = character_details[0].text.strip()
                description = character_details[1].text.strip()
                
                actor = cols[1].text.strip()
                # description = cols[2].text.strip() if len(cols) > 2 else 'No description available.'
                photo_url = cols[0].find('img')
                if photo_url.has_attr('loadlate'):
                    photo_url = photo_url['loadlate']
                else:
                    photo_url = photo_url['src']
                
                characters.append({
                    'name': name,
                    'actor': actor,
                    'description': description,
                    'photo_url': photo_url
                })
    
    return characters


norsemen_characters = scrape_norsemen_characters()
print(norsemen_characters)



#insert_data_to_db('vikings_cast', vikings_cast)
#insert_data_to_db('norsemen_characters', norsemen_characters)
#insert_data_to_db('vikings_nfl_roster', vikings_nfl_players)