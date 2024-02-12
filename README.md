# paved-roads-routes

Proposal: 

Generate the shortest path to the closest paved road in rural areas, considering as rural properties limits as origins and the OSM database as the road network. Calculate the path for all registers and then serve it as a table and map for the user as a return from an API request, considering register code as parameter. 

The project can be implemented in any country denpending on avalability of the data related to the land parcels and the generation of a grid over the area of the interest, which can be done easily with QGIS "Create GRID" tool. 

Data Sources: 

 >OSM Geometry 
    http://download.geofabrik.de/

 >OSM attributes
   https://overpass.kumi.systems/api/interpreter

   

 
