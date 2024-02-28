
# Project title: Paved-roads-routes-main
# Introduction 
The "Paved Road Finder" is a Python-based application designed to efficiently locate the shortest path to the nearest paved road from a given parcel ID. It addresses the critical need for accurate road surface information, crucial for various scenarios such as emergency response planning and outdoor recreation. Leveraging road network data from sources like OpenStreetMap (OSM) and Overpass Turbo, the application collects details on road geometry and attributes, including whether roads are paved or unpaved. Through a user-friendly interface, users input the Parcel ID, and the application dynamically calculates the optimal route to the nearest paved road based on the collected data. The identified path is then visualized on an interactive map interface, providing users with a clear understanding of the route


# Objective
The primary objective of the " paved-roads-routes-main" project is to facilitate efficient transportation logistics by generating optimized routes to the nearest main roads. By leveraging data from the OpenStreetMap (OSM) database, the project aims to provide accurate and reliable routing information, ultimately enhancing productivity and reducing transportation costs in Bavaria region, Germany.


# Data Methodology
The project relies on two main data sources: OSM geometry and OSM attributes. The OSM geometry data, available for download from the provided URL (https://download.geofabrik.de), contains detailed information about road networks, including road segments, intersections, and geographic coordinates. OSM attributes, obtained through the Overpass API (https://overpass.kumi.systems/api/interpreter), offer additional insights into road classifications, surface data, and other relevant attributes. A PostgreSQL database serves as the central repository for storing and managing the extracted OSM data in this project. The data is downloaded and loaded to the database after undergoing ETL process. Initially, the data is downloaded in PBF format and filtered using 'osmconvert' to extract relevant road network information. Subsequently, the 'osm2pgrouting' tool is employed to import the processed data into the PostgreSQL database, optimizing it for routing operations.  In this project, a Flask-based backend API is used which provides the core functionality for handling HTTP requests in the form of GET and POST related to route calculations. The front-end is built using HTML, CSS, and JavaScript, which leverages the Leaflet.js library for map visualization. 

# Setup Instruction
1.	Navigate to the folder where the project is saved in your terminal. In this project, the folder is 'routing-proj'. And change directory.

 ![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/3c91a9ba-f492-45d2-83d2-5e6fe5bbcd6d)




2.	Create Environment

![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/3ef4c6de-bd7b-48d6-b46a-78b208495127)


3.	Activate Environment
   
![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/c289ae7e-5707-408f-955c-20b0bdcb2bd1)



5.	Install Required Packages from ‘requirements.txt’ file
![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/16dbdc13-67dd-49d9-8c4f-29f735d57c79)



# Database Setup
1.	Create database and schema. Load “create_tables.sql” from db folder into Postgres.
2.	Execute the following SQL commands to create necessary tables in your PostgreSQL database: 
•	Create table 'results_routes_final', where the result of calculated rout is saved. And create the create a table called 'tb_origin_polygons' from where the shortest path is calculated to nearest main road.
•	CREATE INDEX sidx_tb_origin_polygons_geom ON novaims.tb_origin_polygons USING gist (geom);
 ![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/3dc459a1-95fd-4b9f-990b-1590ca6b001e)

# Running ETL
First run etl_geom and then etl_surface. If the etl is ran successfully, you receive the message "ETL process complete", otherwise you receive error.
![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/1bf599bc-aa38-4636-843f-9b76e0676fd2)

Creating routing function
Load the “route-calculation” into Postgres and run the function.
If running the function is successful, the success message appears and the function will be created in the database.
![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/674c42dc-ad0f-4d23-b62e-fd3d9a51363a)



# Running API
Run the Flask-based backend API to generate HTTP requests in the form of GET and POST related to route calculations.
 
![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/a98ffa31-b36f-43a6-8c42-0ecf5b4d815f)

# Testing the API

 Testing a GET request by inserting a specific id to check if the API is working properly.
 Put this link in the browser: http://127.0.0.1:5000/get_route_info/10
 The response should look like this:
 

response = {
    "description": None,
    "name": "Random parcels",
    "origin_geom": {
        "type": "MultiPolygon",
        "coordinates": [
            [
                [
                    [9.207400227, 47.782015419],
                    [9.207351284, 47.781706402],
                    [9.207209244, 47.781427634],
                    [9.206988012, 47.781206402],
                    [9.206709244, 47.781064362],
                    [9.206400227, 47.781015419],
                    [9.20609121, 47.781064362],
                    [9.205812442, 47.781206402],
                    [9.20559121, 47.781427634],
                    [9.205449171, 47.781706402],
                    [9.205400227, 47.782015419],
                    [9.205449171, 47.782324436],
                    [9.20559121, 47.782603204],
                    [9.205812442, 47.782824436],
                    [9.20609121, 47.782966475],
                    [9.206400227, 47.783015419],
                    [9.206709244, 47.782966475],
                    [9.206988012, 47.782824436],
                    [9.207209244, 47.782603204],
                    [9.207351284, 47.782324436],
                    [9.207400227, 47.782015419]
                ]
            ]
        ]
    },
    "polygon_id": 10,
    "route_geom": {
        "type": "MultiLineString",
        "coordinates": [
            [
                [9.6095221, 47.7123394],
                [9.6090984, 47.7124757],
                [9.6090581, 47.7124611]
            ],
            [
                [9.6093245, 47.7111408],
                [9.609277, 47.7114257],
                [9.6092949, 47.7116979],
                [9.6095221, 47.7123394]
            ]
        ]
    },
    "route_km": 0.17415832
}


 
 Testing POST request with curl (linux terminal)
 Using curl to send a POST request with JSON data to add a new origin polygon
 Replace the curl command with equivalent Python code

import requests

url = 'http://127.0.0.1:5000/add_origin_polygon'
headers = {'Content-Type': 'application/json'}
data = {
    "geom": "{\"type\":\"Polygon\",\"coordinates\":[[[9.405691, 47.694781],[9.405691, 47.695781],[9.406691, 47.695781],[9.406691, 47.694781],[9.405691, 47.694781]]]}",
    "name": "Square in Markdorf",
    "description": "A square polygon in Markdorf, Germany"
}

response = requests.post(url, json=data, headers=headers)

print(response.json())


# Front End:
The frontend web application offers an intuitive user interface for interacting with the routing system. It is built using HTML, CSS, and JavaScript, which leverages the Leaflet.js library for map visualization.This allows users to make get request by inserting the id of farm locations , then it calculates distances, and visualize route information dynamically. The frontend also seamlessly communicates with the backend API to retrieve routing data and update the user interface in real-time.  
![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/158604785/29a2ba11-9cc1-4c46-a8bc-d47eb520e612)
![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/158604785/8157c37c-5398-4b61-8b65-f6968f25fd2b)



# Future Directions and challenges
The main challenge we face in this project is allowing users to draw their own polygons representing the location from where the shortest path is calculated. And we are looking forward to resolving this issue to make the application more interactive.
Future enhancements to the project may include integrating real-time traffic data for dynamic route adjustments, implementing alternative route suggestions based on user preferences, and optimizing route planning algorithms for faster computation. Additionally, improvements in user interface design and deployment on scalable cloud platforms can enhance accessibility and performance, catering to a broader user base and supporting larger datasets.

# Conclusion
In conclusion, the "Paved Roads Routes" project addresses the critical need for efficient route planning in agricultural contexts. By harnessing the power of OSM data, database management, ETL processes, and web technologies, the project provides a valuable tool for farmers to optimize transportation logistics and enhance productivity. With continued development and enhancements, the project holds significant potential to contribute to agricultural infrastructure planning and management, ultimately benefiting farming communities worldwide.
# Authors
Enayatullah Meskinyaar is currently a master of  

