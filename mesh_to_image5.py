#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 15:49:57 2021

Assumption of the script. STL is exported in LPS, mesh is created with very fine. Image is ITK

@author: benjamin

TODO: possible inversion at sagital orientation, need check

"""

import trimesh as tr
import numpy as np
import itk
import vtk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numba import jit, njit, prange
import argparse

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Texture plugger')
  parser.add_argument('-im', '--inputMesh', help='Input .mesh', type=str, required=False, default = '/home/benjamin/Documents/FetalAtlas/mesh_to_image_testFolder/brain_atlasLPS.mesh')
  parser.add_argument('-it', '--inputNifti', help='Input nifti texture', type=str, required=False, default = '/home/benjamin/Documents/FetalAtlas/mesh_to_image_testFolder/template_T2_reduced_z.nii')
  parser.add_argument('-o', '--output', help='Output file, nii extension required', type=str, required=False, default = '/home/benjamin/Documents/FetalAtlas/mesh_to_image_testFolder/output.nii')

  args = parser.parse_args()

mesh_path = args.inputMesh
nii_path = args.inputNifti
output = args.output

# stl_path = '/home/benjamin/Documents/Datasets/IXILPS.stl'
# nii_path = '/home/benjamin/Documents/Datasets/IXI/IXI002-Guys-0828-T1.nii.gz'
# mesh_path = '/home/benjamin/Documents/Datasets/IXILPS.mesh'

#helper functions
def import_mesh(path):
  '''
  Converts a netgen mesh to a list of np.arrays

  Args:
  path (string): path of mesh file

  Returns:
  mesh (list): list of np.arrays
  
  '''
  mesh = []
  with open(path) as inputfile:
    for line in inputfile:
      mesh.append(line.strip().split(' '))
    for i in range(len(mesh)):
      mesh[i] = list(filter(None, mesh[i]))
      mesh[i] = np.array([float(a) for a in mesh[i]])
  return mesh


def get_vertices(mesh):
  '''
  Extract coordinates and number of nodes from mesh

  Args:
  mesh (list): mesh file as a list of np.arrays

  Returns:
  coordinates (np.array): list of 3 cartesian points
  n_nodes (int): number of nodes
  '''
  n_nodes = np.int64(mesh[0][0])
  coordinates0 = np.zeros((n_nodes,3), dtype=np.float64) # Undeformed coordinates of nodes
  for i in prange(n_nodes):
    coordinates0[i] = np.array([float(mesh[i+1][0]),float(mesh[i+1][1]),float(mesh[i+1][2])]) # Change x, y (Netgen) ORIGINAL: [1][0][2]
    
  coordinates = coordinates0 # Initialize deformed coordinates of nodes
  
  return coordinates0, coordinates, n_nodes

def interpolate_texture(coordinates, itk_image):
    "interpolate texture from itk interpolator for each coordinate"
    texture = np.zeros(len(coordinates))
    interpolator = itk.NearestNeighborInterpolateImageFunction.New(itk_image)
    for i in range(len(coordinates)):       
        index = itk_image.TransformPhysicalPointToContinuousIndex(coordinates[i])
        texture[i] = interpolator.EvaluateAtContinuousIndex(index)
    return texture

itk_image = itk.imread(nii_path)
mesh = import_mesh(mesh_path)
coordinates, coordinates0, n_nodes = get_vertices(mesh)

texture = interpolate_texture(coordinates, itk_image)

shape = np.shape(itk_image)

np_image = np.zeros((shape))
np_mask = np.zeros((shape))
# np_image = np.zeros((256, 256, 256))
for i in range(len(coordinates)):
    index = itk_image.TransformPhysicalPointToIndex(coordinates[i])
    #does not deal with multiple index, if only two it could be stacked
    np_image[index[2], index[1], index[0]] = texture[i]
    np_mask[index[2], index[1], index[0]] = 100
    
nii_image = itk.GetImageFromArray(np_image)
itk.imwrite(nii_image, output)




