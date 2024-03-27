#!/bin/bash

#SBATCH --job-name=SiM_Jimmy_central
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --time=100:00:00
#SBATCH --mem=1G
#SBATCH --error=/home/jacobsen/SLiM_sims/error/SLiM.%J.err
#SBATCH --output=/home/jacobsen/SLiM_sims/error/SLiM.%J.out
#SBATCH --partition=global

for i in {1..2000}
do
 while (( `squeue -n PIPs_sim | wc -l` > 100))
 do
  sleep 1
 done

 echo $i
 
 sbatch --job-name=PIPs_sim --ntasks=1 --nodes=1 --time=02:00:00 --mem=5G --error=/home/jacobsen/SLiM_sims/error/pips_sim.%J.err --output=/home/jacobsen/SLiM_sims/error/pips_sim.%J.out --partition=fast --wrap="module load python/3.9.13; python3 make-pip.py --rep ${i} --outdir pips --Cw 0.025 --sd 0.075"


 sbatch --job-name=PIPs_sim --ntasks=1 --nodes=1 --time=02:00:00 --mem=5G --error=/home/jacobsen/SLiM_sims/error/pips_sim.%J.err --output=/home/jacobsen/SLiM_sims/error/pips_sim.%J.out --partition=fast --wrap="module load python/3.9.13; python3 make-pip.py --rep ${i} --outdir pips --Cw 0.1 --sd 0.25"


 sbatch --job-name=PIPs_sim --ntasks=1 --nodes=1 --time=02:00:00 --mem=5G --error=/home/jacobsen/SLiM_sims/error/pips_sim.%J.err --output=/home/jacobsen/SLiM_sims/error/pips_sim.%J.out --partition=fast --wrap="module load python/3.9.13; python3 make-pip.py --rep ${i} --outdir pips --Cw 0.25 --sd 0.9"

done
