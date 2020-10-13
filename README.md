#### Scripts OSM-contribution

This repository contains some experimental scripts to count OSM-contributions for a particular area of interest and summarizes them per assessed username in CSV-tables. 

#### How to use

1. Run script `overpass_query.py` to obtain changesets in XML format. 
(Note you need to adjust the overpass query to properly obtain the data that you need.)

2. Save the XML-file in the changesets folder and rename it according the feature type. (points.xml, lines.xml, polygons.xml)

3. Adjust the directory if necessary in `contribution_analysis.py`.

4. Run the scripts `contribution_analysis.py`

5. Check the CSV-file in results. 

