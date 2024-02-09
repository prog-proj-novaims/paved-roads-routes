import requests
import psycopg2
from shapely.geometry import box
from shapely.wkb import dumps
import json
import yaml

def load_config():
    with open("config/00_proj.yml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config

 # Create the table if it doesn't exist
    print("Checking and creating the table...")
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS novaims.tb_highway_surface (
            id SERIAL PRIMARY KEY,
            osm_id BIGINT,
            fclass VARCHAR,
            surface VARCHAR
        );
    ''')

def get_latest_osm_id(cursor):
    cursor.execute("SELECT MAX(osm_id) FROM novaims.tb_highway_surface;")
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 0

def extract_attributes_within_grid(api_url, grid_table, db_params, desired_categories):
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
            f'{bounding_box.bounds[3]},{bounding_box.bounds[2]})["highway"]["surface"];'
            f'out;'
        )

        # Make the request to the Overpass API
        print(f"Requesting data for cell {cell_id}...")
        try:
            response = requests.post(api_url, data={'data': overpass_query})
            response.raise_for_status()  # Check if the request was successful
            data = response.json()

            # Process the data and extract geometry-free attributes for desired categories
            for feature in data.get('elements', []):
                tags = feature.get('tags', {})
                osm_id = feature.get('id')
                category = tags.get('highway')
                surface = tags.get('surface')

                # Check if the category is in the desired list and osm_id is greater than the latest processed
                if category in desired_categories and osm_id > latest_osm_id:
                    # Update or insert the data into the table
                    cursor.execute(
                        "INSERT INTO novaims.tb_highway_surface (osm_id, fclass, surface) "
                        "VALUES (%s, %s, %s) "
                        "ON CONFLICT (osm_id) DO UPDATE SET "
                        "fclass = EXCLUDED.fclass, surface = EXCLUDED.surface;",
                        (osm_id, category, surface)
                    )
        except requests.exceptions.RequestException as e:
            print(f"Error in request for cell {cell_id}: {e}")

    print("Committing and closing the connection...")
    # Commit and close the connection to the database
    conn.commit()
    cursor.close()
    conn.close()

    print("Data extraction completed.")

if __name__ == "__main__":
    config = load_config()

    # Call the function to extract geometry-free attributes
    extract_attributes_within_grid(
        config["overpass_api_url"], config["grid_table_name"], config["db_params"], config["desired_categories"]
    )
