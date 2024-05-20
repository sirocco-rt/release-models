#!/bin/bash
RUNDIR=$1
mkdir -p Results
cp $RUNDIR/*.txt Results
cp $RUNDIR/*.sig Results
cp $RUNDIR/*spec Results

