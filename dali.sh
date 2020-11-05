#!/bin/bash
#SBATCH --partition=p_sdk94_1
#SBATCH --job-name=dali_arr
#SBATCH --array=0-12
#SBATCH --cpus-per-task=1
#SBATCH --mem=12G
#SBATCH --time=99:00:00
#SBATCH --nodes=1
 

srun python get_neighbor_neighbors.py $SLURM_ARRAY_TASK_ID
echo $SLURM_ARRAY_TASK_ID
