#!/bin/bash

CONFIG_FILE="config.yml"
JOB_NAME="$1" # The specific job name passed as an argument (e.g., cut_tiles_distributed)

if [ -z "$JOB_NAME" ]; then
    echo "You must provide a job name as an argument."
    exit 1
fi

# Extract SLURM settings from the config using the provided job name
#SBATCH --job-name=$(yq eval ".jobs.$JOB_NAME.JOB_NAME" $CONFIG_FILE)
#SBATCH --nodes=$(yq eval ".jobs.$JOB_NAME.NODES" $CONFIG_FILE)
#SBATCH --cpus-per-task=$(yq eval ".jobs.$JOB_NAME.CPUS_PER_TASK" $CONFIG_FILE)
#SBATCH --time=$(yq eval '.SLURM.DEFAULT.RUN_TIME' $CONFIG_FILE)
#SBATCH --mem-per-cpu=$(yq eval '.SLURM.DEFAULT.MEM_PER_CPU' $CONFIG_FILE)
#SBATCH --ntasks-per-node=$(yq eval ".jobs.$JOB_NAME.NTASKS_PER_NODE" $CONFIG_FILE)

# Extract paths and arguments from the config
WORK_DIR=$(yq eval '.SLURM.WORK_DIR' $CONFIG_FILE)
PYTHON_ENV=$(yq eval '.SLURM.PYTHON_ENV' $CONFIG_FILE)
LOG_FILE=$(yq eval ".jobs.$JOB_NAME.LOG_FILE" $CONFIG_FILE)

INPUT_TIF=$(yq eval ".jobs.$JOB_NAME.INPUT_TIF" $CONFIG_FILE)
OUTPUT_DIR=$(yq eval ".jobs.$JOB_NAME.OUTPUT_DIR" $CONFIG_FILE)
PICKLE_DIR=$(yq eval ".jobs.$JOB_NAME.PICKLE_DIR" $CONFIG_FILE)
WINDOW_SIZE=$(yq eval '.GLOBAL.WINDOW_SIZE' $CONFIG_FILE)
MASK_FILE=$(yq eval ".jobs.$JOB_NAME.MASK_FILE" $CONFIG_FILE)
OVERWRITE=$(yq eval ".jobs.$JOB_NAME.OVERWRITE" $CONFIG_FILE)

# Modules to load
MODULES=($(yq eval '.SLURM.MODULES[]' $CONFIG_FILE))

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
