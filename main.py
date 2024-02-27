from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import psycopg2
import yaml
import time
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

def load_config():
    """
    Load configuration settings from a YAML file.

    Returns:
        dict: Configuration settings read from the YAML file.
    """
    with open("config_files/00_proj.yml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config

def execute_sql_query(sql_query, db_params, commit=False):
    """
    Execute an SQL query using psycopg2.

    Args:
        sql_query (str): SQL query to execute.
        db_params (dict): Database connection parameters.
        commit (bool, optional): Whether to commit the transaction. Defaults to False.

    Returns:
        list or None: Result of the query or None if an error occurs.
    """
    connection_string = (
        f"dbname='{db_params['dbname']}' user='{db_params['user']}' "
        f"host='{db_params['host']}' password='{db_params['password']}' port='{db_params['port']}'"
    )

    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute(sql_query)

        if commit:
            conn.commit()

        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result
    except psycopg2.Error as e:
        print(f"Error executing SQL query: {e}")
        return None

def wait_for_result(id_param, config):
    """
    Wait for the result of a route calculation.

    Args:
        id_param (int): Polygon ID.
        config (dict): Configuration settings.

    Returns:
        list or None: Result of the route calculation or None if not found.
    """
    max_attempts = 10
    for attempt in range(max_attempts):
        time.sleep(2)
        result = execute_sql_query(
            f"SELECT polygon_id, route_km, ST_AsGeoJSON(route_geom) FROM novaims.results_routes_final WHERE polygon_id = {id_param}",
            config["db_params"]
        )

        if result:
            return result
        else:
            socketio.emit('update_message', {'message': 'Calculating route...'})

    return None

@app.route('/get_route_info/<int:id_param>', methods=['GET'])
def get_route_info(id_param):
    """
    Get route information for a given polygon ID.

    Args:
        id_param (int): Polygon ID.

    Returns:
        dict: Route information.
    """
    config = load_config()

    route_query = f"SELECT polygon_id, route_km, ST_AsGeoJSON(route_geom) FROM novaims.results_routes_final WHERE polygon_id = {id_param}"
    route_info = execute_sql_query(route_query, config["db_params"])

    if route_info:
        response = {
            'polygon_id': route_info[0][0],
            'route_km': float(route_info[0][1]),
            'route_geometry': json.loads(route_info[0][2])
        }
        return jsonify(response)
    else:
        return jsonify({'message': 'Route information not found'})

if __name__ == '__main__':
    socketio.run(app)
