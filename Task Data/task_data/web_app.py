import streamlit as st
import sqlite3

# Database connection
def get_data(query, params=()):
    conn = sqlite3.connect('vikings.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

# Display table of characters
st.title("Viking Characters")
search_query = st.text_input("Search characters:")

# Fetch characters based on search query
if search_query:
    query = "SELECT * FROM characters WHERE name LIKE ? OR description LIKE ?"
    characters = get_data(query, (f'%{search_query}%', f'%{search_query}%'))
else:
    characters = get_data("SELECT * FROM characters")

# Display table
for character in characters:
    st.subheader(character[1])  # Name
    st.image(character[4], width=150)  # Photo
    st.write(character[2])  # Description
    st.write(f"Played by: {character[3]}")  # Actor

# Detailed view for a single character
character_names = [char[1] for char in characters]
selected_character = st.selectbox("View details for:", character_names)

if selected_character:
    character_details = get_data("SELECT * FROM characters WHERE name=?", (selected_character,))
    if character_details:
        char = character_details[0]
        st.image(char[4], width=300)
        st.write(f"Name: {char[1]}")
        st.write(f"Description: {char[2]}")
        st.write(f"Actor: {char[3]}")
