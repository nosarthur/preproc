#!/bin/sh

echo "image registration"

total=`find $1 -type d -mindepth 1 -maxdepth 1 |wc -l`
cDIR=`pwd`
echo $cDIR
for dir in $1*; do 
    echo $dir
    cd $dir
    /Users/nos/Dropbox/iResearch/15preproc/preproc.py t1.nii -r mag.nii
    cd $cDIR
done
