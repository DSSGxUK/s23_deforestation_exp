# Deforestation risk prediction (EXPERIMENTS)

Experiments for the DSSGx-UK 2023 Deforestation project with UN-REDD:

- [Creating and generating predictions using JNR Risk maps](./JNR/):
    - [1. Create Input](./JNR/1.%20Create%20Input/) : Process and obtain maps of forest cover change (FCC) for the required years
    - [2. Run JNR](./JNR/2.%20Run%20JNR/) : Run the JNR algorithm to obtain the risk maps
    - [3. Create Output](./JNR/3.%20Create%20Output/) : Create the deforestation prediction and ground truth maps using the risk maps
- Additional experiments
    - [k-Means Clustering](./PRODES_clustering/) : perform k-Means clustering on the PRODES data to obtain the deforested regions. The deforested/ no forest regions have been segmented in a deep blue color whereas the remaining forest cover remains green
