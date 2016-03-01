#!/bin/bash

INPUTS=Step1/inputs/*
mkdir Step1/usertest
for i in $INPUTS
    do
        filename=${i%.*}
        name=${filename##*/}
        echo "Testing input file $i"
        output="${name}Test.out"
        outtest="${name}.out"
        ./MicroStep1.sh $i > Step1/usertest/$output
        colordiff -b -s Step1/usertest/$output Step1/outputs/$outtest
    done