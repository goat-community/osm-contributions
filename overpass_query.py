import requests

overpass_url = "http://overpass-api.de/api/interpreter"

queries = ['''[diff:"2020-09-24T15:00:00Z","2020-09-24T18:00:00Z"];
{{geocodeArea: München}}->.searchArea;
(
node(area.searchArea);
);
out meta geom;''']

queries = [
'''[diff:"2020-09-24T15:00:00Z","2020-09-24T23:00:00Z"];
(
way[building](47.801143, 10.914456, 48.575816, 12.152060);
);
out meta geom;''']


count = 0
for i in queries:
    count += 1
    xml = requests.get(overpass_url, params={'data': i})
    
    file_object = open(f'data_{str(count)}.xml', 'w')
    file_object.write(xml.text)
    file_object.close()



