def route_calc_proj(id_param):
    """
    Calculate the route projection for a given polygon ID.

    Args:
        id_param (int): Polygon ID.

    Returns:
        str: Text representation of the calculated route projection.
    """
    with ClosestNode AS (
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
                    WHERE
                        v.the_geom = ClosestNode.nearest_node
                    ORDER BY
                        pmp.polygon_id, cost
                    LIMIT 1
                )
            ) AS route
        FROM
            ClosestNode
    )
    SELECT
        Routes.polygon_id,
        ST_AsText(ST_MakeLine(Routes.route.geom)) as route_geometry
    FROM
        Routes
    WHERE
        Routes.polygon_id = id_param;
