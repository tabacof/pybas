import pystan
import pickle
import matplotlib.pyplot as plt

import numpy as np
from scipy.optimize import minimize

import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Trace:
    def __init__(self, x):
        self.x = x
        self.n = float(len(x))
        
    def pr(self, greater_than=0, less_than=np.inf):
        return len(self.x[(self.x > greater_than) & (self.x < less_than)])/self.n
    
    def mean(self):
        return np.mean(self.x)

    def median(self):
        return np.median(self.x)
    
    def std(self):
        return np.std(self.x)
    
    def hpd(self, alpha=0.95, modes=1):
        x0 = self.ci(alpha)
        print(x0)
        self.fn = lambda x: (alpha - len(self.x[(self.x>=x[0]) & (self.x<=x[1])])/len(self.x))**2
        #cons = ({'type': 'ineq', 'fun': lambda x:})
        #bounds = [(0, 1), (0, 1)]
        res = minimize(self.fn, x0)#, constraints=cons)
        return res
        
    def ci(self, alpha=0.95):
        return np.percentile(self.x, (1-alpha)*100), np.percentile(self.x, alpha*100)
        
    def plot_hist(self):
        plt.figure()
        plt.hist(self.x, bins='auto')
        plt.show()
        
    def plot_trace(self):
        plt.figure()
        plt.plot(self.x)
        plt.show()

    def values(self):
        return self.x

def load_model(model):
    pickled_model = 'pickles/'+model+'.pkl'
    if os.path.exists(pickled_model):
        sm = pickle.load(open(pickled_model, 'rb'))
    else:
        logger.info('Compiling ' + model + ' model')
        with open('stan/'+model+'.stan') as f:
            sc = f.read()
            sm = pystan.StanModel(model_code=sc)
        with open(pickled_model, 'wb') as f:
            pickle.dump(sm, f)
    return sm

def cohens_d(mu_x, mu_y, sd_x, sd_y):
    nx = len(mu_x)
    ny = len(mu_y)
    pooled_sd = np.sqrt(((nx-1)*sd_x**2 + (ny-1)*sd_y**2)/(nx + ny -2))
    return (mu_x - mu_y)/pooled_sd
 
class t_test:
    def __init__(self):
        self.sm = load_model('t_test')

    def fit(self, x, y):
        self.data = {'x': x, 'y': y, 'n_x': len(x), 'n_y': len(y)}
        self.fit = self.sm.sampling(self.data)
        self.trace = self.fit.extract()

    def effect_size(self):
        return Trace(cohens_d(self.trace['mu_x'], self.trace['mu_y'],self.trace['sd_x'], self.trace['sd_y']))

    def diff(self):
        return Trace(self.trace['mu_x'] - self.trace['mu_y'])
    

    
