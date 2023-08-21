#!/bin/bash

# Read config file using yaml python module
read_config() {
    python - << END
import yaml

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)
print(config["$1"].get("$2", config["SLURM"]["DEFAULT"]["$2"]))
END
} 

# For example, to get JOB_NAME for stack_xtest:
JOB_NAME=$(read_config stack_xtest JOB_NAME)

echo JOB_NAME: $JOB_NAME

# And for NODES (which should default unless specified)
NODES=$(read_config stack_xtest NODES)
