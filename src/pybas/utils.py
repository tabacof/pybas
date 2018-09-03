import pystan
import pickle
import seaborn as sns
import numpy as np

import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Trace:
    def __init__(self, x):
        self.x = x
        self.n = float(len(x))
        
    def pr(self, greater_than, less_than):
        return len(self.x[(self.x > greater_than) & (self.x < less_than)])/self.n
    
    def mean(self):
        return np.mean(self.x)

    def median(self):
        return np.median(self.x)
    
    def std(self):
        return np.std(self.x)
        
    def ci(self, alpha=0.95):
        return np.percentile(self.x, (1-alpha)*100), np.percentile(self.x, alpha*100)
        
    def plot_hist(self, **kwargs):
        sns.distplot(self.x, **kwargs)

    def plot_trace(self,  **kwargs):
        sns.lineplot(self.x,  **kwargs)

    def values(self):
        return self.x


def load_model(model):
    path, _ = os.path.split(__file__)
    pickled_model = f'{path}/../../pickles/{model}.pkl'
    if os.path.exists(pickled_model):
        sm = pickle.load(open(pickled_model, 'rb'))
    else:
        logger.info(f'Compiling {model} model')
        with open(f'{path}/stan/{model}.stan') as f:
            sc = f.read()
        sm = pystan.StanModel(model_code=sc)
        with open(pickled_model, 'wb') as f:
            pickle.dump(sm, f)
    return sm


def cohens_d(mu_x, mu_y, sd_x, sd_y):
    nx = len(mu_x)
    ny = len(mu_y)
    pooled_sd = np.sqrt(((nx-1)*sd_x**2 + (ny-1)*sd_y**2)/(nx + ny - 2))
    return (mu_x - mu_y)/pooled_sd
 

