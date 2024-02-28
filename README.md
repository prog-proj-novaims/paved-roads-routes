
Project Report: Paved Roads Routes
Introduction 
Routing plays a crucial role in various domains such as transportation, logistics, urban planning, and emergency response systems. The process of finding the shortest path from one location to another has significant importance in optimizing resource utilization, minimizing travel time, and enhancing overall efficiency. In agricultural contexts, routing is essential for tasks like transporting goods, machinery, and personnel between farms and marketplaces, warehouses, or processing facilities.
The importance of routing in agriculture stems from the need to streamline operations and maximize productivity while minimizing costs and resource wastage. Efficient routing can lead to significant benefits such as reduced fuel consumption, decreased vehicle wear and tear, and improved delivery timelines. For farmers, accessing paved roads efficiently is crucial for transporting crops to market or accessing essential services like veterinary care and equipment maintenance.
In the context of this project, the process involves leveraging geographic information system (GIS) tools to create a grid over the area of interest, such as farmland or agricultural regions. This grid serves as a reference for identifying farm locations and generating routes to the closest main roads. Utilizing OpenStreetMap (OSM) data provides access to a comprehensive road network, allowing for accurate routing calculations.
The implementation involves querying the OSM database through an API to retrieve road network data, including road types and geometries. By integrating farm location data with the road network data, it becomes possible to calculate the shortest path from each farm to the nearest main road. This information can then be utilized to optimize transportation routes, improve accessibility, and enhance overall efficiency in agricultural operations.
Furthermore, the flexibility of this approach allows for adaptation to various geographical regions and agricultural settings. Whether in developed or developing countries, the availability of OSM data and GIS tools enables farmers and agricultural stakeholders to implement routing solutions tailored to their specific needs and challenges. Overall, routing plays a vital role in modern agriculture by facilitating efficient movement and transportation, ultimately contributing to increased productivity and sustainability in the sector.



Objective:
The primary objective of the " paved-roads-routes-main" project is to facilitate efficient transportation logistics for farmers by generating optimized routes from farm locations to the nearest main roads. By leveraging data from the OpenStreetMap (OSM) database, the project aims to provide farmers with accurate and reliable routing information, ultimately enhancing productivity and reducing transportation costs in Baden-Württemberg region, Germany.


Data Methodology
The project relies on two main data sources: OSM geometry and OSM attributes. The OSM geometry data, available for download from the provided URL (https://download.geofabrik.de), contains detailed information about road networks, including road segments, intersections, and geographic coordinates. OSM attributes, obtained through the Overpass API (https://overpass.kumi.systems/api/interpreter), offer additional insights into road classifications, surface data, and other relevant attributes. A PostgreSQL database serves as the central repository for storing and managing the extracted OSM data in this project. The data is downloaded and loaded to the database after undergoing ETL process. Initially, the data is downloaded in PBF format and filtered using 'osmconvert' to extract relevant road network information. Subsequently, the 'osm2pgrouting' tool is employed to import the processed data into the PostgreSQL database, optimizing it for routing operations.  In this project, a Flask-based backend API is used which provides the core functionality for handling HTTP requests in the form of GET and POST related to route calculations. The front-end is built using HTML, CSS, and JavaScript, which leverages the Leaflet.js library for map visualization. 

Setup Instruction
1.	Navigate to the folder where the project is saved in your terminal. In this project, the folder is 'routing-proj'. And change directory.

 



2.	Create Environment
 ![image](https://github.com/prog-proj-novaims/paved-roads-routes/assets/123589817/e689d50a-ad7d-4b73-afac-bd1f18382ae0)


3.	Activate Environment
 

4.	Install Required Packages from ‘requirements.txt’ file
 

Database Setup
1.	Create database and schema. Load “create_tables.sql” from db folder into Postgres.
2.	Execute the following SQL commands to create necessary tables in your PostgreSQL database: 
•	Create table 'results_routes_final', where the result of calculated rout is saved. And create the create a table called 'tb_origin_polygons' from where the shortest path is calculated to nearest main road.
•	CREATE INDEX sidx_tb_origin_polygons_geom ON novaims.tb_origin_polygons USING gist (geom);
 
Running ETL
First run etl_geom and then etl_surface. If the etl is ran successfully, you receive the message "ETL process complete", otherwise you receive error.

Creating routing function
Load the “route-calculation” into Postgres and run the function.
If running the function is successful, the success message appears and the function will be created in the database.


Running API
Run the Flask-based backend API to generate HTTP requests in the form of GET and POST related to route calculations.
 

Testing the API
Testing GET request by inserting a specific id to check if the api is working properly. 

 “http://127.0.0.1:5000/get_route_info/10”
Response; { "description": null, "name": "Random parcels", "origin_geom": "{"type":"MultiPolygon","coordinates":[[[[9.207400227,47.782015419],[9.207351284,47.781706402],[9.207209244,47.781427634],[9.206988012,47.781206402],[9.206709244,47.781064362],[9.206400227,47.781015419],[9.20609121,47.781064362],[9.205812442,47.781206402],[9.20559121,47.781427634],[9.205449171,47.781706402],[9.205400227,47.782015419],[9.205449171,47.782324436],[9.20559121,47.782603204],[9.205812442,47.782824436],[9.20609121,47.782966475],[9.206400227,47.783015419],[9.206709244,47.782966475],[9.206988012,47.782824436],[9.207209244,47.782603204],[9.207351284,47.782324436],[9.207400227,47.782015419]]]]}", "polygon_id": 10, "route_geom": "{"type":"MultiLineString","coordinates":[[[9.6095221,47.7123394],[9.6090984,47.7124757],[9.6090581,47.7124611]],[[9.6093245,47.7111408],[9.609277,47.7114257],[9.6092949,47.7116979],[9.6095221,47.7123394]]]}", "route_km": 0.17415832 }

Testing POST request by inserting a specific id to make the api is working properly. 




Future Directions and challenges:
The main challenge we face in this project is allowing users to draw their own polygons representing the location from where the shortest path is calculated. And we are looking forward to resolving this issue to make the application more interactive.
Future enhancements to the project may include integrating real-time traffic data for dynamic route adjustments, implementing alternative route suggestions based on user preferences, and optimizing route planning algorithms for faster computation. Additionally, improvements in user interface design and deployment on scalable cloud platforms can enhance accessibility and performance, catering to a broader user base and supporting larger datasets.

Conclusion:
In conclusion, the "Paved Roads Routes" project addresses the critical need for efficient route planning in agricultural contexts. By harnessing the power of OSM data, database management, ETL processes, and web technologies, the project provides a valuable tool for farmers to optimize transportation logistics and enhance productivity. With continued development and enhancements, the project holds significant potential to contribute to agricultural infrastructure planning and management, ultimately benefiting farming communities worldwide.
Authors:
Enayatullah Meskinyaar 

