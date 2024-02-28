
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
