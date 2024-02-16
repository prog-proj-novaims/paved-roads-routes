-- DROP FUNCTION novaims.route_calc_proj(int4);

CREATE OR REPLACE FUNCTION novaims.route_calc_proj(id_param integer)
 RETURNS text
 LANGUAGE plpgsql
AS $function$
BEGIN
    WITH ClosestNode AS (
        SELECT
            p.fid AS polygon_id,
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
            p.fid = id_param
    ),
    centroid_parcel AS (
        SELECT
            p.fid AS polygon_id,
            ST_Centroid(st_transform(p.geom, 4326)) as parcel_centroid
        FROM
            novaims.tb_origin_polygons p
        WHERE
            p.fid = id_param
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
        IF (select fid from novaims.tb_origin_polygons where fid = id_param) is null THEN
        RETURN 'Error: ID not found.';
    ELSE
        RETURN 'Route calculated successfully.';
    END IF;
END $function$
;
