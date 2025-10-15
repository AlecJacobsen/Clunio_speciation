#!/bin/bash 
#SBATCH --job-name=SiM_Jimmy_2_central
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --time=200:00:00
#SBATCH --mem=1G
#SBATCH --error=/home/jacobsen/SLiM_sims/error/SLiM.%J.err
#SBATCH --output=/home/jacobsen/SLiM_sims/error/SLiM.%J.out
#SBATCH --partition=global

eval "$(/data/modules/python/python-anaconda3-2020.02/bin/conda shell.bash hook)"
conda activate slim;

for i in {1..1000}
do
  while (( `squeue -n SiM_Jimmy_2 | wc -l` > 100 ))
  do
    sleep 5
  done
  
  echo $i
  
  sbatch --job-name=SiM_Jimmy_2 --ntasks=1 --nodes=1 --time=10:00:00 --mem=5G --error=/home/jacobsen/SLiM_sims/error/gen_sim.%J.err --output=/home/jacobsen/SLiM_sims/error/gen_sim.%J.out --partition=highmem --wrap="python3 CwSd_ParamSweep_flat.py --rep ${i}"
  sbatch --job-name=SiM_Jimmy_2 --ntasks=1 --nodes=1 --time=10:00:00 --mem=5G --error=/home/jacobsen/SLiM_sims/error/gen_sim.%J.err --output=/home/jacobsen/SLiM_sims/error/gen_sim.%J.out --partition=highmemnew --wrap="python3 CwSd_ParamSweep_linear.py --rep ${i}"
  sbatch --job-name=SiM_Jimmy_2 --ntasks=1 --nodes=1 --time=10:00:00 --mem=5G --error=/home/jacobsen/SLiM_sims/error/gen_sim.%J.err --output=/home/jacobsen/SLiM_sims/error/gen_sim.%J.out --partition=highmemnew --wrap="python3 CwSd_ParamSweep_unimodal.py --rep ${i}"
  sbatch --job-name=SiM_Jimmy_2 --ntasks=1 --nodes=1 --time=10:00:00 --mem=5G --error=/home/jacobsen/SLiM_sims/error/gen_sim.%J.err --output=/home/jacobsen/SLiM_sims/error/gen_sim.%J.out --partition=highmem2new --wrap="python3 CwSd_ParamSweep_bimodal.py --rep ${i}"
done
