# paved-roads-routes

Proposal: 

Generate the shortest path from farms to the closest paved road. It is done using road network from OSM database returning the distance and the route geometry by an API request, considering the farm ID as parameter. 

The project can be implemented in any country depending on the availability of the data related to the land parcels and the generation of a grid over the area of the interest, which can be done easily with QGIS "Create GRID" tool. 

Data Sources: 

 >OSM Geometry 
    http://download.geofabrik.de/

 >OSM attributes
   https://overpass.kumi.systems/api/interpreter

   



##testing get
http://127.0.0.1:5000/get_route_info/10
Response; {
    "description": null,
    "name": "Random parcels",
    "origin_geom": "{\"type\":\"MultiPolygon\",\"coordinates\":[[[[9.207400227,47.782015419],[9.207351284,47.781706402],[9.207209244,47.781427634],[9.206988012,47.781206402],[9.206709244,47.781064362],[9.206400227,47.781015419],[9.20609121,47.781064362],[9.205812442,47.781206402],[9.20559121,47.781427634],[9.205449171,47.781706402],[9.205400227,47.782015419],[9.205449171,47.782324436],[9.20559121,47.782603204],[9.205812442,47.782824436],[9.20609121,47.782966475],[9.206400227,47.783015419],[9.206709244,47.782966475],[9.206988012,47.782824436],[9.207209244,47.782603204],[9.207351284,47.782324436],[9.207400227,47.782015419]]]]}",
    "polygon_id": 10,
    "route_geom": "{\"type\":\"MultiLineString\",\"coordinates\":[[[9.6095221,47.7123394],[9.6090984,47.7124757],[9.6090581,47.7124611]],[[9.6093245,47.7111408],[9.609277,47.7114257],[9.6092949,47.7116979],[9.6095221,47.7123394]]]}",
    "route_km": 0.17415832
}

##testing post with curl (linux terminal)
curl -X POST -H "Content-Type: application/json" -d '{
  "geom": "{\"type\":\"Polygon\",\"coordinates\":[[[9.405691, 47.694781],[9.405691, 47.695781],[9.406691, 47.695781],[9.406691, 47.694781],[9.405691, 47.694781]]]}",
  "name": "Square in Markdorf",
  "description": "A square polygon in Markdorf, Germany"
}' http://127.0.0.1:5000/add_origin_polygon

