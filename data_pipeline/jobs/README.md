<div class="markdown prose w-full break-words dark:prose-invert light">
    <hr>
    <h1><strong>README for the jobs folder of the data_pipeline module</strong></h1>
    <p>Welcome to the <code>jobs</code> folder of the <code>data_pipeline</code> module. 
       This folder contains various job scripts primarily intended for SLURM execution, aiding in diverse data processing tasks for the <code>dssg23-deforestation</code> project.
    </p>
    <h2><strong>Script Descriptions</strong>:</h2>
    <h3><strong>1. average_tif.exp</strong></h3>
    <ul>
       <li><strong>Purpose</strong>: Calculates the average value for a specified list of TIFF files.</li>
       <li><strong>Functionality</strong>: Computes the average value, specifically excluding the '-1' values during the calculation.</li>
       <li><strong>Key Parameters</strong>: List of files, exclusion criteria.</li>
    </ul>
    <h3><strong>2. calculate_global_stats.exp</strong></h3>
    <ul>
       <li><strong>Purpose</strong>: Computes statistical values for TIFF files.</li>
       <li><strong>Functionality</strong>: Launches a Python script to calculate mean, standard deviation, minimum, and maximum for the TIFF files, storing the results to later be utilized by the <code>cut_tiles</code> scripts and for standardization.</li>
       <li><strong>Key Parameters</strong>: Output directory, list of TIFF files.</li>
    </ul>
    <h3><strong>3. clip_tifs.exp</strong></h3>
    <ul>
       <li><strong>Purpose</strong>: Clips TIFF files based on a shapefile.</li>
       <li><strong>Functionality</strong>: Uses a specified shapefile to determine the boundaries for clipping the TIFF files.</li>
       <li><strong>Key Parameters</strong>: Shapefile path, list of TIFF files.</li>
    </ul>
    <h3><strong>4-5. cut_tiles.exp and cut_tiles_distributed.sh</strong></h3>
    <ul>
       <li><strong>Purpose</strong>: Segments and normalizes TIFF files.</li>
       <li><strong>Functionality</strong>: Slices the TIFF files and applies a normalization function to each band. For specifics regarding the normalization, refer to the associated Python script.</li>
       <li><strong>Key Parameters</strong>: List of TIFF files, normalization details.</li>
    </ul>
    <h3><strong>6. proximity.exp</strong></h3>
    <ul>
       <li><strong>Purpose</strong>: Produces proximity maps for TIFF files.</li>
       <li><strong>Functionality</strong>: Creates proximity maps for a given set of TIFF files.</li>
       <li><strong>Key Parameters</strong>: Source and destination directories.</li>
    </ul>
    <h3><strong>7. stack.exp scripts</strong></h3>
    <ul>
       <li><strong>Purpose</strong>: Aggregates multiple TIFF files.</li>
       <li><strong>Functionality</strong>: Merges multiple TIFF files into one VRT and then converts that VRT into a GeoTIFF, maintaining a consistent resolution.</li>
       <li><strong>Key Parameters</strong>: SLURM settings, paths, and filenames.</li>
    </ul>
    <h3><strong>8. standardize_tifs.exp</strong></h3>
    <ul>
       <li><strong>Purpose</strong>: Standardizes geospatial map data.</li>
       <li><strong>Functionality</strong>: Merges TIFF files, reprojects them, and clips them to a designated shapefile. It expects the root directory to have folders formatted as "feature_{year}" with associated TIFFs or "feature_static" with associated TIFFs. The script then categorizes these features as either Dynamic or Static accordingly.</li>
       <li><strong>Key Parameters</strong>: Root directory, shapefile, feature categorization.</li>
    </ul>
    <hr>
    <p>To utilize these scripts, you can either submit them through a SLURM scheduler or run them directly in a bash-compatible terminal, based on your setup.</p>
 </div>