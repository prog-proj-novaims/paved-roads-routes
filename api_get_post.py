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
    with open("config_files/00_proj.yml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config

def execute_sql_query(sql_query, db_params, commit=False):
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
    config = load_config()

    route_query = f"SELECT polygon_id, route_km, ST_AsGeoJSON(route_geom) FROM novaims.results_routes_final WHERE polygon_id = {id_param}"
    route_info = execute_sql_query(route_query, config["db_params"])

    if route_info:
        response = {
            'polygon_id': route_info[0][0],
            'route_km': float(route_info[0][1]),
            'route_geom': route_info[0][2]
        }

        # Get origin information
        origin_query = f"SELECT name, description, ST_AsGeoJSON(geom) FROM novaims.tb_origin_polygons WHERE id = {id_param}"
        origin_info = execute_sql_query(origin_query, config["db_params"])

        if origin_info:
            response['name'] = origin_info[0][0]
            response['description'] = origin_info[0][1]
            response['origin_geom'] = origin_info[0][2]

        return jsonify(response)
    else:
        id_check_query = f"SELECT id FROM novaims.tb_origin_polygons WHERE id = {id_param}"
        id_check = execute_sql_query(id_check_query, config["db_params"])

        if id_check:
            route_calc_query = f"SELECT novaims.route_calc_proj({id_param})"
            execute_sql_query(route_calc_query, config["db_params"], commit=True)

            updated_route_info = wait_for_result(id_param, config)

            if updated_route_info:
                response = {
                    'polygon_id': updated_route_info[0][0],
                    'route_km': float(updated_route_info[0][1]),
                    'route_geom': updated_route_info[0][2]
                }

                # Get origin information
                origin_query = f"SELECT name, description, ST_AsGeoJSON(geom) FROM novaims.tb_origin_polygons WHERE id = {id_param}"
                origin_info = execute_sql_query(origin_query, config["db_params"])

                if origin_info:
                    response['name'] = origin_info[0][0]
                    response['description'] = origin_info[0][1]
                    response['origin_geom'] = origin_info[0][2]

                return jsonify(response)
            else:
                return jsonify({'message': 'Error fetching route info after calculation'})
        else:
            return jsonify({'message': 'ID not found'})

@app.route('/add_origin_polygon', methods=['POST'])
def add_origin_polygon():
    config = load_config()

    # Get geometry and other values from the request
    data = request.get_json()
    geom = data.get('geom')
    name = data.get('name')
    description = data.get('description')

    # Insert the new record into tb_origin_polygons
    insert_query = f"INSERT INTO novaims.tb_origin_polygons (geom, name, description) VALUES (ST_GeomFromGeoJSON('{geom}'),  '{name}', '{description}')"
    execute_sql_query(insert_query, config["db_params"], commit=True)

    # Get the ID of the newly inserted record
    id_query = f"SELECT max(id) FROM novaims.tb_origin_polygons"
    result = execute_sql_query(id_query, config["db_params"])

    if result:
        new_id = result[0][0]
        return jsonify({'message': 'Polygon added successfully', 'id': new_id})
    else:
        return jsonify({'message': 'Error adding polygon'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
