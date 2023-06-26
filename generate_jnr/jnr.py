# Imports
import os
import multiprocessing as mp
import pkg_resources

import numpy as np
import pandas as pd
from tabulate import tabulate

import riskmapjnr as rmj

# GDAL
os.environ["GDAL_CACHEMAX"] = "1024"


def main():

    # Specify the output directory
    out_dir = "/home/shared/dssg23-deforestation/jnr_outputs"
    rmj.make_dir(out_dir)

    # Specify the input file
    fcc_file = "/home/shared/dssg23-deforestation/fcc_map_america/amazon.tif"
    border_file = None

    # Plot the input file
    ofile = os.path.join(out_dir, "fcc123.png")
    fig_fcc123 = rmj.plot.fcc123(
        input_fcc_raster=fcc_file,
        maxpixels=1e8,
        output_file=ofile,
        borders=border_file,
        linewidth=0.2,
        figsize=(5, 4), dpi=800)

    ncpu = mp.cpu_count() - 2
    print(f"Number of CPUs to use: {ncpu}.")

    # Run the JNR algorithm with validation
    results_makemap = rmj.makemap(
        fcc_file=fcc_file,
        time_interval=[10, 10],
        output_dir=out_dir,
        clean=False,
        dist_bins=np.arange(0, 5000, step=30),
        win_sizes=np.arange(5, 200, 16),
        ncat=30,
        parallel=False,
        ncpu=ncpu,
        methods=["Equal Interval", "Equal Area"],
        csize=300,
        no_quantity_error=True,
        figsize=(6.4, 4.8),
        dpi=800,
        blk_rows=256,
        verbose=True)

    print(results_makemap)

    dist_thresh = results_makemap["dist_thresh"]
    print(f"The distance theshold is {dist_thresh} m.")

    ws_hat = results_makemap["ws_hat"]
    m_hat = results_makemap["m_hat"]
    print(f"The best moving window size is {ws_hat} pixels.")
    print(f"The best slicing algorithm is '{m_hat}'.")

    # Plot the risk map
    ifile = os.path.join(out_dir, f"endval/riskmap_ws{ws_hat}_{m_hat}_ev.tif")
    ofile = os.path.join(out_dir, f"endval/riskmap_ws{ws_hat}_{m_hat}_ev.png")
    riskmap_fig = rmj.plot.riskmap(
        input_risk_map=ifile,
        maxpixels=1e8,
        output_file=ofile,
        borders=border_file,
        legend=True,
        figsize=(5, 4), dpi=800, linewidth=0.2,)

if __name__ == "__main__":
    main()