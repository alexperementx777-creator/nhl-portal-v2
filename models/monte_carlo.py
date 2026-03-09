import numpy as np

def run_monte_carlo(xG_home=2.85, xG_away=2.65, n=50000):
    home = np.random.negative_binomial(n=10, p=0.62, size=n) * (xG_home / 2.8)
    away = np.random.negative_binomial(n=10, p=0.62, size=n) * (xG_away / 2.8)
    total = home + away
    return round((total >= 4.5).mean() * 100, 1)
