import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from data_src import get_product_links
from database import create_tables, get_db_connection


def fetch_html(url):
    """Fetches and returns the HTML content from the given URL."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()  # Check for request errors
    return response.text


def parse_html(html_content):
    """Parses the HTML content using BeautifulSoup."""
    return BeautifulSoup(html_content, 'html.parser')


def extract_images(soup, base_url):
    """Extracts image URLs from the parsed HTML that do not have alt attributes."""
    img_tags = [img for img in soup.find_all('img') if not img.get('alt')]
    img_urls = [urljoin(base_url, img['src']) for img in img_tags if 'src' in img.attrs]
    return img_urls


def extract_text_by_class(soup, class_name):
    """Extracts and returns the text of a specific span class."""
    element = soup.find('span', class_=class_name)
    return element.get_text(strip=True) if element else None


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


def save_images(img_urls, download_dir):
    """Downloads images from the given list of URLs and saves them to the specified directory."""
    for img_url in img_urls:
        try:
            # Skip files with ext .webp
            if img_url.lower().endswith('.webp'):
                print(f'Skipping .webp file: {img_url}')
                continue

            # Fetch the image
            img_response = requests.get(img_url)
            img_response.raise_for_status()

            # Process the image name
            img_name = os.path.basename(img_url)
            if not any(img_name.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                img_name += '.jpg'
            else:
                img_name = os.path.splitext(img_name)[0] + os.path.splitext(img_url)[1].lower()

            # Create a full path for saving the image
            img_path = os.path.join(download_dir, img_name)

            # Write the image content to a file
            with open(img_path, 'wb') as file:
                file.write(img_response.content)

            print(f'Downloaded: {img_url}')

        except Exception as e:
            print(f'Failed to download {img_url}: {e}')


def process_categories(product_links):
    from models import insert_products_with_attributes_and_other_ver
    """Processes product links for all categories and saves data."""
    base_url = 'https://www.lexington.com'

    for cat, links in product_links.items():
        # Create directory for each category
        cat_dir = cat
        os.makedirs(cat_dir, exist_ok=True)

        for prod in links:
            print(f'Processing: {prod}')

            # Sanitize product name for directory
            product_name = os.path.basename(prod).replace('/', '_').replace(':', '_').replace('?', '_')
            product_dir = os.path.join(cat_dir, product_name)
            os.makedirs(product_dir, exist_ok=True)

            # Fetch and parse HTML
            prod = base_url+prod
            html_content = fetch_html(prod)
            soup = parse_html(html_content)

            # Extract product data
            img_urls = extract_images(soup, base_url)
            img_urls = [img_url.replace('Small', 'Full') for img_url in img_urls]
            dims = extract_text_by_class(soup, 'dimensions')
            stock = extract_text_by_class(soup, 'avail')
            sku = extract_text_by_class(soup, 'sku')
            sizes_and_dims = extract_sizes_and_dimensions(soup)
            extra_dims = extra_dimensions(soup)

            # Insert data into database
            insert_products_with_attributes_and_other_ver(
                name=product_name,
                sku=sku,
                stock=stock,
                dimensions=dims,
                extra_dims=extra_dims,
                sizes_and_dims=sizes_and_dims
            )

            # Save product data
            with open(os.path.join(product_dir, 'details.txt'), 'w') as f:
                f.write(f"Dimensions: {dims}\n")
                f.write(f"Stock: {stock}\n")
                f.write(f"SKU: {sku}\n")
                f.write(f"Extra Dimensions: {extra_dims}\n")
                for size_text, SKU, DIMS in sizes_and_dims:
                    f.write(f"{size_text}: SKU: {SKU}, DIMS: {DIMS}\n")
                for key, value in extra_dims.items():
                    # Zapisz linię w formacie "klucz: wartość" do pliku
                    f.write(f'{key}: {value}\n')

            # Save images
            save_images(img_urls, product_dir)


def main():
    # Initialize database and create tables
    create_tables()
    # Assume this function returns a dictionary of product links by category
    product_links = get_product_links()

    # Process categories and products
    process_categories(product_links)


if __name__ == "__main__":
    main()
