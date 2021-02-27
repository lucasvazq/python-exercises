Script para obtener datos geográficos de Argentina

Herramientas complementarias que nos permite recortar parte de los datos y minificarlos: https://mapshaper.org/

Resultado final: 

## Rutas provinciales (geojson)
```python
import json
import requests

url = 'https://ide.transporte.gob.ar/geoserver/observ/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=observ:_3.4.1.7.red_vial_ign_ont_a_prov_view&outputFormat=application%2Fjson'
output_file = 'provincial_routes.geojson'
precision = 4

def process_coordinates(coordinates):
    if isinstance(coordinates, list):
        return [process_coordinates(x) for x in coordinates]
    return round(coordinates, precision)

response = requests.get(url)
json_data = response.json()

for feature in json_data['features']:
    feature['geometry']['coordinates'] = process_coordinates(feature['geometry']['coordinates'])
    for key in [key for key in feature.keys() if key not in ('type', 'geometry')]:
        del feature[key]

for key in [key for key in json_data.keys() if key not in ('type', 'features')]:
    del json_data[key]

with open(output_file, 'w') as file:
    file.write(json.dumps(json_data))
```

## Rutas nacionales (geojson)
```python
import json
import requests

url = 'https://ide.transporte.gob.ar/geoserver/observ/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=observ:_3.4.1.1.6.rutas_nacionales_dnv18.view&outputFormat=text%2Fjavascript'
output_file = 'national_routes.geojson'
precision = 4

def process_coordinates(coordinates):
    if isinstance(coordinates, list):
        return [process_coordinates(x) for x in coordinates]
    return round(coordinates, precision)

response = requests.get(url)
json_data = json.loads(response.text[14:-1])

for feature in json_data['features']:
    feature['geometry']['coordinates'] = process_coordinates(feature['geometry']['coordinates'])
    for key in [key for key in feature.keys() if key not in ('type', 'geometry')]:
        del feature[key]

for key in [key for key in json_data.keys() if key not in ('type', 'features')]:
    del json_data[key]

with open(output_file, 'w') as file:
    file.write(json.dumps(json_data))
```

## Provincias (topojson)
```python
import json
import requests

url = 'https://raw.githubusercontent.com/deldersveld/topojson/master/countries/argentina/argentina-provinces.json'
output_file = 'provinces.topojson'

response = requests.get(url)
json_data = response.json()

json_data['objects']['provinces'] = json_data['objects'].pop('ARG_adm1')
for geometry in json_data['objects']['provinces']['geometries']:
    for key in [key for key in geometry.keys() if key not in ('arcs', 'type')]:
        del geometry[key]

with open(output_file, 'w') as file:
    file.write(json.dumps(json_data))
```
