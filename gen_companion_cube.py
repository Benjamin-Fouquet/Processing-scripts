#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 13:44:55 2021

Creates a cube with different textures to test the geometry of various scripts

@author: benjamin
"""

import numpy as np
import itk

image = np.zeros((128, 128, 128))

for i in range(len(image)):
    for j in range(len(image[i])):
        for k in range(len(image[i][j])):
            if i > 64 and i < 96:
                image[i][j][k] += 100
            if j > 64 and j < 96:
                image[i][j][k] += 100
            if k > 64 and k < 96:
                image[i][j][k] += 100
            if i < 32 or i > 96:
                image[i][j][k] = 0
            if j < 32 or j > 96:
                image[i][j][k] = 0
            if k < 32 or k > 96:
                image[i][j][k] = 0
            
                
nii_image = itk.GetImageFromArray(image)
itk.imwrite(nii_image, '/home/benjamin/Documents/FetalAtlas/mesh_to_image_testFolder/companion_cube_plain.nii.gz')