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

# Find Hrefs to category
find_cat_by_room = [room for room in soup.find_all('li', class_='level_4')]

# Hrefs to sub-category by room ( products inside it )
hrefs = [room.find('a')['href'] for room in find_cat_by_room if room.find('a')]
fixed_hrefs = [room for room in hrefs if not '=' in room]

# Create full links to sub-cat
full_links = [urljoin(url, sub_cat_url) for sub_cat_url in fixed_hrefs]

# For every single sub-cat get products urls to individual list
for sub_cat_link in full_links:
    # Send a request to fetch the HTML content
    response = requests.get(sub_cat_link)
    try:
        response.raise_for_status()  # Check for request errors
    except Exception as e:
        print(f'Failed to request: {e}')

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    find_products_selector = soup.find_all('div', class_='product-image')
    find_product_link = [product.find('a')['href'] for product in find_products_selector if product.find('a')]
    print(find_product_link)