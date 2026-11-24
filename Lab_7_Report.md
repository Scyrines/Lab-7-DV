# TFB3133 / TEB3133 Data Visualization
# Lab 7: Interactive Map Visualization Examples using Streamlit — Laboratory Report

---

## 1. Executive Summary & Lab Objectives

- **Course:** TFB3133 / TEB3133 Data Visualization
- **Topic:** Lab 7 — Geospatial Data Visualization, Thematic Cartography, and Map Projections
- **Framework:** GeoPandas, Matplotlib, Streamlit, and Natural Earth Spatial Vector Data
- **Core Objectives:**
  1. **Map Cosmetics:** Applying cartographic styling (fill hues, ocean background contrast, boundary stroke widths).
  2. **Map Visual Hierarchy:** Directing audience focus using pre-attentive color highlighting to distinguish focal nations from contextual baselines.
  3. **Choropleth Maps:** Visualizing continuous spatial attributes (population density) using sequential colormaps and mathematical transformations ($\log_{1p}$).
  4. **Geo Projections:** Evaluating the mathematical trade-offs between Conformal, Equal-Area, and Compromise coordinate reference systems (CRS).

---

## 2. Dataset Setup & Preprocessing

The lab utilizes the **Natural Earth 1:110m Cultural Vector Dataset** (`ne_110m_admin_0_countries.shp`):
- **Features:** 177 administrative country polygons.
- **Attributes:** Country identifiers (`NAME`, `NAME_LONG`, `ISO_A3`) and population estimates (`POP_EST`).
- **Derived Metric — Population Density:**
  $$\text{Population Density} = \frac{\text{Population Estimate}}{\text{Polygon Geographic Area}}$$
- **CRS Initialization:** Loaded in WGS 84 (`EPSG:4326`) Geographic Coordinate System (degrees latitude and longitude).

---

## 3. Detailed Technical Analysis of the Four Map Modules

### 3.1 Module 1: Map Cosmetics (Styling & Aesthetics)
*Output Image: `map_cosmetics.png`*

- **Cartographic Implementation:**
  - Polygons styled with a clean `skyblue` fill, sharp `0.5` stroke black boundaries, and a subtle `lightgrey` facecolor representing oceanic water bodies.
- **Visualization Principles:**
  - Establishes foundational **Figure-Ground Separation** (Gestalt principle). The high contrast between continental landmasses and the oceanic background allows the human visual cortex to instantly delineate terrestrial borders without eye strain.

### 3.2 Module 2: Map Visual Hierarchy (Pre-attentive Highlighting)
*Output Image: `map_visual_hierarchy.png`*

- **Cartographic Implementation:**
  - Focal nations (`Brazil`, `India`, `China`, `Australia`, `South Africa`, `Russia`) highlighted in vivid `red`, while remaining global nations are rendered in neutral `skyblue`.
- **Visualization Principles:**
  - Implements **Visual Hierarchy** via the pre-attentive attribute of **color hue**.
  - Rather than requiring the viewer to perform a slow serial visual search across 177 labels, the contrasting red hue pops out in under 200 milliseconds, establishing an immediate cognitive focus group while preserving global geographic orientation.

### 3.3 Module 3: Choropleth Mapping & Logarithmic Transformation
*Output Image: `map_choropleth.png`*

- **Challenge — Extreme Distribution Skewness:**
  Global population density spans several orders of magnitude (from sparse regions in Greenland and Australia to dense urban agglomerations in Bangladesh and Singapore).
- **The Mathematical Solution ($\log_{1p}$ Scaling):**
  - **Raw Scale:** An unadjusted linear color ramp results in a virtually binary visualization: 95% of countries cluster in the lowest color bracket, while 2 or 3 high-density outliers consume the upper color tiers.
  - **Logarithmic Scale ($\text{np.log1p}$):**
    $$y = \ln(x + 1)$$
    Normalizes the distribution, spreading values evenly across the sequential colormap (`OrRd`, `Blues`, `YlGn`). This reveals subtle regional density gradients across Europe, the Americas, and Africa that were previously invisible.
- **Colormap Selection:** Utilizes perceptual sequential color ramps (`OrRd`) where color luminance correlates monotonically with increasing density.

### 3.4 Module 4: Geo Projections Comparison
*Output Image: `map_geo_projection.png`*

Projecting a 3-dimensional oblate spheroid onto a 2-dimensional planar surface inherently forces a trade-off between **area**, **shape**, **distance**, and **direction**:

| Projection Name | CRS Code | Projection Type | Distortion Characteristics & Suitability |
| :--- | :---: | :--- | :--- |
| **Plate Carrée** | `EPSG:4326` | Equirectangular (Cylindrical) | Maps latitude and longitude directly to Cartesian $X/Y$. Severe horizontal stretching at the poles; polar landmasses appear unnaturally flattened. |
| **Mercator** | `EPSG:3395` | Conformal (Cylindrical) | **Preserves local angles and shapes.** However, area distortion approaches infinity near the poles. Greenland appears equal in size to the entire continent of Africa, even though Africa is actually **14 times larger**! |
| **Robinson** | `ESRI:54030` | Compromise (Pseudocylindrical) | **Balances shape and area distortion.** Neither strictly conformal nor equal-area, but provides a visually intuitive, aesthetically pleasing depiction of global distributions. |
| **Mollweide** | `ESRI:54009` | Equal-Area (Pseudocylindrical) | **Preserves true relative landmass proportions.** Crucial for thematic maps showing land-based densities, though equatorial regions experience slight angular shear. |
| **Equal Earth** | `EPSG:8857` | Equal-Area (Pseudocylindrical) | Modern standard developed in 2018. Retains accurate proportional land areas with curved meridians that mimic natural Earth curvature without extreme shape warping. |

---

## 4. Summary of Deliverables

| Deliverable File | Format | Description |
| :--- | :--- | :--- |
| `app.py` | Python (Streamlit) | Complete, interactive application containing all four map modules with dynamic inputs. |
| `generate_maps.py` | Python Script | Script to render and export all four static map figures at 300 DPI. |
| `map_cosmetics.png` | PNG (300 DPI) | Styled map demonstration with customized fill, boundaries, and background. |
| `map_visual_hierarchy.png` | PNG (300 DPI) | Pre-attentive focal highlighting of selected nations. |
| `map_choropleth.png` | PNG (300 DPI) | Log-transformed population density choropleth map. |
| `map_geo_projection.png` | PNG (300 DPI) | Projected global choropleth map in Robinson projection. |
| `requirements.txt` | Text | Environment dependencies (`streamlit`, `geopandas`, `matplotlib`, `numpy`, `pyproj`). |
| `Lab_7_Report.md` | Markdown | Comprehensive laboratory documentation and cartographic reflection. |

---

## 5. Cartographic Reflection: Hierarchy, Scaling, and Projections (150–200 Words)

> Cartographic visualization demands a careful balance between spatial geometry and perceptual communication. Transforming geographic data into an effective thematic map requires deliberate choices in visual hierarchy, projection selection, and numeric scaling. When employing map cosmetics and visual hierarchy, selective color contrast—such as accentuating focal nations in vibrant crimson against desaturated backgrounds—leverages human pre-attentive processing, immediately isolating primary subjects from background context.
>
> Furthermore, quantitative spatial mapping relies heavily on appropriate mathematical transformations. Because demographic distributions follow power-law skews, unadjusted population density choropleths compress most nations into the lowest color bin, obscuring variance. Applying a logarithmic transformation normalizes this distribution, revealing regional density gradients across Europe and Asia. Finally, selecting an appropriate map projection is a critical ethical and analytical decision. While conformal projections like Mercator distort high-latitude landmasses—making polar regions appear disproportionately massive—equal-area projections such as Equal Earth and compromise projections like Robinson preserve geometric proportions, preventing spatial misinformation. Combining balanced projection geometry with logarithmic scaling and disciplined visual contrast ensures that thematic maps convey geographic insights with analytical rigor and perceptual honesty.

*(Word Count: 181 words)*
