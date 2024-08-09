import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from data_src import main

# Get products data
product_links = main()

for prod in product_links['https://www.lexington.com/beds']:
    print(prod)

# Replace with the URL of the website you want to scrape
url = 'https://www.lexington.com/ashbourne-panel-bed'
base_url = 'https://www.lexington.com'

# Directory to save downloaded images
download_dir = 'downloaded_images'
os.makedirs(download_dir, exist_ok=True)

# Send a request to fetch the HTML content
response = requests.get(url)
try:
    response.raise_for_status()  # Check for request errors
except Exception as e:
    print(f'Failed to request: {e}')

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all img tags without alt attrs
img_tags = [img for img in soup.find_all('img') if not img.get('alt')]

# Extract the 'src' attribute from each image tag
img_urls = [urljoin(base_url, img['src']) for img in img_tags if 'src' in img.attrs]

# Extract Dimensions
dims = soup.find('span', class_='dimensions').get_text()
print(dims)

# Extract Stock Availability
stock = soup.find('span', class_='avail').get_text()
print(stock)

# Extract SKU
sku = soup.find('span', class_='sku').get_text()
print(sku)

# Extract Extra Option
sizes = soup.find_all('h3', class_=r'showPrint')
# Filtered to remove "first" selector
filtered_sizes = [h3 for h3 in sizes if 'first' not in h3.get('class', [])]
for size in filtered_sizes:
    size_text = size.contents[0].strip()
    print(size_text)

# Extract <strong> from <h3>
for h3 in filtered_sizes:
    strong_tags = h3.find_all('strong')
    if len(strong_tags) >= 2:
        SKU = strong_tags[0].get_text(strip=True).replace('Item: ', '')
        DIMS = strong_tags[1].get_text(strip=True).replace('Dimensions: ', '')
        print(f'SKU: {SKU}')
        print(f'DIMS: {DIMS}')

# Print or process the list of image URLs
for img_url in img_urls:
    print(img_url)

# First, replace 'Small' with 'Full' in all URLs
img_urls = [img_url.replace('Small', 'Full') for img_url in img_urls]

for img_url in img_urls:
    try:
        # Skip files with ext .webp
        if img_url.lower().endswith('.webp'):
            print(f'Skipping .webp file: {img_url}')
            continue

        # Fetch the image
        img_response = requests.get(img_url)
        img_response.raise_for_status()  # Check for request errors

        # Get the image file name from the URL
        img_name = os.path.basename(img_url)

        # If URL dont have ext add .jpg
        if not any(img_name.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
            img_name += '.jpg'
        else:
            # If URL have ext keep it
            img_name = os.path.splitext(img_name)[0] + os.path.splitext(img_url)[1].lower()

        # Create a full path for saving the image
        img_path = os.path.join(download_dir, img_name)

        # Write the image content to a file
        with open(img_path, 'wb') as file:
            file.write(img_response.content)

        print(f'Downloaded: {img_url}')

    except Exception as e:
        print(f'Failed to download {img_url}: {e}')