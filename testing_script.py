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
    exact_smaller_elements = [div for div in soup.find_all('div', class_='smaller') if not div.get('data-image-name')]
    print(exact_smaller_elements)
    span_tags = [span for span in exact_smaller_elements if 'dimensions' not in span.get('class', [])]
    extra_dims = []
    # Print the text content of the filtered <span> tags
    for span in span_tags:
        extra_dims.append(span.get_text(strip=True))
    return extra_dims

def main():
    html_content = fetch_html("https://www.lexington.com/aidan-upholstered-arm-chair")
    soup = parse_html(html_content)
    data  = extra_dimensions(soup)
    print(data)

if __name__ == "__main__":
    main()
