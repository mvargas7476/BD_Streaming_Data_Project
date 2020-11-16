#! /bin/bash

for filename in ../stream/*; do
	echo $filename
	touch $filename
	sleep 5
done
