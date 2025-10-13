#!/bin/bash 
#SBATCH --job-name=SiM_Jimmy_central
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --time=100:00:00
#SBATCH --mem=1G
#SBATCH --error=/home/jacobsen/SLiM_sims/error/SLiM.%J.err
#SBATCH --output=/home/jacobsen/SLiM_sims/error/SLiM.%J.out
#SBATCH --partition=global

out_dir="CwSd_paramSweep"

for i in {1..1000}
do
  while (( `squeue -n SiM_Jimmy | wc -l` > 25 ))
  do
    sleep 5
  done
  
  echo $i
  
  sbatch --job-name=SiM_Jimmy --ntasks=1 --nodes=1 --time=05:00:00 --mem=5G --error=/home/jacobsen/SLiM_sims/error/ecol_sim.%J.err --output=/home/jacobsen/SLiM_sims/error/ecol_sim.%J.out --partition=highmem --wrap="module load python/3.9.13; python3 run_optimized_eco_model.py --rep ${i} --out_dir ${out_dir}"
done
