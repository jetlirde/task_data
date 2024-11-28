import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Vikings stats page
url = "https://www.vikings.com/team/stats/2021/REG"

# Send a request to fetch the HTML content of the page
response = requests.get(url)
response.raise_for_status()  # Raise an exception if the request fails

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table element with the class name 'd3-o-table' (adjust based on inspection)
table = soup.find('table', {'class': 'd3-o-table'})

# Ensure the table was found
if table is None:
    print("Table not found.")
else:
    print("Table found!")

# Extract headers (columns) from the table
headers = []
for th in table.find_all('th'):
    headers.append(th.get_text(strip=True))

# Extract rows (player stats) from the table
rows = []
player_links = []
for tr in table.find_all('tr')[1:]:  # Skip the header row
    cols = tr.find_all('td')
    row = [col.get_text(strip=True) for col in cols]
    if row:
        rows.append(row)
        player_name = tr.find('a')
        if player_name:
            # Make sure the link is to a specific player's profile
            link = player_name.get('href', '')
            if link and link.startswith('/team/players-roster/'):
                player_links.append('https://www.vikings.com' + link)

# Check if headers and rows are correctly populated
if not headers or not rows:
    print("No valid data found.")
else:
    # Create a DataFrame using pandas
    df = pd.DataFrame(rows, columns=headers)
    print("Player Statistics Data:")
    print(df)

    # Optionally, save the data to a CSV file
    df.to_csv('vikings_2021_player_stats.csv', index=False)

# Scrape player profile images, biographies, and stats (if available)
players = []
for link in player_links:
    player_data = {}
    player_data['profile_url'] = link
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract player name (as a backup check)
    player_name = soup.find('h1')
    if player_name:
        player_data['name'] = player_name.get_text(strip=True)

    # Extract biography (if available)
    biography = soup.find('div', {'class': 'bio-text'})  # Adjust according to actual class or structure
    if biography:
        player_data['biography'] = biography.get_text(strip=True)

    # Extract player photo (image URL)
    player_photo = soup.find('img', {'class': 'player-photo'})  # Adjust according to the actual image class or ID
    if player_photo:
        player_data['photo_url'] = player_photo.get('src', '')

    # Collect the player data if it exists
    if player_data:
        players.append(player_data)

# Optionally save player profiles and photos
if players:
    players_df = pd.DataFrame(players)
    print("Player Profile Data:")
    print(players_df)

    # Save to CSV
    players_df.to_csv('vikings_pla  yer_profiles.csv', index=False)
