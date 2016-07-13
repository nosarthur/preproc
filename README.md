# preproc

Wrapper for dcm2nii and fsl flirt.

Convert dicom images in a folder to nifti or do flirt registration between
dicom images and/or nifti images.

## usage

`preproc.py [-h] [-r reference] imPath [imPath ...]`

* `imPath` and `reference` could be either dicom folders or nifti files.

## notes

* I assumed that dcm2nii and flirst could be accessed from command line directly.

