#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 15:09:44 2021

@author: benjamin
"""
import numpy as np
import nibabel as nb
from math import sin, cos, exp, pi
import itk
TE = 10
TR = 300
alpha = 10
alpha = alpha * (pi/180)
output = 'MRIsignalCalculus.nii'


def generate_map(image, padding):
    for i in range(len(image)):
        for j in range(len(image[i])):
            for k in range(len(image[i][j])):
                if i > 64 and i < 96:
                    image[i][j][k] += padding
                if j > 64 and j < 96:
                    image[i][j][k] += padding
                if k > 64 and k < 96:
                    image[i][j][k] += padding
                if i < 32 or i > 96:
                    image[i][j][k] = 0
                if j < 32 or j > 96:
                    image[i][j][k] = 0
                if k < 32 or k > 96:
                    image[i][j][k] = 0
    return image

np_image = np.zeros((128, 128, 128))

T1_map = generate_map(np_map, 500)
T2star_map = generate_map(np_map, 10)
#choose paramters, TE, TR, alpha
def calculate_signal_GRE(TE, TR, alpha, T1, T2star):
    #source of equation: 
    pd = 100 #proton density assumed to be homogenous
    return pd * exp(-TE/T2star) * ((sin(alpha) * (1 - exp(-TR/T1)))/(1 - (cos(alpha)) * exp(-TR/T1)))

def calculate_signal_spinecho(TE, TR, T1, T2):
    #simplified case with alphas 90/180, approximation not taking into account pd
    #source of equation: https://tel.archives-ouvertes.fr/tel-01954603/file/69264_LEROI_2018_archivage.pdf, chapter 2.2
    M0 = 100
    return M0 * exp(-TE/T2)*(1 - 2 * exp(-(TR - (TE/2))/T1) + exp(-TR/T1))
    
    
#vectorizable non de diou
for i in range(len(np_image)):
    for j in range(len(np_image[i])):
        for k in range(len(np_image[i][j])):
            np_image[i][j][k] = calculate_signa_GRE(TE, TR, alpha, T1_map[i][j][k], T2star_map[i][j][k])
            
nii_image = itk.GetImageFromArray(np_image)
itk.imwrite(nii_image, output)