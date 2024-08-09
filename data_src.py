import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def main():
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

    # Dict to store multi-cat with their list of links to products
    products_dict = {}
    i = 0

    # For every single sub-cat get products urls to individual list
    for sub_cat_link in full_links:
        # Get name of category for key name in dict
        item = fixed_hrefs[i]
        item = item.replace('/', '')
        # Send a request to fetch the HTML content
        response = requests.get(sub_cat_link)
        try:
            response.raise_for_status()  # Check for request errors
        except Exception as e:
            print(f'Failed to request: {e}')
            continue # If error exist

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        find_products_selector = soup.find_all('div', class_='product-image')
        find_product_link = [product.find('a')['href'] for product in find_products_selector if product.find('a')]
        #print(find_product_link)

        # Adding a list of links to the dictionary under the appropriate key
        products_dict[item] = find_product_link

        # List of links for a given sub_cat_link
        #print(f"Links for {item}: {find_product_link}")
        i += 1

    return products_dict  # Return Data

    # Run def
if __name__ == "__main__":
    final_products_dict = main()
    print(final_products_dict)