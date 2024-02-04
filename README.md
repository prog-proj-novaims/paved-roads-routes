# paved-roads-routes

Proposal: 

Generate the shortest path to the closest paved road in rural areas, considering as rural properties limits as origins and the OSM database as the road network. Calculate the path for all registers and then serve it as a table and map for the user as a return from an API request, considering register code as parameter. 

The project will be developed over Mato Grosso state area https://en.wikipedia.org/wiki/Mato_Grosso, because it is a large state and has a large and impportant rural area. 

 

 

Data Sources: 

    OSM Geometry 

    http://download.geofabrik.de/south-america/brazil/centro-oeste.html 

    OSM attributes 

    https://overpass-turbo.eu/ 

[out:json]; 

// gather results 

way[highway~"motorway|trunk|primary|secondary|tertiary|unclassified|residential"]({{bbox}}); 

// print results 

out body; 

    Rural parcels geometry 

    http://acervofundiario.incra.gov.br/i3geo/ogc.php?tema=certificada_sigef_particular_pa 

 
