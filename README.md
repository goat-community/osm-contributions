#### Scripts OSM-contribution

This repository contains some experimental scripts to count OSM-contributions for a particular area of interest and summarizes them per assessed username in CSV-tables and creates Geojson-file of the modified/created geometries. 

#### How to use

1. Run script `overpass_query.py` to obtain changesets in XML format. 
(Note you need to adjust the overpass query to properly obtain the data that you need.)

It could be easier to run the overpass queries using the Overpass Turbo API service and export the results in the OSM-format.

Node
`[diff:"2020-09-24T15:00:00Z","2020-09-24T23:00:00Z"];
(
node({{bbox}});
);
out meta geom;`

Streets
`[diff:"2020-09-24T15:00:00Z","2020-09-24T23:00:00Z"];
(
way[highway]({{bbox}});
);
out meta geom;`

Buildings
`[diff:"2020-09-24T15:00:00Z","2020-09-24T23:00:00Z"];
(
way[building]({{bbox}});
);
out meta geom;`


2. Save the XML-files in the changesets folder and rename it according the feature type. (point.osm, line.osm, polygon.osm)

3. Add the contributors to `osm_mappers.py´.

4. Adjust the directory if necessary in `contribution_analysis.py`.

5. Run the scripts `contribution_analysis.py`

6. Check the CSV-files and Geojson-file in results-folder. 

