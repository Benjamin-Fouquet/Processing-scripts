#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 15:50:24 2021

compare 2 stl and return % of similarity, and accumulated distance of the difference. The comparison is done node to node, for the whole mesh. 
TODO: purcentage of tolerance to consider that its a matching point ?

@author: benjamin
"""
import numpy as np
import trimesh as tr
import argparse

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Texture plugger')
  parser.add_argument('-i1', '--input1', help='Input STL 1', type=str, required=False, default = '/home/benjamin/Documents/tests/step_control/ground_truth/pov_H0.042000AT1.829000/B223500.stl')
  parser.add_argument('-i2', '--input2', help='Input STL 2', type=str, required=False, default = '/home/benjamin/Documents/tests/step_control/0.1/pov_H0.042000AT1.829000/B22000.stl')
  args = parser.parse_args()

path1 = args.input1
path2 = args.input2
            
def compare_stl(path1, path2):
    mesh1 = tr.load(path1)
    mesh2 = tr.load(path2)
    closest_point, distance, closest_face = tr.proximity.closest_point(mesh1, mesh2.vertices)
    comparison = mesh1.vertices == mesh2.vertices
    matches = 0
    cumulative_distance = 0
    for i in comparison:
        if comparison.all() == True:
            matches += 1
    for i in distance:
        cumulative_distance += i
    
    brain_length1 = np.max(mesh1.vertices[:,0]) - np.min(mesh1.vertices[:,0])
    brain_length2 = np.max(mesh2.vertices[:,0]) - np.min(mesh2.vertices[:,0])
    print(str(matches/len(comparison)*100) + "% one to one node accuracy")
    print("Cumulative distance is " + str(cumulative_distance)) 
    print("Brain length 1 is " + str(brain_length1))
    print("Brain length 1 is " + str(brain_length2))
    #volume accuracy ? volume mismatch /total volum of stl:: complicated...
    #ideally, you want to calculate the two volumes and tell the difference, also in term of outside volume in space
    
    
    
compare_stl(path1, path2)
    
#closest_point, distance, closest_face = tr.proximity.closest_point(mesh, coord_list)
    