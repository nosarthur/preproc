#!/usr/bin/env python

import os
import argparse

class C:
    pass
c = C();

parser = argparse.ArgumentParser(description=
        'Convert dicom images in a folder to nifti \
        or do flirt registration between dicom images and/or nifti images.')

parser.add_argument('-r', dest='refPath', metavar='reference', 
                        nargs=1, help='reference images')
parser.add_argument('imPath',nargs='+', help='images to be processed') 
args = parser.parse_args(namespace=c)

niftiList = []

for dicomPath in c.imPath: # convert images to 3D nifti files
    if ".nii" not in dicomPath:     # indeed a path, instead of .nii file
        os.system("dcm2nii -n -4 "+dicomPath)
        for dirName, subDirName, fileList in os.walk(dicomPath):
            for fileName in fileList:
                if ".nii.gz" in fileName.lower():
                    tmpName = os.path.join(dirName,fileName)
                    os.system("fslswapdim " +tmpName+ " x -y z "+ tmpName)
                    parDir = os.path.abspath(os.path.join(dirName, os.pardir))
                    os.system("mv "+tmpName+" "+parDir)
                    os.system("gzip -d "+os.path.join(parDir,fileName))
                    niftiList.append(os.path.join(parDir, os.path.splitext(fileName)[0]))
    else:
        niftiList.append(dicomPath) # dicomPath is a .nii file in this case

if c.refPath: # do registration
    refPath = c.refPath[0]
    if ".nii" not in refPath:     # indeed a path, instead of .nii file
        os.system("dcm2nii -n -4 "+refPath)
        for dirName, subDirName, fileList in os.walk(refPath):
            for fileName in fileList:
                if ".nii.gz" in fileName.lower():
                    tmpName = os.path.join(dirName,fileName)
                    os.system("fslswapdim " +tmpName+ " x -y z "+ tmpName)
                    parDir = os.path.abspath(os.path.join(refPath, os.pardir))
                    os.system("mv "+tmpName+" "+parDir+" && gzip -d "+fileName)
                    os.system("cp "+parDir+os.path.splitext(fileName)[0]+" ref.nii")
    else:   # input is .nii file
        os.system("cp "+refPath+" ref.nii")

    for fileName in niftiList:
        regName = os.path.splitext(fileName)[0] + "_reg.nii"
        myCmd = "flirt -in "+fileName+" -ref ref.nii -out "+ regName \
                    + " -omat im_reg.mat -bins 256 \
                    -cost corratio -searchrx -30 30 -searchry -30 30 -searchrz -30 30 \
                    -dof 12 -interp trilinear"
        print myCmd
        os.system(myCmd)
        os.system("gzip -d "+regName +".gz")



