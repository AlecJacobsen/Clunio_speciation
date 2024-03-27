import subprocess

#eval "$(/data/modules/python/python-anaconda3-2020.02/bin/conda shell.bash hook)"
#python3 run_sim_LunarNonWF.py

# PARAMS
# pop_size = number of individuals
# mu = mutation rate
# r = recombination ra
# lunar_qtl_effect_sd = standard deviation of effect sizes for luanr mutations
# lunar_qtl_proportion = relative proportion of lunar qtls
# day_sd = standard deviation of lunar phenotype probability
# day_mating_interaction_sd = standard deviation of interactions over days - set it as low as possible for mating only within day
# depth_competition_interaction_sd = stander deviation or depth interaction for competiti
# initial_x = initial lunar phenotype
# initial_y = initial depth
# larval_dispersal = larval dispersal sd 

def slim_command(working_dir, file_name, pop_size = 1000, mu = 1e-7, r = 1e-7, lunar_qtl_effect_sd = 0.5, lunar_qtl_proportion = 0.1, day_sd = 0.25, day_mating_interaction_sd = 0.00000001,  comp_sd = 0.5, initial_x = 15, initial_y = 0, larval_dispersal = 0.1, K = 500, total_gens = 5001):
    slim_command = """
slim \
-d pop_size=%s \
-d mu=%s \
-d r=%s \
-d lunar_qtl_effect_sd=%s \
-d lunar_qtl_proportion=%s \
-d day_sd=%s \
-d day_mating_interaction_sd=%s \
-d comp_sd=%s \
-d initial_x=%s \
-d initial_y=%s \
-d larval_dispersal=%s \
-d K=%s \
-d total_gens=%s \
/home/jacobsen/SLiM_sims/ClockEvol_Lunar_nonWF/ClockEvol_Lunar_nonWF.slim > %s/%s
    """ % (pop_size, mu, r, lunar_qtl_effect_sd, lunar_qtl_proportion, day_sd,  day_mating_interaction_sd, comp_sd, initial_x, initial_y, larval_dispersal, K, total_gens, working_dir, file_name)
    return(slim_command)

def QTL_slim_command(working_dir, file_name, pop_size = 1000, mu = 1e-7, r = 1e-7, lunar_qtl_effect_sd = 0.5, lunar_qtl_proportion = 0.1, day_sd = 0.25, day_mating_interaction_sd = 0.00000001,  comp_sd = 0.5, initial_x = 15, initial_y = 0, larval_dispersal = 0.1, K = 500, total_gens = 5001, run = 0):
    slim_command = """
slim \
-d pop_size=%s \
-d mu=%s \
-d r=%s \
-d lunar_qtl_effect_sd=%s \
-d lunar_qtl_proportion=%s \
-d day_sd=%s \
-d day_mating_interaction_sd=%s \
-d comp_sd=%s \
-d initial_x=%s \
-d initial_y=%s \
-d larval_dispersal=%s \
-d K=%s \
-d total_gens=%s \
-d run=%s \
/home/jacobsen/SLiM_sims/ClockEvol_Lunar_nonWF/ClockEvol_Lunar_nonWF_returnEffects.slim > %s/%s
    """ % (pop_size, mu, r, lunar_qtl_effect_sd, lunar_qtl_proportion, day_sd,  day_mating_interaction_sd, comp_sd, initial_x, initial_y, larval_dispersal, K, total_gens, run, working_dir, file_name)
    return(slim_command)

def inversion_slim_command(working_dir, file_name, pop_size = 1000, mu = 1e-7, r = 1e-7, lunar_qtl_effect_sd = 0.5, lunar_qtl_proportion = 0.1, day_sd = 0.25, day_mating_interaction_sd = 0.00000001,  comp_sd = 0.5, initial_x = 15, initial_y = 0, larval_dispersal = 0.1, K = 500, total_gens = 2501, inversion = 1):
    slim_command = """
slim \
-d pop_size=%s \
-d mu=%s \
-d r=%s \
-d lunar_qtl_effect_sd=%s \
-d lunar_qtl_proportion=%s \
-d day_sd=%s \
-d day_mating_interaction_sd=%s \
-d comp_sd=%s \
-d initial_x=%s \
-d initial_y=%s \
-d larval_dispersal=%s \
-d K=%s \
-d total_gens=%s \
-d inversion=%s \
/home/jacobsen/SLiM_sims/ClockEvol_Lunar_nonWF/ClockEvol_Lunar_nonWF_inversion.slim > %s/%s
    """ % (pop_size, mu, r, lunar_qtl_effect_sd, lunar_qtl_proportion, day_sd,  day_mating_interaction_sd, comp_sd, initial_x, initial_y, larval_dispersal, K, total_gens, inversion, working_dir, file_name)
    return(slim_command)


slurm_boilerplate = """#!/bin/bash 
#SBATCH --job-name=SLiM_Jimmy
#SBATCH --ntasks=10
#SBATCH --nodes=1
#SBATCH --time=10:00:00
#SBATCH --mem=10G
#SBATCH --error=/home/jacobsen/SLiM_sims/error/SLiM.%J.err
#SBATCH --output=/home/jacobsen/SLiM_sims/error/SLiM.%J.out
#SBATCH --partition=highmem

eval "$(/data/modules/python/python-anaconda3-2020.02/bin/conda shell.bash hook)"

conda activate slim
"""
### Single Run ###
# working_dir = '/home/jacobsen/SLiM_sims/ClockEvol_Lunar_nonWF/test' #change this for other runs
# with open('%s/run_SLiM_test.sbatch' % (working_dir),'w') as nf: # creating the sbatch files to run
#     nf.write(slurm_boilerplate)
#     nf.write(inversion_slim_command(working_dir,file_name='test.output'))
# subprocess.run(['sbatch','%s/run_SLiM_test.sbatch' % (working_dir)])


### Different Initial States ###
# working_dir = '/home/jacobsen/SLiM_sims/ClockEvol_Lunar_nonWF/initial_states' #change this for other runs
# for x in [0,5,10,15,20,25]: # set param values to be tested
#     for y in [-1,-0.5,0,0.5,1]:
#         with open('%s/run_SLiM_X%sY%s.sbatch' % (working_dir,x,y),'w') as nf: # creating the sbatch files to run
#             nf.write(slurm_boilerplate)
#             for i in range(10):
#                 nf.write(slim_command(working_dir,file_name='X%s_Y%s_run_%s.output' % (x,y,i),initial_x=x,initial_y=y))
#         subprocess.run(['sbatch','%s/run_SLiM_X%sY%s.sbatch' % (working_dir,x,y)])

## Different Competition Strengths ###
# working_dir = '/home/jacobsen/SLiM_sims/ClockEvol_Lunar_nonWF/competition_interaction' #change this for other runs
# for comp in [0.1,0.2,0.3,0.4,0.5,0.7,1.0,1.5]: # set param values to be tested
#     for disp in [0.05, 0.1, 0.15, 0.2, 0.25,0.35,0.5,0.75]:
#         with open('%s/run_SLiM_comp%s_disp%s.sbatch' % (working_dir,comp,disp),'w') as nf: # creating the sbatch files to run
#             nf.write(slurm_boilerplate)
#             for i in range(10):
#                 nf.write(slim_command(working_dir,file_name='comp%s_disp%s_run_%s.output' % (comp,disp,i),comp_sd=comp, larval_dispersal=disp))
#         subprocess.run(['sbatch','%s/run_SLiM_comp%s_disp%s.sbatch' % (working_dir,comp,disp)])

### Different Lunar QTL effect sizes and proportions ###
# working_dir = '/home/jacobsen/SLiM_sims/ClockEvol_Lunar_nonWF/QTL_effects' #change this for other runs
# for Le in [0.01,0.1,0.5,1.0]: # set param values to be tested
#     for Lp in [0.001,0.01,0.1,0.2,0.5]:
#         with open('%s/run_SLiM_Le%sLp%s.sbatch' % (working_dir,Le,Lp),'w') as nf: # creating the sbatch files to run
#             nf.write(slurm_boilerplate)
#             for i in range(10):
#                 nf.write(QTL_slim_command(working_dir,file_name='Le%s_Lp%s_run_%s.output' % (Le,Lp,i),lunar_qtl_effect_sd = Le, lunar_qtl_proportion = Lp, run = i))
#         subprocess.run(['sbatch','%s/run_SLiM_Le%sLp%s.sbatch' % (working_dir,Le,Lp)])

## Different number of gens before the split 
# working_dir = '/home/jacobsen/SLiM_sims/ClockEvol_JustLunar/pre_gens' #change this for other runs
# for gen in [100,200,300,400,500,600,700,800,900,1000]: # set param values to be tested
#     with open('%s/run_SLiM_gen%s.sbatch' % (working_dir,gen),'w') as nf: # creating the sbatch files to run
#         nf.write(slurm_boilerplate)
#         for i in range(10):
#             nf.write(slim_command(working_dir,file_name='gen%s_run_%s.output' % (gen,i), gens_before_split = gen, total_gens = 2000))
#     subprocess.run(['sbatch','%s/run_SLiM_gen%s.sbatch' % (working_dir,gen)])

## Long runs
# working_dir = '/home/jacobsen/SLiM_sims/ClockEvol_JustLunar/long_run' #change this for other runs
# with open('%s/run_SLiM_long_run.sbatch' % (working_dir),'w') as nf: # creating the sbatch files to run
#     nf.write(slurm_boilerplate)
#     for i in range(20):
#         nf.write(slim_command(working_dir,file_name='long_run_%s.output' % (i), total_gens = 20000))
# subprocess.run(['sbatch','%s/run_SLiM_long_run.sbatch' % (working_dir)])

## Inversion 
# working_dir = '/home/jacobsen/SLiM_sims/ClockEvol_Lunar_nonWF/Inversion'
# for inv in [0,1]:
#     for replicate in range(25):
#         with open('%s/run_SLiM_inv%s_rep%s.sbatch' % (working_dir,inv,replicate),'w') as nf: # creating the sbatch files to run
#             nf.write(slurm_boilerplate)
#             for i in range(20):
#                 nf.write(inversion_slim_command(working_dir,file_name='inv_run_inv%s_rep%s_run%s.output' % (inv,replicate,i), inversion = inv, lunar_qtl_effect_sd = 0.2, lunar_qtl_proportion = 0.3, initial_x= 12))
#         subprocess.run(['sbatch','%s/run_SLiM_inv%s_rep%s.sbatch' % (working_dir,inv,replicate)])

## Randomness
working_dir = '/home/jacobsen/SLiM_sims/ClockEvol_Lunar_nonWF/randomness' #change this for other runs
for sd in [2.5,3.0,3.5,4.0]: # set param values to be tested
    with open('%s/run_SLiM_sd%s.sbatch' % (working_dir,sd),'w') as nf: # creating the sbatch files to run
        nf.write(slurm_boilerplate)
        for i in range(10):
            nf.write(slim_command(working_dir,file_name='sd%s_run_%s.output' % (sd,i), day_sd=sd))
    subprocess.run(['sbatch','%s/run_SLiM_sd%s.sbatch' % (working_dir,sd)])

