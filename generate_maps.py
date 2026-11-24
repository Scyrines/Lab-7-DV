"""
Generate static map images for Lab 7:
1. map_cosmetics.png
2. map_visual_hierarchy.png
3. map_choropleth.png
4. map_geo_projection.png
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import os

out_dir = r"C:\Users\ASUS\Documents\Uni Docs\Data Viz\Lab 7"
shp_path = os.path.join(out_dir, "ne_110m_admin_0_countries", "ne_110m_admin_0_countries.shp")

gdf = gpd.read_file(shp_path)
country_col = "name" if "name" in gdf.columns else "NAME"
gdf["country_name"] = gdf[country_col]

if "pop_est" not in gdf.columns:
    if "POP_EST" in gdf.columns:
        gdf["pop_est"] = gdf["POP_EST"]
    else:
        np.random.seed(0)
        gdf["pop_est"] = np.random.randint(1e6, 1e9, size=len(gdf))

gdf = gdf[gdf.geometry.is_valid & ~gdf.geometry.is_empty].copy()
gdf["pop_density"] = gdf["pop_est"] / gdf["geometry"].area

# 1. Map Cosmetics
fig1, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
gdf.plot(ax=ax1, color="skyblue", edgecolor="black", linewidth=0.5)
ax1.set_title("Styled Map Example", fontsize=15, fontweight="bold", pad=12)
ax1.set_facecolor("lightgrey")
ax1.set_xticks([])
ax1.set_yticks([])
fig1.tight_layout()
fig1.savefig(os.path.join(out_dir, "map_cosmetics.png"), dpi=300, bbox_inches="tight")
plt.close(fig1)

# 2. Map Visual Hierarchy
highlighted = ["Brazil", "India", "China", "Australia", "South Africa", "Russia"]
gdf["color"] = gdf["country_name"].apply(lambda x: "red" if x in highlighted else "skyblue")
fig2, ax2 = plt.subplots(figsize=(10, 6), dpi=300)
gdf.plot(color=gdf["color"], edgecolor="black", linewidth=0.5, ax=ax2)
ax2.set_title("Map Visual Hierarchy with Selected Countries Highlighted in Red", fontsize=14, fontweight="bold", pad=12)
ax2.set_facecolor("#F5F5F5")
ax2.set_xticks([])
ax2.set_yticks([])
fig2.tight_layout()
fig2.savefig(os.path.join(out_dir, "map_visual_hierarchy.png"), dpi=300, bbox_inches="tight")
plt.close(fig2)

# 3. Choropleth Map (with Log Scale)
gdf["pop_density_log"] = np.log1p(gdf["pop_density"])
fig3, ax3 = plt.subplots(figsize=(10, 6), dpi=300)
gdf.plot(
    column="pop_density_log",
    cmap="OrRd",
    edgecolor="black",
    linewidth=0.4,
    legend=True,
    legend_kwds={"label": "Log(Population Density + 1)", "orientation": "horizontal", "shrink": 0.6, "pad": 0.05},
    ax=ax3
)
ax3.set_title("Population Density by Country (Color Scheme: OrRd)", fontsize=14, fontweight="bold", pad=12)
ax3.set_facecolor("#FAFAFA")
ax3.set_xticks([])
ax3.set_yticks([])
fig3.tight_layout()
fig3.savefig(os.path.join(out_dir, "map_choropleth.png"), dpi=300, bbox_inches="tight")
plt.close(fig3)

# 4. Geo Projection (Robinson)
gdf_rob = gdf.to_crs("ESRI:54030")
fig4, ax4 = plt.subplots(figsize=(10, 6), dpi=300)
gdf_rob.plot(
    column="pop_density_log",
    cmap="OrRd",
    edgecolor="black",
    linewidth=0.4,
    legend=True,
    legend_kwds={"label": "Log(Population Density + 1)", "orientation": "horizontal", "shrink": 0.6, "pad": 0.05},
    ax=ax4
)
ax4.set_title("Map in Robinson (ESRI:54030) Projection", fontsize=14, fontweight="bold", pad=12)
ax4.set_facecolor("#FAFAFA")
ax4.set_xticks([])
ax4.set_yticks([])
fig4.tight_layout()
fig4.savefig(os.path.join(out_dir, "map_geo_projection.png"), dpi=300, bbox_inches="tight")
plt.close(fig4)

print("All Lab 7 map images generated successfully!")
