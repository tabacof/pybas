from .utils import load_model, Trace, cohens_d


class TTest:
    def __init__(self):
        self.sm = load_model('t_test')

    def fit(self, x, y, **kwargs):
        self.data = {'x': x, 'y': y, 'n_x': len(x), 'n_y': len(y)}
        self.fit = self.sm.sampling(self.data, **kwargs)
        self.trace = self.fit.extract()

    def effect_size(self):
        return Trace(cohens_d(self.trace['mu_x'], self.trace['mu_y'], self.trace['sd_x'], self.trace['sd_y']))

    def means_diff(self):
        return Trace(self.trace['mu_x'] - self.trace['mu_y'])


