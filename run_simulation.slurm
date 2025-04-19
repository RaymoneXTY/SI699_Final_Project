#!/bin/bash
#SBATCH --job-name=sim_$SIM_ID
#SBATCH --account=si699s305w25_class
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:30:00
#SBATCH --mem=4G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=xiongty@umich.edu

module load python/3.10.4
cd $SLURM_SUBMIT_DIR

source sim_env/bin/activate

python driver.py --variant $SIM_ID \
  --weapons physical_weapons.csv \
  --enemies generated_enemies.csv \
  --output simulation_results/simulation_results_${SIM_ID}.csv
