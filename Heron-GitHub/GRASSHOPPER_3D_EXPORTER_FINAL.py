# HERON 3D EXPORTER - FINAL PRODUCTION VERSION
# Direct upload naar ArcGIS Online 3D Feature Service
# Geschikt voor Grasshopper Python component
# Versie: 3.0 - Production Ready

import sys
import os
import json
import urllib.request
import urllib.parse

class Heron3DExporter:
    """Upload GeoJSON naar ArcGIS Online 3D Feature Service"""
    
    def __init__(self, feature_service_url):
        self.base_url = feature_service_url.rstrip('/')
        if not self.base_url.endswith('/0'):
            self.base_url = self.base_url + '/0'
        self.add_features_url = self.base_url + '/addFeatures'
    
    def export_3d(self, geojson_data):
        """
        Upload 3D buildings naar ArcGIS Feature Service
        
        Args:
            geojson_data: GeoJSON FeatureCollection dict
            
        Returns:
            (success: bool, message: str)
        """
        
        try:
            features = geojson_data.get('features', [])
            if not features:
                return False, 'No features in GeoJSON'
            
            # Upload in batches
            batch_size = 100
            total_added = 0
            total_failed = 0
            
            for batch_num in range(0, len(features), batch_size):
                batch_end = min(batch_num + batch_size, len(features))
                batch_features = features[batch_num:batch_end]
                
                arcgis_features = []
                for idx, feat in enumerate(batch_features):
                    try:
                        coords = feat['geometry']['coordinates'][0]
                        rings = [coords]
                        
                        height = feat['properties'].get('height', 0.0)
                        if not height:
                            height = 0.0
                        height = float(height)
                        
                        arcgis_feat = {
                            'geometry': {'rings': rings},
                            'attributes': {
                                'OBJECTID': batch_num + idx + 1,
                                'height': height,
                                'name': feat['properties'].get('name', '')
                            }
                        }
                        arcgis_features.append(arcgis_feat)
                    except Exception as e:
                        total_failed += 1
                        continue
                
                # Upload batch
                data = {
                    'features': json.dumps(arcgis_features),
                    'f': 'json'
                }
                params = urllib.parse.urlencode(data).encode('utf-8')
                
                try:
                    req = urllib.request.Request(self.add_features_url, data=params)
                    response = urllib.request.urlopen(req, timeout=30)
                    result = json.loads(response.read())
                    
                    if 'addResults' in result:
                        added = sum(1 for r in result['addResults'] if r.get('success'))
                        total_added += added
                        failed = len([r for r in result['addResults'] if not r.get('success')])
                        total_failed += failed
                except Exception as e:
                    total_failed += len(arcgis_features)
            
            message = 'Exported ' + str(total_added) + ' buildings successfully'
            if total_failed > 0:
                message += ' (' + str(total_failed) + ' failed)'
            
            return True, message
        
        except Exception as e:
            return False, 'Error: ' + str(e)


# GRASSHOPPER COMPONENT CODE
# Plak dit in Grasshopper Python component

def main():
    """Grasshopper entry point"""
    
    # Set this to your Python environment path
    SCRIPT_FOLDER = r'C:\Users\Thijs W\Desktop\Heron\FINAL_SOLUTION_COMPLETE'
    
    if SCRIPT_FOLDER not in sys.path:
        sys.path.insert(0, SCRIPT_FOLDER)
    
    # Set defaults if inputs not connected
    if 'geojson_path' not in dir() or geojson_path is None:
        geojson_path = ''
    if 'feature_service_url' not in dir() or feature_service_url is None:
        feature_service_url = ''
    if 'run_export' not in dir() or run_export is None:
        run_export = False
    
    result = ''
    
    # Validate
    if not geojson_path:
        result = 'ERROR: geojson_path input missing'
    elif not feature_service_url:
        result = 'ERROR: feature_service_url input missing'
    elif not os.path.exists(geojson_path):
        result = 'ERROR: File not found: ' + geojson_path
    elif not run_export:
        result = 'INFO: Export paused (set run_export = True)'
    else:
        try:
            # Load GeoJSON
            with open(geojson_path, 'r', encoding='utf-8') as f:
                geojson_data = json.load(f)
            
            num_features = len(geojson_data.get('features', []))
            result += '[OK] Loaded: ' + os.path.basename(geojson_path) + ' (' + str(num_features) + ' buildings)\n'
            
            # Export
            exporter = Heron3DExporter(feature_service_url)
            success, message = exporter.export_3d(geojson_data)
            
            if success:
                result += '[OK] ' + message + '\n'
                result += '[OK] Check ArcGIS Scene Viewer in 3D mode!'
            else:
                result += '[ERROR] ' + message
        
        except Exception as e:
            result = '[ERROR] ' + str(e)
    
    return result

if __name__ == '__main__':
    print(main())
