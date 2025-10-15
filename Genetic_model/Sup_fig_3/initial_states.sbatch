#!/bin/bash 
#SBATCH --job-name=Gen_sims_central
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --time=00:10:00
#SBATCH --mem=1G
#SBATCH --error=/home/jacobsen/SLiM_sims/error/SLiM_genParams.%J.err
#SBATCH --output=/home/jacobsen/SLiM_sims/error/SLiM_genParams.%J.out
#SBATCH --partition=global

eval "$(/data/modules/python/python-anaconda3-2020.02/bin/conda shell.bash hook)"
conda activate slim;

for i in {1..30}
do
  echo $i
  sbatch --job-name=SiM_Jimmy_3 --ntasks=1 --nodes=1 --time=50:00:00 --mem=5G --error=/home/jacobsen/SLiM_sims/error/gen_genParams.%J.err --output=/home/jacobsen/SLiM_sims/error/gen_genParams.%J.out --partition=highmem --wrap="python3 initial_states.py --X ${i}"
done

