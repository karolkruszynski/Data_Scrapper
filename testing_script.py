import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def fetch_html(url):
    """Fetches and returns the HTML content from the given URL."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()  # Check for request errors
    return response.text

def parse_html(html_content):
    """Parses the HTML content using BeautifulSoup."""
    return BeautifulSoup(html_content, 'html.parser')

def extract_sizes_and_dimensions(soup):
    """Extracts sizes and dimensions from h3 tags with the class 'showPrint'."""
    sizes = soup.find_all('h3', class_='showPrint')
    filtered_sizes = [h3 for h3 in sizes if 'first' not in h3.get('class', [])]
    size_info = []
    for h3 in filtered_sizes:
        size_text = h3.contents[0].strip()
        strong_tags = h3.find_all('strong')
        if len(strong_tags) >= 2:
            SKU = strong_tags[0].get_text(strip=True).replace('Item: ', '')
            DIMS = strong_tags[1].get_text(strip=True).replace('Dimensions: ', '')
            size_info.append((size_text, SKU, DIMS))
    return size_info

def main():
    html_content = fetch_html("https://www.lexington.com/arlington-platform-bed")
    soup = parse_html(html_content)
    data  = extract_sizes_and_dimensions(soup)
    print(data)

if __name__ == "__main__":
    main()
