# Project Title: Paved Roads Routes

## Introduction
The "Paved Road Finder" is a Python-based application crafted to efficiently determine the shortest path to the nearest paved road from a given parcel ID. This tool addresses the crucial need for accurate road surface information, essential for scenarios such as emergency response planning and outdoor recreation. Utilizing road network data from sources like OpenStreetMap (OSM) and Overpass Turbo, the application collects details on road geometry and attributes, distinguishing between paved and unpaved roads. Users input the Parcel ID via a user-friendly interface, and the application dynamically calculates the optimal route to the nearest paved road based on the gathered data. The identified path is then visualized on an interactive map interface, providing users with a clear understanding of the route.

## Objective
The primary objective of the "Paved Roads Routes" project is to facilitate efficient transportation logistics by generating optimized routes to the nearest main roads, considering its surface attributes. Leveraging data from the OpenStreetMap (OSM) database, the project aims to provide accurate and reliable routing information, ultimately enhancing productivity and reducing transportation costs for any region.

## Data Methodology
The project relies on two main data sources: OSM geometry and OSM attributes. The OSM geometry data, downloadable from [GeoFabrik](https://download.geofabrik.de), contains detailed information about road networks, including road segments, intersections, and geographic coordinates. OSM attributes, obtained through the Overpass API ([Overpass API](https://overpass.kumi.systems/api/interpreter)), offer additional insights into road classifications, surface data, and other relevant attributes. A PostgreSQL database serves as the central repository for storing and managing the extracted OSM data in this project. The data undergoes an Extract, Transform, Load (ETL) process, initially downloaded in PBF format, filtered using 'osmconvert,' and then imported into the PostgreSQL database using 'osm2pgrouting.' The Flask-based backend API handles HTTP requests related to route calculations, while the front-end is built using HTML, CSS, and JavaScript, leveraging the Leaflet.js library for map visualization.

## Setup Instructions
1. Navigate to the project folder in your terminal (e.g., 'routing-proj') and change the directory.
   ![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/3c91a9ba-f492-45d2-83d2-5e6fe5bbcd6d)

2. Create Environment
   ![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/3ef4c6de-bd7b-48d6-b46a-78b208495127)

3. Activate Environment
   ![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/c289ae7e-5707-408f-955c-20b0bdcb2bd1)

4. Install Required Packages from ‘requirements.txt’ file
   ![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/16dbdc13-67dd-49d9-8c4f-29f735d57c79)

5. Setup up the yalm file with the connection and the desired parameters

## Database Setup
1. Create a database and schema. Load “create_tables.sql” from the db folder into PostgreSQL.
2. Execute the following SQL commands to create necessary tables in your PostgreSQL database:
   - Create 'results_routes_final' table to store calculated route results.
   - Create 'tb_origin_polygons' table for calculating the shortest path to the nearest main road.
   - Create an index on 'tb_origin_polygons' geometry column for efficient spatial queries.
   ![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/3dc459a1-95fd-4b9f-990b-1590ca6b001e)

## Running ETL
Run 'etl_geom' and 'etl_surface.' If the ETL runs successfully, you will receive the message "ETL process complete"; otherwise, an error will be displayed.
![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/1bf599bc-aa38-4636-843f-9b76e0676fd2)

## Creating Routing Function
Load “route-calculation” into PostgreSQL and execute the function. A success message indicates that the function is created in the database.
![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/674c42dc-ad0f-4d23-b62e-fd3d9a51363a)

## Running API
Run the Flask-based backend API to handle HTTP requests related to route calculations.
![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/a98ffa31-b36f-43a6-8c42-0ecf5b4d815f)

## Testing the API
Test a GET request by inserting a specific ID to check if the API is

 working properly. Use the link http://127.0.0.1:5000/get_route_info/10 to get a response similar to the provided JSON structure.
```python
response = {
    "description": None,
    "name": "Random parcels",
    "origin_geom": {...},
    "polygon_id": 10,
    "route_geom": {...},
    "route_km": 0.17415832
}
```
Test a POST request using curl (Linux terminal) or equivalent Python code to add a new origin polygon.

```
curl -X POST -H "Content-Type: application/json" -d '{
  "geom": "{\"type\":\"Polygon\",\"coordinates\":[[[9.405691, 47.694781],[9.405691, 47.695781],[9.406691, 47.695781],[9.406691, 47.694781],[9.405691, 47.694781]]]}",
  "name": "Square in Markdorf",
  "description": "A square polygon in Markdorf, Germany"
}' http://127.0.0.1:5000/add_origin_polygon
```


## Front End
The frontend web application offers an intuitive user interface for interacting with the routing system. Built using HTML, CSS, and JavaScript, it leverages the Leaflet.js library for map visualization. Users can make GET requests by inserting farm location IDs, calculate distances, and visualize route information dynamically. The frontend communicates seamlessly with the backend API, updating the user interface in real-time.
![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/158604785/29a2ba11-9cc1-4c46-a8bc-d47eb520e612)
![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/158604785/8157c37c-5398-4b61-8b65-f6968f25fd2b)

## Future Directions and Challenges
The were two main challenges we faced in this project, the first is allowing user to draw their own polygons representing the location from where the shortest path is calculated. And we are looking forword to resolve this issue to make the application more interactive and also to host a interesting database from places in which people whould have interest in know this kind of information. The second was related to nodes that were close to the origin but the path to them was longer than to the next node from a paved road. It can be a bit difccult to explain and to understand, but as an image can talk for tousand words, this figure ilustrate that 
[figures/example.png](https://github.com/prog-proj-novaims/paved-roads-routes/blob/276c08518d6e47d991b6e5c098a4762db80e6f84/figures/example.png)

Future enhancements may include real-time traffic data integration, alternative route suggestions based on user preferences, and optimizing route planning algorithms for faster computation.

Improvements in UI design and deployment on scalable cloud platforms can enhance accessibility and performance, catering to a broader user base and supporting larger datasets.

## Conclusion
In conclusion, the "Paved Roads Routes" project addresses the critical need for efficient route planning in agricultural contexts. By harnessing the power of OSM data, database management, ETL processes, and web technologies, the project provides a valuable tool for farmers to optimize transportation logistics and enhance productivity. With continued development and enhancements, the project holds significant potential to contribute to agricultural infrastructure planning and management, ultimately benefiting farming communities worldwide.

