
CREATE TABLE novaims.results_routes_final (
	polygon_id int4 NULL,
	route_km float4 NULL,
	route_geom public.geometry NULL,
	"name" varchar NULL,
	description varchar NULL
);

CREATE TABLE novaims.tb_origin_polygons (
	id serial4 NOT NULL,
	geom public.geometry(multipolygon, 4326) NULL,
	"name" varchar(200) NULL,
	description varchar(255) NULL,
	CONSTRAINT tb_origin_polygons_pkey PRIMARY KEY (id)
);
CREATE INDEX sidx_tb_origin_polygons_geom ON novaims.tb_origin_polygons USING gist (geom);

-- DROP FUNCTION novaims.route_calc_proj(int4);

CREATE OR REPLACE FUNCTION novaims.route_calc_proj(id_param integer)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
BEGIN
    WITH ClosestNode AS (
        SELECT
            p.id AS polygon_id,
            v.source,
            (ST_ClosestPoint(v.the_geom, ST_Centroid(st_transform(p.geom, 4326)))) as nearest_node
        FROM
            novaims.tb_origin_polygons p,
            LATERAL (
                SELECT 
                    a.source,
                    the_geom
                FROM (
                    SELECT
                        a.*,
                        c.surface,
                        c.fclass
                    FROM
                        novaims.ways a -- roads lines
                        JOIN novaims.tb_highway_surface -- roads surface
                        c ON c.osm_id = a.osm_id
                ) a
                WHERE
                    "surface" IN ('asphalt','paved','pavimentado','concrete') AND
                    "fclass" IN ('motorway','motorway_junction','motorway_link','primary',
                    			'primary_link','road','secondary','secondary_link',
                    			'tertiary','tertiary_link','trunk','trunk_link')
                ORDER BY a.the_geom <-> ST_Centroid(st_transform(p.geom, 4326))
                LIMIT 1
            ) AS v
        WHERE
            p.id = id_param
    ),
    centroid_parcel AS (
        SELECT
            p.id AS polygon_id,
            ST_Centroid(st_transform(p.geom, 4326)) as parcel_centroid
        FROM
            novaims.tb_origin_polygons p
        WHERE
            p.id = id_param
    ),
    Routes AS (
        SELECT
            pmp.polygon_id,
            (
                pgr_bddijkstra(
                    'SELECT gid as id, source, target, length_m/1000 as cost FROM novaims.ways',
                    (SELECT id FROM 
                                    novaims.ways_vertices_pgr v, -- road nodes
                                    centroid_parcel cass
                            ORDER BY v.the_geom <-> cass.parcel_centroid LIMIT 1),
                   pmp.source,
                    FALSE -- directional parameter
                )
            ).*
        FROM
            ClosestNode pmp
    )
    INSERT INTO novaims.results_routes_final(polygon_id, route_km, route_geom)
    SELECT
        route.polygon_id,
        sum(st_length(road.the_geom::geography))/1000 AS route_km,
        ST_Collect(road.the_geom) AS route_geom
    FROM
        (
            SELECT
                polygon_id,
                edge
            FROM
                Routes
        ) AS route
        JOIN novaims.ways AS road ON route.edge = road.gid
    GROUP BY
        route.polygon_id;             
        IF (select id from novaims.tb_origin_polygons where id = id_param) is null THEN
        RETURN 'Error: ID not found.';
    ELSE
        RETURN 'Route calculated successfully.';
    END IF;
END $function$
;


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




