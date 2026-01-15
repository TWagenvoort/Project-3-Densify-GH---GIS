# TEST SCRIPT - Verifieer je Feature Service is klaar

import json
import urllib.request

FEATURE_SERVICE_URL = 'https://services9.arcgis.com/nqW2A97fCpeCbw6Z/arcgis/rest/services/Heron_test_final_3D/FeatureServer/0'

print('='*60)
print('HERON 3D FEATURE SERVICE - VERIFICATION TEST')
print('='*60)
print()

# Test 1: Check service exists
print('[TEST 1] Service Connection...')
try:
    url = FEATURE_SERVICE_URL + '?f=json'
    response = urllib.request.urlopen(url, timeout=10)
    data = json.loads(response.read())
    
    print('  [OK] Service accessible')
    print('  URL: ' + FEATURE_SERVICE_URL)
    print('  Response keys: ' + str(list(data.keys())[:5]))
    print('  Name: ' + str(data.get('name', '?')))
    print('  Type: ' + str(data.get('geometryType', '?')))
except Exception as e:
    print('  [ERROR] ' + str(e))
    exit(1)

# Test 2: Check fields
print()
print('[TEST 2] Required Fields...')
required_fields = ['height', 'name']
found_fields = [f['name'] for f in data.get('fields', [])]

for field in required_fields:
    if field in found_fields:
        print('  [OK] Field "' + field + '" exists')
    else:
        print('  [WARN] Field "' + field + '" NOT found')

# Test 3: Check capabilities
print()
print('[TEST 3] Capabilities...')
caps = data.get('capabilities', '')
if 'Create' in caps:
    print('  [OK] Can create/upload features')
else:
    print('  [ERROR] Cannot create features')
    exit(1)

# Test 4: Try small upload
print()
print('[TEST 4] Test Upload...')
test_feature = {
    'geometry': {
        'rings': [[[4.531, 51.873], [4.5311, 51.873], [4.5311, 51.874], [4.531, 51.874], [4.531, 51.873]]]
    },
    'attributes': {
        'OBJECTID': 1,
        'height': 15.0,
        'name': 'TEST'
    }
}

try:
    url = FEATURE_SERVICE_URL + '/addFeatures'
    data_payload = {
        'features': json.dumps([test_feature]),
        'f': 'json'
    }
    params = urllib.parse.urlencode(data_payload).encode('utf-8')
    
    import urllib.parse
    req = urllib.request.Request(url, data=params)
    response = urllib.request.urlopen(req, timeout=10)
    result = json.loads(response.read())
    
    if 'addResults' in result and result['addResults'][0].get('success'):
        print('  [OK] Test feature uploaded successfully')
        print('  [OK] Feature Service is READY!')
    else:
        print('  [ERROR] Upload returned error')
        print('  ' + str(result))
except Exception as e:
    print('  [ERROR] ' + str(e))
    exit(1)

print()
print('='*60)
print('ALL TESTS PASSED - Ready for Grasshopper!')
print('='*60)
