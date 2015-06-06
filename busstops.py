from bs4 import BeautifulSoup as bs
xml = open('busstops.kml', 'r')
xml_raw = xml.read()
# Parse
soup = bs(xml_raw, ['lxml', 'xml'])
placemark_datas = []
for placemark in soup.find_all('Placemark'):
    description = str(placemark.find('description'))
    description = description.replace('&lt;', '<').replace('&gt;', '>')
    placemark_data = dict()
    if description:
        description_soup = bs(description)
        for description_pair in description_soup.find_all('tr'):
            description_pair = description_pair.find_all('td')
            description_pair = map((lambda x: x.get_text()), tuple(description_pair))
            if len(description_pair) is 2:
                placemark_data[description_pair[0]] = description_pair[1]
        stop = placemark_data['0=Stop 1=Station'] == 'Stop'
        longitude, latitude, altitude = placemark.Point.coordinates.get_text().strip().split(',')
        placemark_data['Latitude'] = latitude
        placemark_data['Longitude'] = longitude
        placemark_data['Location Type'] = '0' if stop else '1'
    placemark_datas.append(placemark_data)

# Print
output_fields = {
    'route_id': 'Route Number',
    'stop_id': 'GlobalID',
    'stop_name': 'Stop Name',
    'stop_lat': 'Latitude',
    'stop_long': 'Longitude',
    'location_type': 'Location Type',
    'stop_desc': 'Description of Stop',
    'stop_seq': 'Stop Number'
}
commafy = lambda x: ','.join(x)
linify = lambda x: '\n'.join(x)
values = lambda x: map(lambda y: x.get(y), output_fields.values())
output_file = open('busstops.txt', 'w')
output_file.write(
    linify([commafy(output_fields.keys())] + map(commafy, map(values, placemark_datas))
))

### Placemark
#   name
#   coordinates (trim, longitude, lattitude)
#   description
#       tr where td is Route Number
#       Stop Number
#       Inbound or Outbound
###
