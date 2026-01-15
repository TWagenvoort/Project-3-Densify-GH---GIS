# GRASSHOPPER SETUP HANDLEIDING - HERON 3D EXPORTER
# Volledige gids om je Grasshopper component in te stellen

## STAP 1: Voorbereiding

### Benodigde bestanden:
- `GRASSHOPPER_PYTHON_COMPONENT.txt` (Python code)
- `Primo_Levihof_buildings.geojson` (of je eigen GeoJSON)
- Feature Service URL (hieronder)

### Je Feature Service URL:
```
https://services9.arcgis.com/nqW2A97fCpeCbw6Z/arcgis/rest/services/Heron_test_final_3D/FeatureServer/0
```

---

## STAP 2: Grasshopper Python Component Aanmaken

### In Grasshopper:

1. **Open Grasshopper** (Type "Grasshopper" in Rhino command line)
2. **Double-click op canvas** → Zoek **"Python"** component
3. **Sleep de Python component** op je canvas

---

## STAP 3: Python Code Toevoegen

### In de Python component:

1. **Double-click** op de Python component (oranje icoon)
2. **Code editor opent** (rechts in de panel)
3. **Kopiëer ALLES** uit `GRASSHOPPER_PYTHON_COMPONENT.txt`
4. **Plak** in de code editor
5. **OK** klikken

---

## STAP 4: Inputs Aanmaken (9 parameters)

De Python component voegt automatisch 3 inputs toe. Check deze:

### Input 1: `geojson_path`
- **Type:** String (text)
- **Waarde:** Pad naar je GeoJSON bestand
- **Voorbeeld:** `C:\Users\Thijs W\Desktop\Heron\FINAL_SOLUTION_COMPLETE\Primo_Levihof_buildings.geojson`
- **Connectie:** Text panel of String component

### Input 2: `feature_service_url`
- **Type:** String (text)
- **Waarde:** Je Feature Service URL
- **Voorbeeld:** `https://services9.arcgis.com/nqW2A97fCpeCbw6Z/arcgis/rest/services/Heron_test_final_3D/FeatureServer/0`
- **Connectie:** Text panel of String component

### Input 3: `run_export`
- **Type:** Boolean (true/false)
- **Waarde:** `True` = upload, `False` = preview
- **Connectie:** Toggle/Boolean component

---

## STAP 5: Inputs Verbinden

1. **Right-click** op de Python component → **"Refresh Input/Output"**
2. **Voeg Text panels toe** (Params → Input → String):
   - 1 voor `geojson_path`
   - 1 voor `feature_service_url`
   - 1 voor `run_export` (of use Toggle)

3. **Verbind** elk panel naar de bijbehorende input

---

## STAP 6: Output Checker

1. **Right-click** op Python component → **"Preview"** aanzetten
2. Of **Panel component** verbinden aan de output
3. Dit toont de status/log

---

## STAP 7: Test Run

### Eerste test:

1. **Set `run_export` = False**
2. **Druk F5** of **Solution → Recompute**
3. **Check output:** Moet zeggen "[OK] Loaded: XX buildings"
4. Geen errors? Goed teken!

### Echte export:

1. **Set `run_export` = True**
2. **Recompute**
3. **Output:** "[OK] Uploaded: XX buildings"
4. **Check ArcGIS Scene Viewer** → Je gebouwen zijn daar!

---

## STAP 8: Scene Viewer Setup (3D Rendering)

### In ArcGIS Online Scene Viewer:

1. **Open je Feature Service item** → **"Open in Scene Viewer"**
2. **Layers panel** (links) → Zoek je laag
3. **Right-click** → **"Extrude"**
4. **Extrude polygons by:** Kies `height` field
5. **Height scale:** `1.0`
6. **Apply**
7. **Enable 3D mode** (button top-right)
8. **Rotate camera** → Zie je 3D gebouwen!

---

## TROUBLESHOOTING

### "Service not found"
→ Check: Feature Service is PUBLIC gemaakt?
→ Check: URL klopt?

### "Token Required"
→ Feature Service moet PUBLIC zijn
→ Ga naar item → Share → Everyone (public)

### "Field 'height' not found"
→ Voeg height field toe in ArcGIS:
   - Item → Data → Fields → Add Field
   - Name: `height`, Type: `Number`

### Niets verschijnt in Scene Viewer
→ Check: Extrusion setting correct?
→ Zoom naar Rotterdam (4.531, 51.873)
→ Rotate camera omhoog

### Grasshopper geeft error
→ Check Python syntax
→ Check Feature Service URL klopt
→ Test via `TEST_FEATURE_SERVICE.py`

---

## ITERATIEF DESIGN WORKFLOW

Dit is nu het power van Grasshopper + Scene Viewer:

1. **Rhino/Grasshopper**: Design je gebouwen
2. **Grasshopper Python**: Export naar ArcGIS
3. **ArcGIS Scene Viewer**: Instant 3D preview
4. **Iterate**: Aanpassingen → Export → Preview → Repeat!

Geen handwerk meer! Alles automatisch! 🚀

---

## NEXT STEPS

- Experimenteer met je eigen GeoJSON data
- Pas hoogte waarden aan → zie direct 3D effect
- Voeg meer data toe → Batch upload naar Scene Viewer
- Share met team via ArcGIS Online link

**Vragen?** Check de Python code comments in `GRASSHOPPER_PYTHON_COMPONENT.txt`

Veel plezier! 🎉
