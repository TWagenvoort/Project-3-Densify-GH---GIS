# HERON 3D EXPORTER FOR ARCGIS ONLINE

Export 3D Heron geometry data to ArcGIS Online Scene Viewer with automatic Scene Viewer visualization.

## ✅ QUICK START (5 minutes)

### 1. Prerequisites

**ArcGIS Online (Student Account):**
- ✅ One Feature Service created (e.g., "Grasshopper_3d_data")
- ✅ Point or Polygon geometry type
- ✅ Fields: `z_value` (Double), `type1` (String), `description` (String)

**Get your Feature Service URL from ArcGIS Online:**
```
https://services9.arcgis.com/[YOUR_ORG_ID]/arcgis/rest/services/[YOUR_SERVICE_NAME]/FeatureServer
```

### 2. Python Script Setup

```python
from HERON_3D_EXPORTER_FINAL import Heron3DExporter

# Your Feature Service URL
service_url = "https://services9.arcgis.com/.../FeatureServer"

# Initialize exporter
exporter = Heron3DExporter(service_url)

# Export GeoJSON to ArcGIS
success, message = exporter.export_3d("your_geometry.geojson")

print(message)
```

### 3. GeoJSON Format

Prepare your geometry as GeoJSON with height values:

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[4.4, 51.9], [4.5, 51.9], [4.5, 51.8], [4.4, 51.8], [4.4, 51.9]]]
      },
      "properties": {
        "name": "Building A",
        "type": "building",
        "height": 25
      }
    }
  ]
}
```

**Required properties:**
- `height` (number) - Height in meters for 3D visualization
- `name` (string) - Feature name
- `type` (string) - Feature type (building, street, etc.)

---

## 🏗️ HOW IT WORKS

### Point Layer Method (Recommended for Student Account)

If your Feature Service uses **Point geometry**:
1. ✅ Extracts coordinates from Polygon/LineString/Point geometries
2. ✅ Converts WGS84 → Web Mercator (ArcGIS standard)
3. ✅ Stores height as `z_value` attribute
4. ✅ Uploads as 3D point features
5. ✅ Scene Viewer visualizes with configurable markers

**Why Points?** Simpler, stable, supports all ArcGIS accounts

### Polygon Layer Method (Better visual quality)

If your Feature Service uses **Polygon geometry**:
1. ✅ Converts polygon rings to Web Mercator
2. ✅ Adds `height` field for auto-extrusion
3. ✅ Scene Viewer automatically extrudes 3D buildings
4. ✅ Professional 3D geometry appearance

**Why Polygons?** ArcGIS auto-extrudes = real 3D geometry

---

## 📊 FEATURE SERVICE SETUP

### ArcGIS Online (Web)

1. **Create Feature Service:**
   - Go to Content → New Item → Feature Layer
   - Create from file (GeoJSON) OR new empty service
   - Name: `Grasshopper_3d_data`

2. **Add Fields (if empty service):**
   | Field Name | Type | Example |
   |-----------|------|---------|
   | `z_value` | Double | 25 |
   | `type1` | String | building |
   | `description` | String | Building A |

3. **Get URL:**
   - Share → View Service Details
   - Copy REST Endpoint URL

4. **Enable Scene Viewer:**
   - Visualization → Scene Viewer
   - Configure marker size/color based on `z_value`

### Using ArcGIS Pro (Desktop)

Alternatively, create service in ArcGIS Pro and publish:

```
ArcGIS Pro → Create → New Project
→ Add your geometry shapefile/feature class
→ Share → Publish Feature Service
```

---

## 🐍 GRASSHOPPER INTEGRATION

### Step 1: Copy Script

Copy `HERON_3D_EXPORTER_FINAL.py` to a known location:
```
C:\Users\YOUR_USER\Documents\Heron\HERON_3D_EXPORTER_FINAL.py
```

### Step 2: Create Python Component

In Grasshopper:

```
Math → Python
```

### Step 3: Python Code

Paste in the Python component:

```python
import sys
sys.path.append(r'C:\Users\YOUR_USER\Documents\Heron')

from HERON_3D_EXPORTER_FINAL import Heron3DExporter

# Inputs:
# feature_service_url (string) - Your ArcGIS Feature Service URL
# geojson_path (string) - Path to GeoJSON file
# run_export (bool) - True to execute export

if run_export:
    try:
        exporter = Heron3DExporter(feature_service_url)
        success, message = exporter.export_3d(geojson_path)
        
        result = f"✅ SUCCESS!\n{message}" if success else f"❌ FAILED!\n{message}"
        
        # Show last 10 debug messages
        debug_info = "\n".join(exporter.debug_log[-10:])
        result += f"\n\nDebug:\n{debug_info}"
        
    except Exception as e:
        result = f"❌ ERROR: {str(e)}"
else:
    result = "Export disabled (set run_export = True)"
```

### Step 4: Connect Heron Export

In Grasshopper, connect to Heron:
- Export component → Save to GeoJSON file
- Use that file path in the Python component

---

## 🎨 SCENE VIEWER VISUALIZATION

### Configure Point Layer Visualization

1. **Open Feature Service in ArcGIS Online**
2. **Visualize → Scene Viewer**
3. **Style Options:**
   - **Point Size:** Scale by `z_value` (height)
   - **Point Color:** Categorical by `type1` (building, street, etc.)
   - **Label:** Show `description`

Example:
```
Points: 5-50px size, scale by z_value
Colors: building=red, street=gray, park=green
```

### Configure Polygon Layer Visualization

1. **Open Feature Service in ArcGIS Online**
2. **Visualize → Scene Viewer**
3. **Auto-Extrusion (Automatic):**
   - ArcGIS detects `height` field
   - Automatically extrudes to that height
   - No additional configuration needed

---

## ⚙️ STUDENT ACCOUNT SPECIFICS

**ArcGIS Online (Free/Educational Account):**
- ✅ 5 Feature Services maximum
- ✅ 1 GB total storage
- ✅ All Scene Viewer features included
- ✅ REST API access enabled
- ⚠️ Some service limits apply

**Recommendations:**
- Use Point layers for efficiency (smaller storage)
- Combine multiple geometries into single service
- Export monthly, not continuously
- Monitor storage in Account Settings

---

## 🐛 TROUBLESHOOTING

### Issue: "HTTP 504 Gateway Timeout"

**Cause:** ArcGIS service temporarily overloaded

**Solution:**
- Wait 30 seconds and retry
- Reduce batch size in script
- Check if service is public/shared

### Issue: "0 features uploaded"

**Cause:** Geometry type mismatch (e.g., Point data to Polygon service)

**Solution:**
- Check Feature Service geometry type: `https://[service_url]/0?f=json`
- Look at `"geometryType"` field
- Match GeoJSON type to service type

### Issue: "Incorrect geometry type error"

**Cause:** Uploading wrong geometry type to service

**Solution:**
```
Point service: extract 1 coordinate per feature
Polygon service: use polygon rings
```

### Issue: "Features uploaded but not visible in Scene Viewer"

**Cause:** Missing visualization configuration

**Solution:**
- Open Scene Viewer
- Check "Style" settings
- Ensure layer is visible (not hidden)
- For points: configure symbol size/color
- For polygons: check extrusion height field

### Debug Mode

Get detailed logs:

```python
exporter = Heron3DExporter(service_url)
success, message = exporter.export_3d(geojson_path)

# Print all debug messages
for log_line in exporter.debug_log:
    print(log_line)
```

---

## 📈 OPTIMIZATION TIPS

### Large Datasets (1000+ features)

1. **Reduce batch size:**
   ```python
   # In HERON_3D_EXPORTER_FINAL.py, line ~180
   batch_size = 250  # Instead of 500
   ```

2. **Simplify geometry:**
   - Use Douglas-Peucker algorithm to reduce coordinates
   - Combine small features into groups

3. **Use Point geometry:**
   - Points are faster to upload than polygons
   - Suitable for 3D visualization

### Performance Monitoring

```python
import time

start = time.time()
success, message = exporter.export_3d(geojson_path)
elapsed = time.time() - start

print(f"Upload time: {elapsed:.1f} seconds")
```

---

## 📋 TESTED CONFIGURATIONS

| Layer Type | Geometry | Max Features | Status |
|-----------|----------|-------------|--------|
| Point | Point | 10,000+ | ✅ Tested |
| Point | Polygon* | 5,000+ | ✅ Tested |
| Polygon | Polygon | 1,000+ | ✅ Tested |

*Extracts centroid from polygon

---

## 🔗 RESOURCES

- [ArcGIS REST API Docs](https://developers.arcgis.com/rest/)
- [Feature Service Documentation](https://developers.arcgis.com/documentation/rest-apis/services/feature-service/)
- [Scene Viewer Guide](https://doc.arcgis.com/en/arcgis-online/reference/scene-viewer.htm)
- [Web Mercator Information](https://en.wikipedia.org/wiki/Web_Mercator_projection)

---

## 📞 SUPPORT

**Common Questions:**

**Q: Can I use this without Grasshopper?**
A: Yes! Run the script standalone or in any Python environment.

**Q: Does this work with hosted layers?**
A: Yes, any ArcGIS Online Feature Service.

**Q: What's the maximum upload size?**
A: ~50MB per request, handled automatically in batches.

**Q: Can I update existing features?**
A: Yes, modify `delete_existing_features()` method.

**Q: Does this support 3D shapefiles directly?**
A: No, convert to GeoJSON first using QGIS, Ogre, or similar.

---

**Version:** 1.0  
**Last Updated:** January 2025  
**For:** Grasshopper + Rhino 8 + ArcGIS Online

