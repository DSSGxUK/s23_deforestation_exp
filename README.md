# Deforestation risk prediction (EXPERIMENTS)

Experiments for the DSSGx-UK 2023 Deforestation project with UN-REDD:
- Data preprocessing:
    - [Downsample features](./MapBiomas_downsampling/) : process MapBiomas dataset over given time periods to get downsampled forest cover, deforestation and forest edge density maps
    - [Average values](./Averaging_script/) : script to run averaging over several tiles in paralel, while converting from 1/900m^2 to hectars.
- Creating JNR Risk maps:
    - [Create Forest Cover Change Map](./create_fcc_map/) : download, process and obtain maps of forest cover change (FCC) for the years 2000-2022 using Global Forest Change dataset
    - [Generate JNR Risk Map](./generate_jnr/) : obtain maps of the spatial risk of deforestation and forest degradation following the methodology of REDD+
- Additional experiments
    - [k-Means Clustering](./PRODES_clustering/) : perform k-Means clustering on the PRODES data to obtain the deforested regions. The deforested/ no forest regions have been segmented in a deep blue color whereas the remaining forest cover remains green
