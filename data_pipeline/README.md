<h1>Data Pipeline</h1>
<p>The data pipeline automates a series of tasks related to processing and analysis of geographical and environmental data.</p>
<h2>Directory Structure</h2>
<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">.
├── config.yml                      <span class="hljs-comment"># Configuration file containing settings and paths</span>
├── <span class="hljs-built_in">jobs</span>                            <span class="hljs-comment"># Scripts for various jobs to be executed</span>
│   ├── *.exp                       <span class="hljs-comment"># Job scripts (SLURM/BASH executable)</span>
│   └── README.md
├── launcher.sh                     <span class="hljs-comment"># Main script to launch the jobs</span>
├── scripts                         <span class="hljs-comment"># Python scripts that perform the core functionalities of the pipeline</span>
└── utility                         <span class="hljs-comment"># Additional utilities and helper functions</span>
</code></div></div></pre>
<h2>Setup</h2>
<p>Before running the pipeline:</p>
<ol>
    <li>Ensure that all dependencies specified in the <code>config.yml</code> are installed and available.</li>
    <li>Set the appropriate paths in the <code>config.yml</code> file.</li>
    <li>Check that the necessary data is in place, as specified in the <code>config.yml</code>.</li>
</ol>
<h2>Usage</h2>
<p>To execute the pipeline, you can use the <code>launcher.sh</code> script. It accepts a mode, either "SLURM" or "BASH", to dictate how jobs should be executed.</p>
<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">./launcher.sh &lt;MODE&gt;
</code></div></div></pre>
<p>Replace <code>&lt;MODE&gt;</code> with either <code>SLURM</code> if you're running on a cluster with SLURM workload manager or <code>BASH</code> to execute the scripts directly.</p>
<p>Example:</p>
<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">./launcher.sh SLURM
</code></div></div></pre>
<p><strong>Note:</strong> When using the <code>SLURM</code> mode, the launcher will submit jobs using the <code>sbatch</code> command and monitor their completion before moving to the next job. In <code>BASH</code> mode, the jobs are executed directly.</p>
<h2>Jobs</h2>
<p>The pipeline consists of several jobs, each dedicated to a specific processing or analysis task. Jobs are located in the <code>jobs</code> directory and can be executed individually or as part of the pipeline using the <code>launcher.sh</code> script.</p>
<p>The jobs included are:</p>
<ul>
    <li><strong>standardize_tifs</strong>: Standardizes TIF files for processing.</li>
    <li><strong>proximity</strong>: Calculates the proximity for the data.</li>
    <li><strong>calculate_global_stats</strong>: Calculates global statistics for the dataset.</li>
    <li><strong>stack</strong>: Stacks layers of data.</li>
    <li><strong>sample_deforestation</strong>: Samples deforestation tiles.</li>
    <li><strong>cut_tiles_distributed</strong>: Cuts tiles, distributing the computantions across different nodes..</li>
</ul>
<h2>Customizing the Pipeline</h2>
<p>You can customize the pipeline by:</p>
<ol>
    <li>Modifying the <code>config.yml</code> for different parameters or paths.</li>
    <li>Adding or removing job scripts in the <code>jobs</code> directory.</li>
    <li>Updating the <code>launcher.sh</code> script to include/exclude jobs as needed.</li>
</ol>
<h2>Configuration Details: <code>config.yml</code></h2>
<p>This configuration file serves as the central settings repository for the data pipeline.</p>
<h3>GLOBAL Settings:</h3>
<ul>
    <li>
        <p><strong>RESOLUTION</strong>: The spatial resolution of the data, in meters. Set to <code>30</code> for 30-meter resolution.</p>
    </li>
    <li>
        <p><strong>WINDOW_SIZE</strong>: The dimension size for splitting datasets into smaller windows. For instance, a window size of <code>256</code> would create 256x256 pixel windows.</p>
    </li>
    <li>
        <p><strong>DST_CRS</strong>: The Coordinate Reference System to be used for output datasets, specified as an EPSG code.</p>
    </li>
    <li>
        <p><strong>TARGET_EXTENT</strong>: The geographical extent for output datasets. This specifies the bounding box for processing data.</p>
    </li>
    <li>
        <p><strong>TARGET_VARIABLE</strong>: The variable of interest in the datasets.</p>
    </li>
    <li>
        <p><strong>MODULES</strong>: Lists the software modules required for the pipeline, which will be loaded before processing.</p>
    </li>
    <li>
        <p><strong>WORK_DIR</strong>: Specifies the main working directory. This is where all processing will take place.</p>
    </li>
    <li>
        <p><strong>PYTHON_ENV</strong>: Path to the Python virtual environment to be used.</p>
    </li>
    <li>
        <p><strong>RAW_DATA</strong>: Directory containing the raw input data.</p>
    </li>
    <li>
        <p><strong>DATA_DIR</strong>: Directory where processed data will be stored.</p>
    </li>
    <li>
        <p><strong>SHAPEFILE</strong>: The path to a shapefile used in the processing, in this case, specifying the Amazon biome borders.</p>
    </li>
    <li>
        <p><strong>LOG_DIR</strong>: Directory where log files will be stored. It helps in tracking the progress and debugging if needed.</p>
    </li>
</ul>
<h3>SLURM Settings:</h3>
<ul>
    <li><strong>DEFAULT</strong>: Contains default settings for running tasks on a SLURM cluster.<ul>
            <li><strong>NODES</strong>: The number of nodes to be used for SLURM jobs.</li>
            <li><strong>NTASKS</strong>: Number of tasks to run.</li>
            <li><strong>CPUS_PER_TASK</strong>: Specifies how many CPUs will be used per task.</li>
            <li><strong>RUN_TIME</strong>: Maximum allowed runtime for the SLURM job.</li>
            <li><strong>MEM_PER_CPU</strong>: Memory allocated per CPU.</li>
        </ul>
    </li>
</ul>
<h3>Jobs:</h3>
<p>Detailed settings and paths for each of the tasks/jobs in the pipeline:</p>
<ul>
    <li><strong>standardize_tifs</strong>: This job processes raw data to standardize TIF files.</li>
    <li><strong>stack_xtest</strong>: Stacks different layers of data together.</li>
    <li><strong>sample_deforestation</strong>: Samples tiles from areas that have undergone deforestation.</li>
    <li><strong>proximity</strong>: Calculates proximity measurements for specified features.</li>
    <li><strong>cut_tiles_distributed</strong>: Splits larger datasets into smaller tiles, distributed across resources.</li>
    <li><strong>clip_tifs</strong>: Clips TIF files based on a specified shape or boundary.</li>
    <li><strong>calculate_global_stats</strong>: Computes global statistics for the datasets over the years specified.</li>
</ul>
<p>Each job section contains specific settings such as log file locations, input data paths, and output directories.</p>
<hr>
<p>To ensure that the pipeline runs smoothly, it is imperative to periodically review and update the <code>config.yml</code> file, especially when introducing new datasets or changing directory structures.</p>
</div>