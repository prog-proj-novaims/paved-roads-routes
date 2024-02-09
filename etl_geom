import subprocess
import urllib.request
import os
import yaml

def load_config():
    with open("config/00_proj.yml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config

def download_osm_pbf(url):
    print("Downloading OSM PBF file...")
    urllib.request.urlretrieve(url, "centro-oeste-latest.osm.pbf")

def run_osmconvert(bounding_box, osmconvert_output):
    print("Running osmconvert command...")
    osmconvert_command = f"osmconvert centro-oeste-latest.osm.pbf -b={bounding_box} --complete-ways -o={osmconvert_output}"
    subprocess.run(osmconvert_command, shell=True, check=True)

def run_osm2pgrouting(osmconvert_output, osm2pgrouting_config, db_params):
    print("Running osm2pgrouting command...")
    osm2pgrouting_command = (
        f"osm2pgrouting -f {osmconvert_output} "
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
    print("Cleaning up: removing downloaded OSM PBF file...")
    os.remove("centro-oeste-latest.osm.pbf")

if __name__ == "__main__":
    config = load_config()

#    download_osm_pbf(config["osm_pbf_url"])
   run_osmconvert(config["bounding_box"], config["osmconvert_output"])
    run_osm2pgrouting(config["osmconvert_output"], config["osm2pgrouting_config"], config["db_params"])
   clean_up()

    print("ETL process completed.")
