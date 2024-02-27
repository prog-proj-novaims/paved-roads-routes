import requests
import psycopg2
from shapely.geometry import box
from shapely.wkb import dumps
import json
import yaml

def load_config():
    """
    Load configuration settings from a YAML file.

    Returns:
        dict: Configuration settings read from the YAML file.
    """
    with open("config_files/00_proj.yml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config

def create_highway_surface_table(cursor):
    """
    Create the table for highway surface data if it doesn't exist.

    Args:
        cursor: Database cursor.

    Returns:
        None
    """
    print("Checking and creating the table...")
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS novaims.tb_highway_surface (
            id SERIAL PRIMARY KEY,
            osm_id BIGINT UNIQUE NOT NULL,
            fclass VARCHAR,
            surface VARCHAR
        );
    ''')

def get_latest_osm_id(cursor):
    """
    Get the latest processed OSM ID from the database.

    Args:
        cursor: Database cursor.

    Returns:
        int: Latest OSM ID or 0 if none exists.
    """
    cursor.execute("SELECT MAX(osm_id) FROM novaims.tb_highway_surface;")
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 0

def extract_attributes_within_grid(api_url, grid_table, db_params, desired_categories):
    """
    Extract OSM attributes within each grid cell.

    Args:
        api_url (str): Overpass API URL.
        grid_table (str): Name of the grid table.
        db_params (dict): Database connection parameters.
        desired_categories (list): List of desired OSM categories.

    Returns:
        None
    """
    # Construct the connection string
    connection_string = (
        f"dbname='{db_params['dbname']}' user='{db_params['user']}' "
        f"host='{db_params['host']}' password='{db_params['password']}' port='{db_params['port']}'"
    )
    # Connect to the PostGIS database
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    # Get the latest osm_id processed
    latest_osm_id = get_latest_osm_id(cursor)

    # Query the grid and iterate over each cell
    cursor.execute(f'SELECT id, "left", top, "right", bottom FROM {grid_table};')
    for row in cursor.fetchall():
        cell_id, left, top, right, bottom = row

        # Create a bounding box based on the cell's limits
        bounding_box = box(left, bottom, right, top)

        # Convert the bounding box to WKB (Well-Known Binary)
        bounding_box_wkb = dumps(bounding_box)

        # Build the Overpass query to get geometry-free attributes within the cell
        overpass_query = (
            f'[out:json];'
            f'way({bounding_box.bounds[1]},{bounding_box.bounds[0]},'
            f'{bounding_box.bounds[3]},{bounding_box.bounds[2]})'
            f'["highway"]["surface"];'
            f'out;'
        )

        # Make the Overpass API request
        response = requests.get(api_url, params={'data': overpass_query})
        data = response.json()

        # Process the OSM data and insert into the database
        # (You can add your specific logic here)

    # Clean up
    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Load configuration
    config = load_config()
    # Create the highway surface table
    conn = psycopg2.connect(
        dbname=config["db_params"]["dbname"],
        user=config["db_params"]["user"],
        host=config["db_params"]["host"],
        password=config["db_params"]["password"],
        port=config["db_params"]["port"]
    )
    cursor = conn.cursor()
    create_highway_surface_table(cursor)
    conn.commit()
    cursor.close()
    conn.close()

    # Extract OSM attributes within the grid
    extract_attributes_within_grid(
        api_url=config["overpass_api_url"],
        grid_table=config["grid_table"],
        db_params=config["db_params"],
        desired_categories=config["desired_categories"]
    )

    print("ETL process complete")
