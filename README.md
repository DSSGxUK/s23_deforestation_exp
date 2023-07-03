# Deforestation risk prediction (EXPERIMENTS)

Experiments for the DSSGx-UK 2023 Deforestation project with UN-REDD:

- Creating JNR Risk maps:
    - [Create Forest Cover Change Map](./create_fcc_map/README.md) : download, process and obtain maps of forest cover change (FCC) for the years 2000-2022 using Global Forest Change dataset
    - [Generate JNR Risk Map](./generate_jnr_risk_map/README.md) : obtain maps of the spatial risk of deforestation and forest degradation following the methodology of REDD+
- Additional experiments
    - [k-Means Clustering](./PRODES_clustering/terrabrasilis_k-means.png) : perform k-Means clustering on the PRODES data to obtain the deforested regions. The deforested/ no forest regions have been segmented in a deep blue color whereas the remaining forest cover remains green
