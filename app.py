"""
TFB3133/TEB3133 Data Visualization
LAB 7: Interactive Map Visualization Examples using Streamlit

Modules:
1. Map Cosmetics
2. Map Visual Hierarchy
3. Choropleth Map
4. Geo Projection
"""

import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import os

# ---------------------------------------------------------
# Page Setup & Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Lab 7 | Interactive Map Visualizations",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Load Natural Earth Dataset
# ---------------------------------------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    shp_path = os.path.join(base_dir, "ne_110m_admin_0_countries", "ne_110m_admin_0_countries.shp")
    
    if not os.path.exists(shp_path):
        st.error(f"Shapefile not found at {shp_path}. Please verify dataset installation.")
        st.stop()
        
    gdf = gpd.read_file(shp_path)
    
    # Standardize column names
    country_col = "name" if "name" in gdf.columns else "NAME"
    gdf["country_name"] = gdf[country_col]
    
    # Standardize pop_est column
    if "pop_est" not in gdf.columns:
        if "POP_EST" in gdf.columns:
            gdf["pop_est"] = gdf["POP_EST"]
        else:
            np.random.seed(0)
            gdf["pop_est"] = np.random.randint(1e6, 1e9, size=len(gdf))
            
    # Calculate population density (people per degree area)
    # Filter valid geometries
    gdf = gdf[gdf.geometry.is_valid & ~gdf.geometry.is_empty].copy()
    gdf["pop_density"] = gdf["pop_est"] / gdf["geometry"].area
    return gdf

gdf = load_data()

# ---------------------------------------------------------
# Sidebar Controls & Map Type Selection
# ---------------------------------------------------------
st.sidebar.title("Lab 7: Map Controls")
st.sidebar.markdown(
    """
    **Course Reference:**  
    TFB3133/TEB3133 Data Visualization  
    *Lab 7: Geographic Data & Map Projections*
    """
)

st.title("Interactive Map Visualization Examples")
st.markdown("Explore cartographic aesthetics, visual hierarchy, choropleth density mapping, and global map projections.")

st.sidebar.header("Choose a Map Type")
map_type = st.sidebar.radio(
    "Select Map Type:",
    [
        "Map Cosmetics",
        "Map Visual Hierarchy",
        "Choropleth Map",
        "Geo Projection"
    ]
)

# Supported Projection dictionary
projection_options = {
    "Robinson (ESRI:54030) - Compromise": "ESRI:54030",
    "Equal Earth (EPSG:8857) - Equal Area": "EPSG:8857",
    "Mollweide (ESRI:54009) - Pseudocylindrical": "ESRI:54009",
    "Plate Carrée (EPSG:4326) - Equirectangular": "EPSG:4326",
    "Eckert IV (ESRI:54012) - Equal Area": "ESRI:54012",
    "Mercator (EPSG:3395) - Conformal": "EPSG:3395"
}

# ---------------------------------------------------------
# 1. Map Cosmetics Example
# ---------------------------------------------------------
if map_type == "Map Cosmetics":
    st.subheader("1. Map Cosmetics: Styling & Aesthetics")
    st.markdown(
        "Demonstrates basic map style customization using a sky-blue fill, dark boundary lines, "
        "and a soft neutral background representing oceans."
    )
    
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        land_color = st.color_picker("Land Color:", "#87CEEB")
    with col_ctrl2:
        ocean_color = st.color_picker("Ocean Background Color:", "#D3D3D3")
        
    fig, ax = plt.subplots(figsize=(11, 6), dpi=150)
    gdf.plot(ax=ax, color=land_color, edgecolor="black", linewidth=0.5)
    ax.set_title("Styled Map Example", fontsize=15, fontweight="bold", pad=12)
    ax.set_facecolor(ocean_color)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#BDBDBD")
        
    fig.tight_layout()
    st.pyplot(fig, clear_figure=False)
    st.caption("A basic map style customization example with customizable fill color and light background.")

# ---------------------------------------------------------
# 2. Map Visual Hierarchy Example
# ---------------------------------------------------------
elif map_type == "Map Visual Hierarchy":
    st.subheader("2. Map Visual Hierarchy: Highlighting Focal Regions")
    st.markdown(
        "Employs pre-attentive color contrast to establish visual hierarchy. Selected focal nations "
        "are rendered in vivid red, while contextual nations remain neutral."
    )
    
    country_col = "country_name"
    available_countries = sorted(gdf[country_col].dropna().unique().tolist())
    
    highlighted_countries = st.multiselect(
        "Select countries to highlight in red:",
        options=available_countries,
        default=["Brazil", "India", "China", "Australia", "South Africa", "Russia"]
    )
    
    gdf_hier = gdf.copy()
    gdf_hier["color"] = gdf_hier[country_col].apply(
        lambda x: "red" if x in highlighted_countries else "skyblue"
    )
    
    m1, m2 = st.columns([1, 3])
    with m1:
        st.metric("Total Countries Highlighted", len(highlighted_countries))
    with m2:
        st.write(f"**Highlighted Selection:** {', '.join(highlighted_countries) if highlighted_countries else 'None'}")
        
    fig, ax = plt.subplots(figsize=(11, 6), dpi=150)
    gdf_hier.plot(color=gdf_hier["color"], edgecolor="black", linewidth=0.5, ax=ax)
    ax.set_title("Map Visual Hierarchy with Selected Countries Highlighted in Red", fontsize=14, fontweight="bold", pad=12)
    ax.set_facecolor("#F5F5F5")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#BDBDBD")
        
    fig.tight_layout()
    st.pyplot(fig, clear_figure=False)
    st.caption("Visual hierarchy guides the viewer's immediate perception toward prioritized countries.")

# ---------------------------------------------------------
# 3. Choropleth Map Example
# ---------------------------------------------------------
elif map_type == "Choropleth Map":
    st.subheader("3. Choropleth Map: Continuous Density Distribution")
    st.markdown(
        "Choropleth mapping visualizes quantitative attributes across geographic administrative units. "
        "Log transformation normalizes extreme population skews."
    )
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        color_choice = st.selectbox(
            "Choose Color Scheme:",
            ["OrRd", "YlGn", "Blues", "Purples", "Greens"],
            index=0
        )
    with col_c2:
        use_log_scale = st.checkbox("Use Log Transformation", value=True)
        
    gdf_choro = gdf.copy()
    gdf_choro["plot_metric"] = gdf_choro["pop_density"]
    
    if use_log_scale:
        gdf_choro["plot_metric"] = np.log1p(gdf_choro["pop_density"])
        legend_label = "Log(Population Density + 1)"
    else:
        legend_label = "Raw Population Density (people / degree²)"
        
    fig, ax = plt.subplots(figsize=(11, 6), dpi=150)
    gdf_choro.plot(
        column="plot_metric",
        cmap=color_choice,
        edgecolor="black",
        linewidth=0.4,
        legend=True,
        legend_kwds={"label": legend_label, "orientation": "horizontal", "shrink": 0.6, "pad": 0.05},
        ax=ax
    )
    ax.set_title(f"Population Density by Country (Color Scheme: {color_choice})", fontsize=14, fontweight="bold", pad=12)
    ax.set_facecolor("#FAFAFA")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#BDBDBD")
        
    fig.tight_layout()
    st.pyplot(fig, clear_figure=False)
    st.caption("Interactive choropleth map with color scheme selection and logarithmic skew normalization.")

# ---------------------------------------------------------
# 4. Geo Projection Example
# ---------------------------------------------------------
elif map_type == "Geo Projection":
    st.subheader("4. Geo Projections: Transforming Spatial Surfaces")
    st.markdown(
        "Explore how different coordinate reference systems (CRS) project the 3D spherical Earth "
        "onto a 2D plane, altering shape, area, and scale."
    )
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        proj_choice = st.selectbox("Select a Projection:", list(projection_options.keys()))
    with col_p2:
        color_choice = st.selectbox("Choose Color Scheme:", ["OrRd", "YlGn", "Blues", "Purples", "Greens"], index=0)
    with col_p3:
        use_log_scale = st.checkbox("Use Log Transformation for Population Density", value=True)
        
    gdf_proj_base = gdf.copy()
    if use_log_scale:
        gdf_proj_base["plot_metric"] = np.log1p(gdf_proj_base["pop_density"])
        legend_label = "Log(Population Density + 1)"
    else:
        gdf_proj_base["plot_metric"] = gdf_proj_base["pop_density"]
        legend_label = "Raw Population Density"
        
    target_crs = projection_options[proj_choice]
    
    # Handle Mercator extreme latitude bounds if chosen
    if "Mercator" in proj_choice:
        gdf_proj_base = gdf_proj_base[(gdf_proj_base.geometry.bounds.miny > -80) & (gdf_proj_base.geometry.bounds.maxy < 84)].copy()
        
    try:
        gdf_proj = gdf_proj_base.to_crs(target_crs)
    except Exception as e:
        st.warning(f"Projection error: {e}. Falling back to default CRS.")
        gdf_proj = gdf_proj_base
        
    fig, ax = plt.subplots(figsize=(11, 6), dpi=150)
    gdf_proj.plot(
        column="plot_metric",
        cmap=color_choice,
        edgecolor="black",
        linewidth=0.4,
        legend=True,
        legend_kwds={"label": legend_label, "orientation": "horizontal", "shrink": 0.6, "pad": 0.05},
        ax=ax
    )
    ax.set_title(f"Map in {proj_choice.split('-')[0].strip()} Projection", fontsize=14, fontweight="bold", pad=12)
    ax.set_facecolor("#FAFAFA")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#E0E0E0")
        
    fig.tight_layout()
    st.pyplot(fig, clear_figure=False)
    st.caption(f"Projected GeoDataFrame transformed using CRS: {target_crs}.")
