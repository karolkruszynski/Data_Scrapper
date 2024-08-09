import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

# Base URL
url = 'https://www.lexington.com/'

# Send a request to fetch the HTML content
response = requests.get(url)
try:
    response.raise_for_status()  # Check for request errors
except Exception as e:
    print(f'Failed to request: {e}')

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

find_cat_by_room = [room for room in soup.find_all('li', class_='level_4')]

hrefs = [room.find('a')['href'] for room in find_cat_by_room if room.find('a')]

