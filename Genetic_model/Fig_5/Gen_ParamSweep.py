import subprocess
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--rep', dest = 'rep')
args = parser.parse_args()

def slim_command(pop_size = 10, mu = 1e-7, r = 1e-7, lunar_qtl_effect_sd = 0.5, lunar_qtl_proportion = 0.1, day_sd = 0.25, day_mating_interaction_sd = 0.00000001,  Cw = 0.1, initial_x = 15, initial_y = 0, disp_sd = 0.25, K = 200, num_kids = 10, total_gens = 1500):
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
-d num_kids=%s \
-d total_gens=%s \
reduced_model_OutputsFreqs.slim
    """ % (pop_size, mu, r, lunar_qtl_effect_sd, lunar_qtl_proportion, day_sd,  day_mating_interaction_sd, Cw, initial_x, initial_y, disp_sd, K, num_kids, total_gens)
    return(slim_command)

effects = np.linspace(0.01,1,21)
proportions = np.linspace(0.01,0.5,21)
herits = np.linspace(0,3,21)

arr = np.zeros((len(effects),len(proportions),len(herits)))
for i, effect in enumerate(effects):
    for j, prop in enumerate(proportions):
        for k, herit in enumerate(herits):
            res = subprocess.run([slim_command(lunar_qtl_effect_sd = effect, lunar_qtl_proportion = prop, day_sd = herit, total_gens = 3000)], shell = True, stdout = subprocess.PIPE)
            vals = np.array(res.stdout.decode('utf-8').split('\n')[-3].split()).astype(float)
            if vals.shape[0] > 0:
                arr[i,j,k] = np.where(np.logical_and(vals<0.7,vals>0.3))[0].shape[0]/vals.shape[0]
            else:
                arr[i,j,k] = np.nan

np.save('Gen_paramSweep/rep%s.npy' % args.rep,arr)

