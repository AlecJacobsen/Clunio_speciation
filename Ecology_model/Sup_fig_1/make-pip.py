import pandas as pd 
import numpy as np 
import argparse 

parser = argparse.ArgumentParser() 
parser.add_argument('--rep', dest = 'rep') 
parser.add_argument('--outdir', dest = 'out_dir')
parser.add_argument('--Cw', dest = 'Cw', type = float)
parser.add_argument('--sd', dest = 'sd', type = float)
args = parser.parse_args()



class ecology_model_pips:
    def __init__(self,sd,Cw,K,N0,X0,Y0,num_kids,gens,mu_gen):
        self.sd = sd
        self.Cw = Cw
        self.K = K
        self.N0 = N0
        self.X0 = X0
        self.Y0 = Y0
        self.num_kids = num_kids
        self.gens = gens
        self.mu_gen = mu_gen
        
    def init_pop(self):
        self.Xs = np.full(self.N0,self.X0)
        self.Ys = np.full(self.N0,self.Y0)

    def disperse_pop(self):
        self.Ys = self.Ys + np.random.normal(0,self.sd,self.Ys.shape)
        
    def calc_Fit(self):
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
        return ((np.sin(2*np.pi*(self.Xs/15) - 5))/2 - 0.5)
    
    def reproduce(self):
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
        self.Xs = (kids_xs).astype(int)%30 ## needs mod 
        ### setting ys for next gen
        self.Ys = y_array[~np.isnan(y_array)]    
        
        
    def introduce_mutant(self):
        self.Xs = np.concatenate((np.array([self.X_inv]),self.Xs[1:]))
        
    def run_generation(self):
        self.disperse_pop()
        self.calc_Fit()
        self.reproduce()
    
    def make_PIP(self):
        pip = np.zeros((30,30))
        for i in range(0,30):
            for j in range(0,30):
                self.X0 = i
                self.X_inv = j
                self.init_pop()
                try:
                    for gen in range(self.gens):
                        self.run_generation()
                        if gen == self.mu_gen:
                            self.introduce_mutant()
                    if np.all(self.Xs == self.X0):
                        pip[i,j] = 0
                    elif np.all(self.Xs == self.X_inv):
                        pip[i,j] = 1
                    elif len(set(self.Xs)) == 2:
                        pip[i,j] = 2
                except ValueError:
                    pip[i,j] = np.nan
        return(pip)

sim = ecology_model_pips(sd = args.sd, Cw = args.Cw, K = 100, N0 = 10, X0 = 15, Y0 = 0, num_kids = 5, gens = 500, mu_gen = 50)

res = sim.make_PIP()
np.save('%s/Cw%s-sd%s_rep%s.npy' % (args.out_dir, args.Cw, args.sd, args.rep),res)


