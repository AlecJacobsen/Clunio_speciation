import subprocess
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--X', dest = 'X', type = int)
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
reduced_model.slim
    """ % (pop_size, mu, r, lunar_qtl_effect_sd, lunar_qtl_proportion, day_sd,  day_mating_interaction_sd, Cw, initial_x, initial_y, disp_sd, K, num_kids, total_gens)
    return(slim_command)

phenos_array = np.full((10000,30),np.nan)
for i in range(10000):
    res = subprocess.run([slim_command(initial_x = args.X)], shell = True, stdout = subprocess.PIPE)
    vals = res.stdout.decode('utf-8').split('\n')[-3].split()
    vals = np.array([float(x) for x in vals])
    phenos_array[i,:] = np.histogram(vals, bins = 30, range = (0,30))[0]

np.save('initial2final_states/%s_Phenos.npy' % args.X,phenos_array)
