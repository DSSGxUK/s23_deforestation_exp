#!/bin/bash

JOBS_DIR="./jobs"
MODE="$1"  # Accept the mode as the first argument (SLURM or BASH)

if [ "$MODE" != "SLURM" ] && [ "$MODE" != "BASH" ]; then
    echo "Invalid mode. Please use either SLURM or BASH."
    exit 1
fi

# Function to check if the job is complete (for SLURM mode)
check_job_complete_slurm() {
    local jobname=$1
    while true; do
        if [ -z "$(squeue | grep $jobname)" ]; then
            break
        else
            sleep 60  # Wait for 60 seconds before checking again
        fi
    done
}

# Execute the job based on the mode
execute_job() {
    local jobscript=$1
    if [ "$MODE" == "SLURM" ]; then
        sbatch "$jobscript"
    else
        bash "$jobscript"
    fi
}

# Run jobs based on the mode
execute_job $JOBS_DIR/standardize_tifs.exp
if [ "$MODE" == "SLURM" ]; then check_job_complete_slurm "standardize_tifs"; fi

execute_job $JOBS_DIR/proximity.exp
if [ "$MODE" == "SLURM" ]; then check_job_complete_slurm "proximity"; fi

execute_job $JOBS_DIR/calculate_global_stats.exp
execute_job $JOBS_DIR/stack.exp
execute_job $JOBS_DIR/sample_deforestation.exp

if [ "$MODE" == "SLURM" ]; then
    check_job_complete_slurm "calculate_global_stats"
    check_job_complete_slurm "stack"
    check_job_complete_slurm "sample_deforestation"
fi

execute_job $JOBS_DIR/cut_tiles_distributed.exp

echo "All jobs have been submitted/executed based on the $MODE mode!"
