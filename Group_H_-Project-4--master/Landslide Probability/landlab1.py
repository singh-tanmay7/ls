import six
import os
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from landlab import RasterModelGrid
from landlab import imshow_grid_at_node
from landlab.components.landslides import LandslideProbability
from landlab.io import read_esri_ascii
from landlab.io import write_esri_ascii
from collections import defaultdict

print(sorted(LandslideProbability.input_var_names))
print(LandslideProbability._var_doc)
print(LandslideProbability._var_units)
(grid,z)=read_esri_ascii("file.asc",name='topographic__elevation')
grid.at_node.keys()
grid.set_nodata_nodes_to_closed(grid.at_node['topographic__elevation'],-9999)
print(grid.number_of_nodes)
gridnodes=grid.number_of_nodes

scatter_dat= np.random.randint(1, 10, gridnodes)

grid['node']['topographic__slope'] = np.random.rand(gridnodes)

grid['node']['topographic__specific_contributing_area']= np.sort(np.random.randint(30, 900, gridnodes))

grid['node']['soil__transmissivity']= np.sort(np.random.randint(5, 20, gridnodes),-1)

grid['node']['soil__mode_total_cohesion']= np.sort(np.random.randint(30, 900, gridnodes))

grid['node']['soil__minimum_total_cohesion']= grid.at_node['soil__mode_total_cohesion'] - scatter_dat

grid['node']['soil__maximum_total_cohesion']= grid.at_node['soil__mode_total_cohesion'] + scatter_dat

grid['node']['soil__internal_friction_angle']= np.sort(np.random.randint(26, 37, gridnodes))

grid['node']['soil__density']= 2000. * np.ones(gridnodes)

grid['node']['soil__thickness']= np.sort(np.random.randint(1, 10, gridnodes))


iterations=250

distribution1 = 'uniform'
Remin_value = 5 
Remax_value = 15 

LS_prob = LandslideProbability(grid,number_of_iterations=iterations,
    groudwater__recharge_distribution=distribution1,
    groundwater__recharge_min_value=Remin_value,
    groundwater__recharge_max_value=Remax_value)
print('Distribution = '+LS_prob.groundwater__recharge_distribution) 
print('Uniform recharge successfully instantiated')


LS_prob.calculate_landslide_probability()
print('Landslide probability successfully calculated')

print(sorted(LS_prob.output_var_names))

LS_prob_probability_of_failure = grid.at_node['landslide__probability_of_failure']
print(grid.at_node['landslide__probability_of_failure'])

LS_prob_relative_wetness = grid.at_node['soil__mean_relative_wetness']
print(grid.at_node['soil__mean_relative_wetness'])


mpl.rcParams['xtick.labelsize'] = 15
mpl.rcParams['ytick.labelsize'] = 15
mpl.rcParams['lines.linewidth'] = 1
mpl.rcParams['axes.labelsize'] = 18
mpl.rcParams['legend.fontsize'] = 15



plt.figure('Elevations from the DEM [m]')
imshow_grid_at_node(grid, 'topographic__elevation', cmap='terrain',
                 grid_units=('coordinates', 'coordinates'),
                 shrink=0.75, var_name='Elevation', var_units='m')
plt.savefig('Elevation.png')





# plt.figure('Landslides')
# ls_mask1 = grid.at_node['landslides'] != 1.0
# ls_mask2 = grid.at_node['landslides'] != 2.0
# ls_mask3 = grid.at_node['landslides'] != 3.0
# ls_mask4 = grid.at_node['landslides'] != 4.0
# overlay_landslide1 = np.ma.array(grid.at_node['landslides'], mask=ls_mask1)
# overlay_landslide2 = np.ma.array(grid.at_node['landslides'], mask=ls_mask2)
# overlay_landslide3 = np.ma.array(grid.at_node['landslides'], mask=ls_mask3)
# overlay_landslide4 = np.ma.array(grid.at_node['landslides'], mask=ls_mask4)
# imshow_grid_at_node(grid, 'topographic__slope', cmap='pink',
#                  grid_units=('coordinates', 'coordinates'), vmax=2.,
#                  shrink=0.75, var_name='Slope', var_units='m/m')
# imshow_grid_at_node(grid, overlay_landslide1, color_for_closed='None',
#                  allow_colorbar=False, cmap='cool')
# imshow_grid_at_node(grid, overlay_landslide2, color_for_closed='None',
#                  allow_colorbar=False, cmap='autumn')
# imshow_grid_at_node(grid, overlay_landslide3, color_for_closed='None',
#                  allow_colorbar=False, cmap='winter')
# imshow_grid_at_node(grid, overlay_landslide4, color_for_closed='None',
#                  allow_colorbar=False,cmap='summer')




plt.figure('Soil Thickness')
imshow_grid_at_node(grid, 'soil__thickness', cmap='copper_r',
                 grid_units=('coordinates', 'coordinates'), shrink=0.75,
                 var_name='Soil Thickness', var_units='m')
plt.savefig('Soil_Thckness.png')




plt.figure('Probability of Saturation')
imshow_grid_at_node(grid, 'soil__probability_of_saturation', cmap='YlGnBu',
                 limits=((0), (1)),
                 grid_units=('coordinates', 'coordinates'),
                 shrink=0.75, var_name='Probability of Saturation',
                 var_units='no units')
plt.savefig('probability_of_saturation.png')


plt.figure('Probability of Failure')
imshow_grid_at_node(grid, 'landslide__probability_of_failure', cmap='OrRd',
                 grid_units=('coordinates', 'coordinates'), shrink=0.75,
                 var_name='Probability of Failure', var_units='no units')
plt.savefig('probability_of_failure.png')