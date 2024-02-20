import subprocess
import urllib.request
import os
import yaml

def load_config():
    # Load configuration from YAML file
    with open("config_files/00_proj.yml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config

def download_osm_pbf(url):
    # Download OSM PBF file from the provided URL
    print("Downloading OSM PBF file...")
    urllib.request.urlretrieve(url, "temporary_data.osm.pbf")

def run_osmconvert(bounding_box, osmconvert_output):
    # Run osmconvert command to filter and process OSM data
    print("Running osmconvert command...")
    osmconvert_command = (
        f"osmconvert temporary_data.osm.pbf --complete-ways "
        f"-o={osmconvert_output} --drop-author --drop-version"
    )
    subprocess.run(osmconvert_command, shell=True, check=True)

def run_osm2pgrouting(osmconvert_output, osm2pgrouting_config, db_params):
    # Run osm2pgrouting command to import OSM data into the database with pgRouting
    print("Running osm2pgrouting command...")
    osm2pgrouting_command = (
        f"osm2pgrouting --chunk 100000 -f {osmconvert_output} "
        f"--dbname {db_params['dbname']} "
        f"--username {db_params['user']} "
        f"--host {db_params['host']} "
        f"--port {db_params['port']} "
        f"-W {db_params['password']} "
        f"-c {osm2pgrouting_config} "
        f"--schema novaims"
    )
    subprocess.run(osm2pgrouting_command, shell=True, check=True)

def clean_up():
    # Clean up: remove downloaded OSM PBF file
    print("Cleaning up: removing downloaded OSM PBF file...")
    os.remove("temporary_data_bb.osm")

if __name__ == "__main__":
    # Load configuration
    config = load_config()

    #download_osm_pbf(config["osm_pbf_url"])
    # Run osmconvert and osm2pgrouting
    # run_osmconvert(config["bounding_box"], config["osmconvert_output"])
    run_osm2pgrouting(config["osmconvert_output"], config["osm2pgrouting_config"], config["db_params"])
    #clean_up()

    print("ETL process completed.")
