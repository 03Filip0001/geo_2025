import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

print("\n\nPROJEKTNI ZADATAK 9 (GEO 1)\n---------------------------\n")

# Loading data from .shp file (adm1 - opstine Srbije)
try:
	opstine_gdf = gpd.read_file("data/SRB_adm2.shp")
	print("Shapefile uspešno učitan.")
except:
	raise Exception("Cannot load data")

# Kreiranje recnika sa opstinama i brojem stanovnika
podaci_stanovnistvo = {
    'opstina': ['Čačak', 'Valjevo', 'Novi Sad', 'Subotica', 'Niš', 'Kragujevac'],
    'stanovnistvo': [105612, 82169, 368967, 127756, 249816, 171186]
}
stanovnistvo_df = pd.DataFrame(podaci_stanovnistvo)
print("\nKreiran DataFrame sa brojem stanovnika:")
print(stanovnistvo_df)

# Spajanje geografskih podataka sa iz shape file sa demografskim podacima iz DataFrame
merged_gdf = opstine_gdf.merge(stanovnistvo_df, left_on='NAME_2', right_on='opstina')
print("\nSpojeni podaci (prvih 5 redova):")
print(merged_gdf[['NAME_2', 'stanovnistvo', 'geometry']].head())

# Transformacija u 2D mapu
merged_gdf_proj = merged_gdf.to_crs(epsg=32634)

# Racunanje povrsine opstina
povrsina_km2 = merged_gdf_proj.geometry.area / 1000000
merged_gdf['povrsina_km2'] = povrsina_km2

# Racunanje gustoce
merged_gdf['gustoca'] = merged_gdf['stanovnistvo'] / merged_gdf['povrsina_km2']
print("\nPodaci nakon dodavanja gustine naseljenosti:")
print(merged_gdf[['NAME_2', 'stanovnistvo', 'povrsina_km2', 'gustoca']].head())

# Menjanje broja stanovnika za opstinu
print("\nAžuriranje broja stanovnika za opštinu Čačak...")
merged_gdf.loc[merged_gdf['opstina'] == 'Čačak', 'stanovnistvo'] = 120000

# Ponovo racunaj gustinu stanovnistva
merged_gdf.loc[merged_gdf['opstina'] == 'Čačak', 'gustoca'] = \
    merged_gdf.loc[merged_gdf['opstina'] == 'Čačak', 'stanovnistvo'] / \
    merged_gdf.loc[merged_gdf['opstina'] == 'Čačak', 'povrsina_km2']

print("Novi podaci za Čačak:")
print(merged_gdf[merged_gdf['opstina'] == 'Čačak'][['opstina', 'stanovnistvo', 'gustoca']])

# Napravi 2 siva subplot-a
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
opstine_gdf.plot(ax=ax1, color='lightgray', edgecolor='white')
opstine_gdf.plot(ax=ax2, color='lightgray', edgecolor='white')

# Oboj opstine po broju stanovnika
merged_gdf.plot(column='stanovnistvo', ax=ax1, legend=True,
                cmap='viridis',
                legend_kwds={'label': "Broj stanovnika",
                             'orientation': "horizontal"})
ax1.set_title('Broj stanovnika po opštinama', fontdict={'fontsize': '16', 'fontweight': '3'})
ax1.set_axis_off()

# Oboj opstine po gustini naseljenosti
merged_gdf.plot(column='gustoca', ax=ax2, legend=True,
                cmap='plasma',
                legend_kwds={'label': "Gustina naseljenosti (st/km²)",
                             'orientation': "horizontal"})
ax2.set_title('Gustina naseljenosti po opštinama', fontdict={'fontsize': '16', 'fontweight': '3'})
ax2.set_axis_off()

# Prikazi plotove
plt.suptitle('Analiza stanovništva odabranih opština u Srbiji', fontsize=20)
plt.show()
