import pandas as pd
import numpy as np                                                                                         
import argparse                                                                                            
                                                                                                           
parser = argparse.ArgumentParser()                                                                         
parser.add_argument('--rep', dest = 'rep', default = 0)                                                                 
parser.add_argument('--out_dir', dest = 'out_dir')
parser.add_argument('--X', dest = 'X', default = 15, type = int)
args = parser.parse_args() 

class ecology_model:
    def __init__(self,sd,Cw,K,mu,N0,X0,Y0,heritability,num_kids,gens):
        self.sd = sd
        self.Cw = Cw
        self.K = K
        self.mu = mu
        self.N0 = N0
        self.X0 = X0
        self.Y0 = Y0
        self.heritability = heritability
        self.num_kids = num_kids
        self.gens = gens
        
    def init_pop(self):
        self.Xs = np.full(self.N0,self.X0)
        self.Ys = np.full(self.N0,self.Y0)

    def disperse_pop(self):
        self.Ys = self.Ys + np.random.normal(0,self.sd,self.Ys.shape)
        
    def calc_Fit(self):
        #print(self.Ys)
        ### Getting interaction strengths 
        y_mat = np.repeat(self.Ys,self.Ys.shape).reshape(self.Ys.shape[0],self.Ys.shape[0])
        arr = -((self.Ys - y_mat)**2)/(2*(self.Cw**2))
        I = np.exp(arr[arr != 0].reshape(arr.shape[0],arr.shape[0]-1)).sum(axis = 1)
        ### Calculating competition fitness
        Fc = self.K/(np.exp(10*I/self.K) + self.K)
        ### Calculating environmental fitness
        Fe = 1/(2+np.exp(6*self.Ys + 1)) + 0.5
        self.Fit = Fc * Fe

    def calc_depth(self):
        actual_Xs = (self.Xs + np.random.normal(0,self.heritability,self.Xs.shape).astype(int))%30 ## needs mod
        return ((np.sin(2*np.pi*(actual_Xs/15) - 5))/2 - 0.5)
    
    def reproduce(self):
        #print(' ')
        ### calculate the number of offspring based off fitness
        num_offs = ((self.Fit * self.num_kids)).astype(int) 
        ### Calculate depth (y) based off emergence phenotype (x)
        Ys = self.calc_depth()
        ### creating array to populate with kids
        x_array = np.full((self.Xs.shape[0],self.num_kids),np.nan)
        y_array = np.full((Ys.shape[0],self.num_kids),np.nan)
        ### filling in arrays with kids 
        for i, num in enumerate(num_offs):
            x_array[i,:num] = self.Xs[i]
            y_array[i,:num] = Ys[i]
        ### mutating kids phenotype (x) and setting it for next gen
        kids_xs = x_array[~np.isnan(x_array)]
        self.Xs = (kids_xs + np.random.normal(0.5,self.mu,kids_xs.shape)).astype(int)%30 ## needs mod 
        #print(self.Xs.shape)
        ### setting ys for next gen
        self.Ys = y_array[~np.isnan(y_array)]    
        #print(self.Ys.shape)

    def run_generation(self):
        self.disperse_pop()
        self.calc_Fit()
        self.reproduce()
    
    def simulate(self,return_array = False, return_N = False):
        self.init_pop()
        if return_array:
            res = np.zeros((self.gens,30))
            #try:
            for i in range(self.gens):
                self.run_generation()
                res[i,:] = np.histogram(self.Xs, bins = 30, range = (0,30))[0]
            return res
            #except (IndexError, ValueError):
            #    print('Population went extict')
            #    return res
        elif return_N:
            N = []
            try:
                for i in range(self.gens):
                    self.run_generation()
                    N.append(self.Xs.shape[0])
                return N
            except ValueError:
                print('Population went extict')
                return N
        else:
            try:
                for i in range(self.gens):
                    self.run_generation()
                return self.count_peaks()
            except ValueError:
                return 0
    
    def count_peaks(self):
        peaks = 0
        prev = 0
        going_up = True
        arr = np.histogram(self.Xs, bins = 30, range = (0,30))[0]
        for num in arr:
            if (num < prev) and going_up:
                peaks += 1
                going_up = False
            if (num > prev):
                going_up = True
            prev = num
        return peaks
    
    def get_split(self, return_array = False):
        self.init_pop()
        gens_since_split = 0
        try:
            if return_array:
                res = np.zeros((self.gens,30))
                for i in range(self.gens):
                    self.run_generation()
                    res[i,:] = np.histogram(self.Xs, bins = 30, range = (0,30))[0]
                    if self.count_peaks() > 1:
                        gens_since_split += 1
                        if gens_since_split >= 50:
                            return (i-49,res)
                    else:
                        gens_since_split = 0
                return (np.nan,res)
            else:
                for i in range(self.gens):
                    self.run_generation()
                    if self.count_peaks() > 1:
                        phenos = np.histogram(self.Xs, bins = 30, range = (0,30))[0]
                        gens_since_split += 1
                        if gens_since_split >= 50:
                            return (i-49,phenos)
                    else:
                        gens_since_split = 0
                phenos = np.histogram(self.Xs, bins = 30, range = (0,30))[0]
                return (np.nan,phenos)
        except IndexError:
            return np.nan

print('Running Sim')                                                                                       

## For CwSd Param Sweep
#Cws = np.linspace(0.025,1,40)                                                                              
#sds = np.linspace(0.025,1,40)                                                                              
#                                                                                                           
#arr = np.zeros((len(Cws),len(sds)))                                                                        
#for i, Cw in enumerate(Cws):                                                                               
#    for j, sd in enumerate(sds):                                                                           
#        arr[i,j] = ecology_model(sd = sd, Cw = Cw, K = 100, mu = 0.18, N0 = 10, X0 = 15, Y0 = 0, heritability = 0, num_kids = 5, gens = 500 
#).simulate()                                                                                               
#                                                                                                           
#np.save('%s/rep%s.npy' % (args.out_dir,args.rep),arr) 

# Testing Different Initial States 
res_arr = np.zeros((1000))
phenos_arr = np.zeros((1000,30))
for i in range(1000):
    res,phenos  = ecology_model(sd = 0.25, Cw = 0.1, K = 100, mu = 0.18, N0 = 10, X0 = args.X, Y0 = 0, heritability = 0.25, num_kids = 5, gens = 1000).get_split()
    res_arr[i] = res
    phenos_arr[i,:] = phenos
np.save('%s/X%s_splitGens.npy' % (args.out_dir,args.X), res_arr)
np.save('%s/X%s_splitPhenos.npy' % (args.out_dir,args.X), phenos_arr)
