# Kopieëer je GeoJSON hierheen of update het pad in Grasshopper component

# Voor nu: Primo Levihof data als voorbeeld
import json
import shutil

# Copy from main folder
try:
    shutil.copy(r'C:\Users\Thijs W\Desktop\Heron\GEOJSON_FOR_GITHUB.geojson',
                r'C:\Users\Thijs W\Desktop\Heron\FINAL_SOLUTION_COMPLETE\Primo_Levihof_buildings.geojson')
    print('GeoJSON copied!')
except:
    print('Manual copy: GEOJSON_FOR_GITHUB.geojson -> Primo_Levihof_buildings.geojson')
