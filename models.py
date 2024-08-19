from database import get_db_connection, create_tables
from app import main

def insert_products_with_attributes_and_other_ver(name: str, sku: str, stock: str, dimensions: str, extra_dims: dict, sizes_and_dims: list):
    # Connection and cursor creation
    conn = get_db_connection()
    cursor = conn.cursor()

    # Default values if no information on site
    if dimensions is None:
        dimensions = "NO DATA"
    elif extra_dims is None:
        extra_dims = "NO DATA"
    elif sizes_and_dims is None:
        sizes_and_dims = "NO DATA"

    # Entry products data
    cursor.execute('''
        INSERT INTO products (name, sku, dimensions, stock)
        VALUES (?, ?, ?, ?)
        ''', (name, sku, dimensions, stock))

    # Take Product ID
    product_id = cursor.lastrowid

    # Entry Product Attributes
    for key, value in extra_dims.items():
        cursor.execute('''
        INSERT INTO product_attribute (product_id, attribute_key, attribute_value)
        VALUES (?, ?, ?)
        ''', (product_id, key, value))

    # Entry Product Other Versions
    other_versions_with_id = [(product_id, name, sku, dimensions) for name, sku, dimensions in sizes_and_dims]
    cursor.executemany('''
    INSERT INTO product_other_versions (product_id, name, sku, dimensions)
    VALUES (?, ?, ?, ?)
    ''', other_versions_with_id)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    insert_products_with_attributes_and_other_ver()


