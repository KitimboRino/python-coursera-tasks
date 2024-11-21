import urllib.request
import urllib.parse
import json
import ssl

# Service URL for the OpenGeo API
serviceurl = 'https://py4e-data.dr-chuck.net/opengeo?'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    address = input('Enter location: ')
    if len(address) < 1:
        break

    address = address.strip()  # Remove any extra spaces

    # URL encode the address parameter
    parms = dict()
    parms['q'] = address

    # Construct the full URL
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)
    
    # Send the request and retrieve data
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))

    try:
        # Try parsing the JSON data
        js = json.loads(data)
    except:
        js = None

    if not js or 'features' not in js:
        print('==== Download error ===')
        print(data)
        break

    if len(js['features']) == 0:
        print('==== Location not found ====')
        print(data)
        break

    # Extract the plus_code from the first feature
    plus_code = js['features'][0]['properties']['plus_code']
    print(f'Plus code: {plus_code}')
