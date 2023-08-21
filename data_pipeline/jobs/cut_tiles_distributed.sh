#!/bin/bash

# SLURM settings
JOB_NAME="cut-tiles"
NODES=32
CPUS_PER_TASK=1
RUN_TIME="48:00:00"
MEM_PER_CPU=3700
NTASKS_PER_NODE=48

# Paths and arguments
WORK_DIR="/home/shared/dssg23-deforestation/mapbiomas-deforest/standartization_pipeline"
PYTHON_ENV="/home/wbs/csuqqj/myenv/bin/activate"
LOG_FILE="logs/cut_tiles_32.log"

INPUT_TIF="x_actual_datacube.tif"
OUTPUT_DIR="x_actual_tiles"
PICKLE_DIR="pickles_actual"
WINDOW_SIZE=256
MASK_FILE="None"  # Set to "None" if no mask file
OVERWRITE=true  # Set to true or false

# Modules to load
MODULES=("GCCcore/11.3.0" "Python/3.10.4" "GCC/11.3.0 OpenMPI/4.1.4" "GDAL/3.5.0" "parallel/20220722")

# Submit to SLURM
#SBATCH --job-name=$JOB_NAME
#SBATCH --nodes=$NODES
#SBATCH --cpus-per-task=$CPUS_PER_TASK
#SBATCH --time=$RUN_TIME
#SBATCH --mem-per-cpu=$MEM_PER_CPU
#SBATCH --ntasks-per-node=$NTASKS_PER_NODE

# Set the working directory 
cd $WORK_DIR

# Activate Python Environment
source $PYTHON_ENV

# Purge all loaded modules
module purge

# Load necessary modules
for module in "${MODULES[@]}"; do
    module load $module
done

# Print start date and time
echo "Job started on \`hostname\` at \`date\`" > $LOG_FILE

# Construct the Python script command
CMD="mpirun python cut_tiles_distributed.py --input_tif $INPUT_TIF --output_dir $OUTPUT_DIR --pickle_dir $PICKLE_DIR --window_size $WINDOW_SIZE"
if [ "$MASK_FILE" != "None" ] ; then
    CMD+=" --mask_file $MASK_FILE"
fi
if [ "$OVERWRITE" = true ] ; then
    CMD+=" --overwrite"
fi

# Execute the command
echo $CMD
eval $CMD >> $LOG_FILE

# Print end date and time
echo "Job ended on \`hostname\` at \`date\`" >> $LOG_FILE
