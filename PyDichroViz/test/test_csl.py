import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from module.csl import sigma_list, calculate_GB_planes
import numpy as np


uvw = np.array([1, 0, 0])
sigma = 5
basis = 'fcc'

angles = sigma_list(uvw, 50)
print("Angles for UVW = [1, 0, 0]:")
for sigma, angle in angles:
    print(f"Sigma: {sigma}, Angle: {angle:.2f} degrees")

results = calculate_GB_planes(basis, uvw, sigma)
print(f"Grain boundary planes for UVW = {uvw}, Basis = {basis}, Sigma = {sigma}:\n")
for GB1, GB2, Type in results:
    print("{0:<20s}   {1:<20s}   {2:<20s}"
        .format(str(GB1), str(GB2), Type))

