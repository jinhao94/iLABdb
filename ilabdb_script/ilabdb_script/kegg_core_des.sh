#!/bin/bash

csvtk join -t -T -H -f"1" $1 /ddn/software/omixer/pathway.mapping | perl -lane 'BEGIN{print "Module_ID\tCopy number\tCompleteness\tPathway ID"}; print $_' > $2