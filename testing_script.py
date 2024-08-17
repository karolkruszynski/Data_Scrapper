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

def extra_dimensions(soup):
    """Extracts additional dimensions information like Arm Depth etc."""
    # Find all <span> tags, excluding those with class 'dimensions'
    exact_smaller_elements = [div for div in soup.find_all('div', class_='smaller')]
    # Znajdź wszystkie <strong> i <span> wewnątrz tych <div> - Flat List
    strong_tags = [strong for div in exact_smaller_elements for strong in div.find_all('strong')]
    span_tags = [span for div in exact_smaller_elements for span in div.find_all('span')]
    full_data = {}
    for key, value in zip(strong_tags, span_tags):
        strip_key = key.get_text(strip=True)
        full_data[strip_key] = value.get_text(strip=True)
    return full_data

def main():
    html_content = fetch_html("https://www.lexington.com/aidan-upholstered-arm-chair")
    soup = parse_html(html_content)
    data  = extra_dimensions(soup)
    print(data)

if __name__ == "__main__":
    main()
