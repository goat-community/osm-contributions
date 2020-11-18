import xml.etree.ElementTree as ET
import geopy.distance as distance
import pandas as pd 
from osm_mappers import *
from os import path
from geojson import FeatureCollection,Feature,Point,LineString,MultiLineString,Polygon


def open_xml(path):
    xml_reader = ET.parse(path)
    return xml_reader 

def parse_attributes(xml):
    attributes = {}
    for i in xml:
        attributes[i.attrib['k']] = i.attrib['v']
   
    return attributes

def diff_attributes(old,new):
    sum_attributes = []
    diff = list(set(old.keys()).symmetric_difference(set(new.keys())))
    all_keys = list(old.keys())+list(new.keys())
    duplicates = list(set([x for x in all_keys if all_keys.count(x) > 1]))
 
    for i in duplicates:
        if old[i] != new[i]:
            diff.append(i)
    return diff
   
def parse_geom(geom_xml,geom_type,modification_type):
    coordinates = []

    if geom_type == 'line' or geom_type == 'polygon':
        for i in geom_xml.findall('./nd'):
            coordinates.append((float(i.attrib['lon']),float(i.attrib['lat'])))  
            
        if geom_type == 'line':
            geometry = Feature(geometry=LineString(coordinates))
            geometry['properties']['modification_type'] = modification_type
        if geom_type == 'polygon':
            geometry = Feature(geometry=Polygon([list(reversed(coordinates))]))
            print(coordinates)
            geometry['properties']['modification_type'] = modification_type
        dist = distance.distance(*coordinates).meters
        
        
    else:
        coordinates = [geom_xml.attrib['lon'],geom_xml.attrib['lat']]
        dist = 0
        geometry = Feature(geometry=Point((float(geom_xml.attrib['lon']),float(geom_xml.attrib['lat']))))
        geometry['properties']['modification_type'] = modification_type
        
    return coordinates, dist, geometry

def contributions_by_mapper(geoms_features, mapper, geom_type, xml_file):  
    #All modified features will be analyzed
    list_modified_keys = []
    count_modified = 0
    count_deleted = 0
    count_created = 0
    total_length = 0
    type_translation = {"point":"node","line":"way","polygon":"way"}
    
    feature_type = type_translation[geom_type]
    
    for feature in xml_file.findall("./*[@type='modify']"):        
        new_feature = feature.find("./new/"+feature_type)
        
        if new_feature == None:
            print('Cannot analyze this feature!')
            continue
        
        if new_feature.attrib['user'] == mapper:
            count_modified += 1
            old_feature = feature.find("./old/"+feature_type)
     
            attributes_old = parse_attributes(old_feature.findall('./tag'))
            attributes_new = parse_attributes(new_feature.findall('./tag'))
            
            geom_old = parse_geom(old_feature,geom_type,'modified')
            geom_new = parse_geom(new_feature,geom_type,'modified')
               
            diff_attrib = diff_attributes(attributes_old,attributes_new)
            
            geoms_features.append(geom_new[2])
            
            if geom_old[0] != geom_new[0]:       
                diff_attrib.append('geometry') 
    
            diff_attrib.append(geom_new[1])
            list_modified_keys = list_modified_keys + diff_attrib[:-1]
         
    d = {"attributes":list_modified_keys}
    df_attrib = pd.DataFrame(data=d)
    
    for feature in xml_file.findall("./*[@type='delete']"):
    
        if feature.find("./old/"+feature_type).attrib['user'] == None:
            print('Cannot analyze this feature!')
            continue
        if feature.find("./old/"+feature_type).attrib['user'] == mapper:
            count_deleted += 1
    
    
    if not df_attrib.empty:
        
        df_attrib = df_attrib.groupby('attributes').size().to_frame()
        df_attrib['Mapper'] = mapper
        df_attrib.to_csv('results/'+geom_type+'_changed_attributes.csv',mode='a',header=False)
             
        #All created features will be analyzed
        
        for feature in xml_file.findall("./*[@type='create']"):
            new_feature = feature.find("./"+feature_type)  
            if new_feature == None:
                print('Cannot analyze this feature!')
                continue
            if new_feature.attrib['user'] == mapper:
                count_created += 1
                geom_new = parse_geom(new_feature,geom_type,'new')
                dist = geom_new[1]
                geoms_features.append(geom_new[2])
                total_length = total_length + dist
        
               
        
    with open('results/'+geom_type+'_count_features.csv','a') as fd:
        fd.write(mapper+',modified_features,'+str(count_modified)+'\n')
        fd.write(mapper+',deleted_features,'+str(count_deleted)+'\n')
        fd.write(mapper+',created_features,'+str(count_created)+'\n')
        fd.write(mapper+',total_size,'+str(total_length)+'\n')

    return geoms_features


osm_mappers = list(dict.fromkeys(contributors))

for geom_type in ['point','line','polygon']:
    f_path = 'changesets/%s.osm' % geom_type
    xml_file = open_xml(f_path)

    geoms_features = []
    
    with open('results/'+geom_type+'_changed_attributes.csv','w') as fd: 
        fd.write('attribute,count,mapper\n')
        
    with open('results/'+geom_type+'_count_features.csv','w') as fd: 
        fd.write('mapper,edit_type,count\n')    
        
    for mapper in osm_mappers:
        geoms_features = contributions_by_mapper(geoms_features, mapper, geom_type, xml_file)
    
    with open('results/'+geom_type+'_geometries.geojson','w') as geoms: 
        geoms.write(str(FeatureCollection(geoms_features)))
    





    