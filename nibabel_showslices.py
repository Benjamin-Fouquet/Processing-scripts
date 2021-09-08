#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 09:58:08 2021

find out the orientation of a nifti image, reorient for LPS standard (or?)

@author: benjamin

What is the goal?
Correct spatial coordinate arrangement so it fits the numpy data
"""
import nibabel as nb
import matplotlib.pyplot as plt
import itk

path = '/home/benjamin/Documents/FetalAtlas/mesh_to_image_testFolder/companion_cube_lite.nii.gz' 
path = '/home/benjamin/Documents/FetalAtlas/DataFrancois/sub-CC00060XX03_ses-12501_desc-fusion_space-T2w_dseg.nii.gz'

def show_slices(image):
    data = image.get_fdata()
    data = data.reshape(image.shape[0:3])
    xmean, ymean, zmean = [int(i/2) for i in image.shape[0:3]]
    """ Function to display row of image slices """
    slice_0 = data[xmean, :, :]
    slice_1 = data[:, ymean, :]
    slice_2 = data[:, :, zmean]
    slices = [slice_0, slice_1, slice_2]
    fig, axes = plt.subplots(1, len(slices))
    for i, slice in enumerate(slices):
        axes[i].imshow(slice.T, cmap="gray", origin="lower")
        
        
def show_itk_slices(image):
    data = itk.GetArrayFromImage(image)
    xmean, ymean, zmean = [int(i/2) for i in image.shape[0:3]]
    """ Function to display row of image slices """
    slice_0 = data[xmean, :, :]
    slice_1 = data[:, ymean, :]
    slice_2 = data[:, :, zmean]
    slices = [slice_0, slice_1, slice_2]
    fig, axes = plt.subplots(1, len(slices))
    for i, slice in enumerate(slices):
        axes[i].imshow(slice.T, cmap="gray", origin="lower")